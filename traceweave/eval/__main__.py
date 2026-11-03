"""Command line: python -m traceweave.eval run CASE --log NATIVE_JSONL."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from .engine import evaluate_case, load_case


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m traceweave.eval")
    parser.add_argument("command", choices=["run"])
    parser.add_argument("case", type=Path, help="frozen case JSON")
    parser.add_argument("--log", type=Path, help="source matching case.source.sha256")
    parser.add_argument("--repo", action="append", type=Path, default=[], help="Git repository for claims; repeatable")
    args = parser.parse_args(argv)
    try:
        case = load_case(args.case)
        report = evaluate_case(case, evidence=args.log, repos=args.repo)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"traceeval: invalid case: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return {"passed": 0, "failed": 1, "integrity_failed": 1, "not_observed": 2, "invalid_input": 2}[report["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
