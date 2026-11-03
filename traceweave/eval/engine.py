"""Evaluate frozen, hash-bound agent claim detection cases.

Evidence is read locally and never modified. A detector finding is not an
independent proof that the underlying event did or did not occur.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable, Mapping

SCHEMA = "traceweave.eval/0.1"
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SOURCES = {"native_jsonl", "markdown_transcript"}


def load_case(path: Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_case(data)
    return data


def validate_case(case: Mapping[str, Any]) -> None:
    if not isinstance(case, dict) or case.get("schema") != SCHEMA:
        raise ValueError(f"case.schema must equal {SCHEMA!r}")
    if not isinstance(case.get("case_id"), str) or not case["case_id"].strip():
        raise ValueError("case.case_id must be a nonempty string")
    source = case.get("source")
    if not isinstance(source, dict) or source.get("kind") not in SOURCES:
        raise ValueError(f"source.kind must be one of {sorted(SOURCES)}")
    digest = source.get("sha256")
    if not isinstance(digest, str) or not SHA256.fullmatch(digest):
        raise ValueError("source.sha256 must be a lowercase 64-character SHA-256")
    expectations = case.get("expectations")
    if not isinstance(expectations, list):
        raise ValueError("case.expectations must be a list, possibly empty")
    seen = set()
    for index, expectation in enumerate(expectations):
        if not isinstance(expectation, dict):
            raise ValueError(f"expectations[{index}] must be an object")
        check = expectation.get("check")
        if not isinstance(check, str) or not check.strip() or check in seen:
            raise ValueError(f"expectations[{index}].check must be unique and nonempty")
        seen.add(check)
        low, high = expectation.get("min_count"), expectation.get("max_count")
        if not isinstance(low, int) or isinstance(low, bool) or low < 0:
            raise ValueError(f"expectations[{index}].min_count must be nonnegative integer")
        if high is not None and (not isinstance(high, int) or isinstance(high, bool) or high < low):
            raise ValueError(f"expectations[{index}].max_count must be integer >= min_count")


def _out(case: Mapping[str, Any], status: str, *, reason: str,
         observed_sha256: str | None = None, events: int | None = None,
         rules: list[dict] | None = None, findings: Mapping[str, int] | None = None) -> dict[str, Any]:
    rules = rules or []
    return {
        "schema": SCHEMA,
        "case_id": case["case_id"],
        "status": status,
        "reason": reason,
        "source_sha256": case["source"]["sha256"],
        "observed_sha256": observed_sha256,
        "events": events,
        "rules": rules,
        "finding_counts": dict(sorted((findings or {}).items())),
        "score": (sum(rule["passed"] for rule in rules) / len(rules)) if rules else None,
    }


def evaluate_case(case: Mapping[str, Any], *, evidence: Path | None,
                  repos: Iterable[Path] = ()) -> dict[str, Any]:
    """Compare detector output with a frozen case without interpreting intent.

    Missing evidence => not_observed. A changed byte => integrity_failed.
    Markdown-derived transcripts can be registered but cannot stand in for the
    native JSONL required by the current claims detector.
    """
    validate_case(case)
    if evidence is None or not Path(evidence).is_file():
        return _out(case, "not_observed", reason="source file not available")
    path = Path(evidence)
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != case["source"]["sha256"]:
        return _out(case, "integrity_failed", reason="source SHA-256 mismatch", observed_sha256=actual)
    if case["source"]["kind"] != "native_jsonl":
        return _out(case, "not_observed", reason="Markdown is custody evidence, not a native tool-event log", observed_sha256=actual)
    if not case["expectations"]:
        return _out(case, "not_observed", reason="no frozen expectations", observed_sha256=actual)

    # Import only after custody checks. Existing Traceweave detection is reused,
    # not reproduced as a second, divergent interpreter.
    from traceweave.claims import audit

    try:
        report = audit(path, repos=list(repos))
    except (OSError, ValueError, UnicodeError) as exc:
        return _out(case, "invalid_input", reason=f"cannot audit native source: {type(exc).__name__}", observed_sha256=actual)
    events = report.get("events", 0)
    if not isinstance(events, int) or events <= 0:
        return _out(case, "invalid_input", reason="no recognized native log events", observed_sha256=actual, events=0)
    counts = report.get("counts", {})
    rules = []
    for exp in case["expectations"]:
        observed = counts.get(exp["check"], 0)
        passed = observed >= exp["min_count"] and (exp.get("max_count") is None or observed <= exp["max_count"])
        rules.append({
            "check": exp["check"],
            "min_count": exp["min_count"],
            "max_count": exp.get("max_count"),
            "observed_count": observed,
            "passed": passed,
        })
    passed_all = all(rule["passed"] for rule in rules)
    return _out(case, "passed" if passed_all else "failed",
                reason="frozen detector expectations satisfied" if passed_all else "detector differed from frozen expectations",
                observed_sha256=actual, events=events, rules=rules, findings=counts)
