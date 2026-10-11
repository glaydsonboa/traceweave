"""Claude Code Stop hook — audit the agent's last turn against its own log.

Reads the hook input from stdin (``session_id``, ``transcript_path``, ``cwd``,
``stop_hook_active``), then:

1. hashes the session transcript as it is at stop time (SHA-256 and size);
2. runs ``traceweave.claims.audit`` and keeps findings from the last turn
   (at or after the last user message);
3. appends one JSON line to ``<cwd>/.traceweave/claims/<session_id>.jsonl``;
4. reports findings: as a message to the user by default, or, with
   ``--block``, by asking the agent to address them before it stops.

It never blocks twice in a row (``stop_hook_active``), so it cannot loop.

The hash fixes what the transcript contained at stop time. It does not prove
the transcript is true, and it does not stop an agent from writing a false
report: it makes a later edit of that report detectable.

Configuration (``.claude/settings.json``)::

    {"hooks": {"Stop": [{"hooks": [{"type": "command",
        "command": "python tools/claude-code-claims-hook.py --repo ."}]}]}}
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from traceweave.claims import audit, load_events  # noqa: E402


def _last_user_ts(path: Path) -> str | None:
    users = [e.ts for e in load_events(path) if e.role == "user" and e.kind == "text"]
    return users[-1] if users else None


def run(hook_input: dict, repos: list[Path], block: bool) -> tuple[int, dict | None]:
    transcript = Path(hook_input.get("transcript_path") or "")
    if not transcript.is_file():
        return 0, {"systemMessage": f"traceweave claims: transcript not found ({transcript}); nothing audited"}

    data = transcript.read_bytes()
    report = audit(transcript, repos=repos, since=_last_user_ts(transcript))
    record = {
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "session_id": hook_input.get("session_id"),
        "transcript": str(transcript),
        "transcript_sha256": hashlib.sha256(data).hexdigest(),
        "transcript_bytes": len(data),
        "findings": report["findings"],
    }
    out_dir = Path(hook_input.get("cwd") or ".") / ".traceweave" / "claims"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / f"{hook_input.get('session_id') or 'unknown'}.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    if not report["findings"]:
        return 0, None
    lines = [f"- [{f['check']} · {f['error_class']}] line {f['line']}: {f['evidence']}" for f in report["findings"]]
    summary = "traceweave claims found statements in the last turn that the log does not back:\n" + "\n".join(lines)
    if block and not hook_input.get("stop_hook_active"):
        return 0, {"decision": "block",
                   "reason": summary + "\nCheck each one against the record and correct the report before stopping."}
    return 0, {"systemMessage": summary}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", type=Path, action="append", default=[],
                        help="repository used to resolve cited commits; repeatable")
    parser.add_argument("--block", action="store_true",
                        help="ask the agent to address findings before stopping (once)")
    args = parser.parse_args(argv)
    try:
        hook_input = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        hook_input = {}
    code, output = run(hook_input, args.repo, args.block)
    if output is not None:
        print(json.dumps(output, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
