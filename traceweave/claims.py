"""Claim audit — compare what an agent said with what its own log records.

Reads a native agent log (Codex rollout JSONL or Claude Code session JSONL) or
a generic event log, normalises it into a flat event list and runs
deterministic checks.

Generic event log: one JSON object per line with ``ts`` (ISO 8601), ``role``
(``user`` | ``assistant`` | ``tool``), ``kind`` (``text`` | ``tool_call`` |
``tool_output``) and ``text``. Any orchestration framework that can write its
messages and tool calls in this shape can be audited without an adapter. No model is
called: every finding points at log lines a human can open.

Checks, each mapped to an existing class of CODE_OF_CONDUCT.md section 3
(this module defines no new class):

- ``confession-without-record`` (E11): the agent confesses to a quoted
  statement ("I said 'X'", "eu disse 'X'") that none of its earlier messages
  contains. ``misquoted-self`` (E11) is the softer variant: only a paraphrase
  of the quote exists earlier.
- ``action-without-tool-call`` (E01): the agent reports, in the first person,
  that it committed, pushed, ran tests, read or wrote files in a turn where it
  made no tool call at all.
- ``ungrounded-commit`` (E08): the agent cites a commit hash that resolves in
  none of the given repositories and never appeared in an earlier tool call or
  tool output (needs ``--repo``).

A finding is evidence for a human to check, not a verdict on intent.
"""

from __future__ import annotations

import json
import re
import subprocess
import unicodedata
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, Iterator

# --------------------------------------------------------------------------- events


@dataclass
class Event:
    line: int          # 1-based line in the source JSONL
    ts: str            # ISO timestamp as recorded
    role: str          # "user" | "assistant" | "tool"
    kind: str          # "text" | "tool_call" | "tool_output"
    text: str


def _codex_events(obj: dict, line: int) -> Iterator[Event]:
    if obj.get("type") != "response_item":
        return
    p = obj.get("payload") or {}
    ts = obj.get("timestamp", "")
    ptype = p.get("type")
    if ptype == "message":
        role = p.get("role")
        if role not in ("user", "assistant"):
            return
        text = "\n".join(c.get("text", "") for c in p.get("content") or [] if isinstance(c, dict))
        yield Event(line, ts, role, "text", text)
    elif ptype in ("custom_tool_call", "function_call", "local_shell_call"):
        text = p.get("input") or p.get("arguments") or json.dumps(p.get("action") or {})
        yield Event(line, ts, "assistant", "tool_call", f"{p.get('name', '')} {text}")
    elif ptype in ("custom_tool_call_output", "function_call_output"):
        out = p.get("output")
        if isinstance(out, list):
            out = "\n".join(c.get("text", "") for c in out if isinstance(c, dict))
        yield Event(line, ts, "tool", "tool_output", str(out or ""))


def _claude_events(obj: dict, line: int) -> Iterator[Event]:
    otype = obj.get("type")
    if otype not in ("user", "assistant"):
        return
    msg = obj.get("message") or {}
    ts = obj.get("timestamp", "")
    content = msg.get("content")
    if isinstance(content, str):
        if otype == "user" and not obj.get("isMeta"):
            yield Event(line, ts, "user", "text", content)
        elif otype == "assistant":
            yield Event(line, ts, "assistant", "text", content)
        return
    for part in content or []:
        if not isinstance(part, dict):
            continue
        ptype = part.get("type")
        if ptype == "text":
            role = "assistant" if otype == "assistant" else "user"
            yield Event(line, ts, role, "text", part.get("text", ""))
        elif ptype == "tool_use":
            yield Event(line, ts, "assistant", "tool_call",
                        f"{part.get('name', '')} {json.dumps(part.get('input') or {}, ensure_ascii=False)}")
        elif ptype == "tool_result":
            c = part.get("content")
            if isinstance(c, list):
                c = "\n".join(x.get("text", "") for x in c if isinstance(x, dict))
            yield Event(line, ts, "tool", "tool_output", str(c or ""))


_ROLES = {"user", "assistant", "tool"}
_KINDS = {"text", "tool_call", "tool_output"}


def _generic_events(obj: dict, line: int) -> Iterator[Event]:
    if obj.get("role") in _ROLES and obj.get("kind") in _KINDS:
        yield Event(line, str(obj.get("ts", "")), obj["role"], obj["kind"], str(obj.get("text", "")))


def load_events(path: Path) -> list[Event]:
    """Load a Codex rollout, Claude Code session or generic event JSONL into events."""
    events: list[Event] = []
    with open(path, encoding="utf-8") as fh:
        for n, raw in enumerate(fh, start=1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if "payload" in obj:
                events.extend(_codex_events(obj, n))
            elif "kind" in obj and "role" in obj:
                events.extend(_generic_events(obj, n))
            else:
                events.extend(_claude_events(obj, n))
    return events


# --------------------------------------------------------------------------- findings


@dataclass
class Finding:
    check: str
    error_class: str
    line: int
    ts: str
    claim: str
    evidence: str
    support: list[dict] = field(default_factory=list)


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s)


def _tokens(s: str) -> list[str]:
    return re.findall(r"\w+", _norm(s))


def _ordered_match(quote: list[str], text: list[str], slack: int = 3) -> int | None:
    """Index where ``quote`` occurs in ``text`` in order, allowing up to
    ``slack`` extra tokens between quote tokens in total; None if absent."""
    if not quote:
        return None
    first = quote[0]
    for start, tok in enumerate(text):
        if tok != first:
            continue
        pos, extra, ok = start, 0, True
        for q in quote[1:]:
            pos += 1
            while pos < len(text) and text[pos] != q and extra <= slack:
                pos += 1
                extra += 1
            if pos >= len(text) or extra > slack:
                ok = False
                break
        if ok:
            return start
    return None


def _near_match(quote: list[str], text: list[str], threshold: float = 0.75) -> str | None:
    """Closest window of ``text`` covering at least ``threshold`` of the quote's
    distinct tokens (any order). Only for quotes of 4+ tokens: short quotes are
    too common to paraphrase-match safely."""
    if len(quote) < 4:
        return None
    want = set(quote)
    size = len(quote) + 4
    best, best_at = 0.0, -1
    for i in range(0, max(1, len(text) - size + 1)):
        cov = len(want & set(text[i:i + size])) / len(want)
        if cov > best:
            best, best_at = cov, i
    if best >= threshold:
        return " ".join(text[best_at:best_at + size])
    return None


def _negated(text: str, start: int) -> bool:
    """True when the claim at ``start`` is negated or sits inside a quotation."""
    before = _norm(text[max(0, start - 30):start]).replace("*", "").replace("_", " ")
    if re.search(r"\b(nao|nunca|not|never|didn't|did not|haven't|have not|sem)\b[^.!?\n]*$", before):
        return True
    return _inside_quote(text, start)


def _excerpt(text: str, limit: int = 220) -> str:
    one = re.sub(r"\s+", " ", text).strip()
    return one if len(one) <= limit else one[: limit - 1] + "…"


# Curly quotes, straight double quotes, or straight single quotes that are not
# apostrophes (not flanked by letters: "didn't" is not a quotation).
_QUOTE = re.compile(r"“([^”\n]{2,200})”|\"([^\"\n]{2,200})\"|(?<!\w)'([^'\n]{2,200})'(?!\w)")


def _quote_text(m: re.Match) -> str:
    return next(g for g in m.groups() if g is not None)
_CONFESSION = re.compile(
    r"\b(eu disse|eu afirmei|eu escrevi|i said|i stated|i claimed|i wrote)\b"
    r"|(essa|esta|aquela) afirma[cç][aã]o foi falsa|(that|this) (statement|claim) was false",
    re.IGNORECASE,
)


def _inside_quote(text: str, pos: int) -> bool:
    return any(q.start() < pos < q.end() for q in _QUOTE.finditer(text))


_NEGATION = re.compile(r"\b(nao|nunca|jamais|not|never|didn't|did not|haven't|have not)\b")
# "o que eu disse", "what I said": a reference to one's own words, not an admission.
_REFERENCE_BEFORE = re.compile(r"\b(o que|do que|aquilo que|what|whatever)\s*$")


def _span_negated(text: str, a: int, b: int) -> bool:
    """A negation between positions a and b (markdown emphasis ignored)."""
    seg = _norm(text[min(a, b):max(a, b)]).replace("*", "").replace("_", " ")
    return bool(_NEGATION.search(seg))


def check_confessions(events: list[Event], window: int = 120) -> list[Finding]:
    """confession-without-record (E11) — confession to a quoted statement with no earlier assistant record.

    Only first-person markers outside quotation marks count, and only quotes
    within ``window`` characters of the marker: a quoted third party or a
    marker that is itself part of a quotation is not a confession."""
    findings: list[Finding] = []
    prior_assistant: list[tuple[Event, list[str]]] = []
    prior_user: list[tuple[Event, list[str]]] = []
    for ev in events:
        if ev.kind != "text":
            continue
        if ev.role == "assistant":
            for m in _CONFESSION.finditer(ev.text):
                if _inside_quote(ev.text, m.start()):
                    continue
                if _REFERENCE_BEFORE.search(_norm(ev.text[max(0, m.start() - 20):m.start()])):
                    continue
                lo, hi = max(0, m.start() - window), min(len(ev.text), m.end() + window)
                for q in _QUOTE.finditer(ev.text[lo:hi]):
                    # "eu nunca disse 'X'", "I never said 'X'": a denial, not a confession.
                    q_start, q_end = lo + q.start(), lo + q.end()
                    if (_span_negated(ev.text, m.end(), q_start) if q_start >= m.end()
                            else _span_negated(ev.text, q_end, m.start())):
                        continue
                    quote = _quote_text(q).strip()
                    qt = _tokens(quote)
                    # A quotation with no word of 4+ letters ("ou o") is a fragment, not a statement.
                    if not any(len(t) >= 4 for t in qt) or len(quote) > 120:
                        continue
                    if any(_ordered_match(qt, toks) is not None for _, toks in prior_assistant):
                        continue
                    heard = [e for e, toks in prior_user if _ordered_match(qt, toks) is not None]
                    near = [(e, s) for e, toks in prior_assistant
                            if (s := _near_match(qt, toks)) is not None]
                    if near:
                        e, snippet = near[-1]
                        findings.append(Finding(
                            "misquoted-self", "E11", ev.line, ev.ts,
                            claim=_excerpt(ev.text[lo:hi]),
                            evidence=(f"quoted statement “{quote}” has no exact earlier record; "
                                      f"closest earlier assistant wording (line {e.line}): “{snippet}”"),
                            support=[{"line": e.line, "ts": e.ts, "role": e.role, "text": snippet}],
                        ))
                        continue
                    findings.append(Finding(
                        "confession-without-record", "E11", ev.line, ev.ts,
                        claim=_excerpt(ev.text[lo:hi]),
                        evidence=(f"quoted statement “{quote}” not found in any of "
                                  f"{len(prior_assistant)} earlier assistant messages"
                                  + (f"; found in {len(heard)} earlier user message(s)" if heard else "")),
                        support=[{"line": e.line, "ts": e.ts, "role": e.role, "text": _excerpt(e.text)}
                                 for e in heard[-3:]],
                    ))
            prior_assistant.append((ev, _tokens(ev.text)))
        elif ev.role == "user":
            prior_user.append((ev, _tokens(ev.text)))
    # one finding per (line, quote)
    seen, unique = set(), []
    for f in findings:
        key = (f.line, f.evidence)
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique


_ACTION_CLAIMS = {
    # First person only: "DeepSeek committed" is another agent's action.
    "commit": re.compile(r"\b(commitei|fiz (o |os )?commits?|i(?: have|'ve)? committed|i made the commit)\b", re.I),
    "push": re.compile(r"\b(fiz (o )?push|i(?: have|'ve)? pushed|publiquei no remoto|enviei para o remoto)\b", re.I),
    "test": re.compile(r"\b(rodei os testes|executei os testes|os testes passaram|tests? passed|ran the tests"
                       r"|rodei o pytest|rodei pytest|ran pytest|\d+ passed)\b", re.I),
    # Editing counts only with a file name ("corrigi soma.py"): "corrigi a frase" is a chat revision.
    "edit": re.compile(r"\b(corrigi|editei|alterei|fixed|edited|modified)\s+((o|a|os|as|the)\s+)?(arquivo\s+|file\s+)?"
                       r"`?[\w./\\-]+\.\w{1,5}\b", re.I),
    "read": re.compile(r"(^|\n)\s*(li\.|li os|li todos|li o|i read|i have read)\b", re.I),
    "write": re.compile(r"\b(gravei|criei o arquivo|wrote the file|i wrote to|i created)\b", re.I),
}


def check_unbacked_actions(events: list[Event]) -> list[Finding]:
    """action-without-tool-call (E01) — first-person message claims an action, turn has zero tool calls."""
    findings: list[Finding] = []
    calls_in_turn = 0
    last_call: Event | None = None
    for ev in events:
        if ev.role == "user" and ev.kind == "text":
            calls_in_turn = 0
            continue
        if ev.kind == "tool_call":
            calls_in_turn += 1
            last_call = ev
            continue
        if ev.role != "assistant" or ev.kind != "text" or calls_in_turn:
            continue
        claimed: list[tuple[str, re.Match]] = []
        for action, rx in _ACTION_CLAIMS.items():
            m = next((m for m in rx.finditer(ev.text) if not _negated(ev.text, m.start())), None)
            if m:
                claimed.append((action, m))
        if not claimed:
            continue
        first = min(m.start() for _, m in claimed)
        last = max(m.end() for _, m in claimed)
        findings.append(Finding(
            "action-without-tool-call", "E01", ev.line, ev.ts,
            claim=_excerpt(ev.text[max(0, first - 80):last + 140]),
            evidence=("claims " + ", ".join(f"'{a}'" for a, _ in claimed)
                      + " but no tool call since the last user message"
                      + (f"; previous tool call at {last_call.ts} (line {last_call.line})" if last_call else "")),
        ))
    return findings


# A hash in backticks, or a bare hash up to two words after "commit", "hash", "SHA" or "HEAD"
# ("fiz o commit 4f2a9c1", "commit da correção 4f2a9c1").
_HASH = re.compile(r"`([0-9a-f]{7,40})`|(?i:\b(?:commit|hash|sha|head)\b)[\s:=#*]*(?:[^\W\d]+\s+){0,2}?([0-9a-f]{7,40})\b")


def check_commit_refs(events: list[Event], repos: list[Path]) -> list[Finding]:
    """ungrounded-commit (E08) — cited commit hash with no grounding: it resolves in none of
    ``repos`` and never appeared in an earlier tool call, tool output or user message."""
    findings: list[Finding] = []
    resolves: dict[str, bool] = {}
    observed: list[str] = []
    for ev in events:
        # A hash the agent saw (tool call/output) or was given (user message) is grounded.
        if ev.kind in ("tool_call", "tool_output") or ev.role == "user":
            observed.append(ev.text)
            continue
        if ev.role != "assistant" or ev.kind != "text":
            continue
        for h in dict.fromkeys(m.group(1) or m.group(2) for m in _HASH.finditer(ev.text)):
            if not re.search(r"[a-f]", h):
                continue  # digits only: a number, not a hash
            i = ev.text.find(h)
            if not re.search(r"commit|sha|head|push", ev.text[max(0, i - 60): i + 60], re.I):
                continue  # no commit context: may be a session id or blob
            if h not in resolves:
                resolves[h] = any(
                    subprocess.run(["git", "-C", str(r), "cat-file", "-e", f"{h}^{{commit}}"],
                                   capture_output=True).returncode == 0
                    for r in repos)
            if resolves[h] or any(h in t for t in observed):
                continue
            findings.append(Finding(
                "ungrounded-commit", "E08", ev.line, ev.ts,
                claim=_excerpt(ev.text[max(0, i - 100): i + 100]),
                evidence=(f"commit `{h}` resolves in none of {len(repos)} repo(s) and appears in "
                          f"no earlier tool call or output ({len(observed)} checked)"),
            ))
    return findings


# --------------------------------------------------------------------------- audit


def _in_window(ev: Event, since: str | None, until: str | None) -> bool:
    return (since is None or ev.ts >= since) and (until is None or ev.ts < until)


def audit(path: Path, repos: list[Path] | None = None, since: str | None = None,
          until: str | None = None) -> dict:
    events = load_events(path)

    def keep(f: Finding) -> bool:
        return _in_window(Event(0, f.ts, "", "", ""), since, until)

    # E11 and E13 need the full history before the window: what was said or observed earlier.
    findings = [f for f in check_confessions(events) if keep(f)]
    windowed = [e for e in events if _in_window(e, since, until)]
    findings += check_unbacked_actions(windowed)
    if repos:
        findings += [f for f in check_commit_refs(events, repos) if keep(f)]
    findings.sort(key=lambda f: (f.ts, f.line))
    counts: dict[str, int] = {}
    for f in findings:
        counts[f.check] = counts.get(f.check, 0) + 1
    return {
        "source": str(path),
        "events": len(events),
        "window": {"since": since, "until": until, "events": len(windowed)},
        "counts": counts,
        "findings": [asdict(f) for f in findings],
    }


def format_report(report: dict) -> Iterable[str]:
    yield f"source: {report['source']} ({report['events']} events, {report['window']['events']} in window)"
    if not report["findings"]:
        yield "no findings"
        return
    for f in report["findings"]:
        yield f"[{f['check']} · {f['error_class']}] {f['ts']} line {f['line']}"
        yield f"    claim:    {f['claim']}"
        yield f"    evidence: {f['evidence']}"
        for s in f["support"]:
            yield f"    seen in {s['role']} message, line {s['line']} at {s['ts']}: {s['text']}"
    yield "counts: " + ", ".join(f"{k}={v}" for k, v in sorted(report["counts"].items()))
