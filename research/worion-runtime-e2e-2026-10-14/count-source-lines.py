#!/usr/bin/env python3
"""Count physical lines in selected tracked source files at an exact Git commit.

This reads Git objects only. It does not infer who authored or generated a line.
"""

import argparse
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path


def run(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--scope", required=True, type=Path)
    args = parser.parse_args()

    scope = json.loads(args.scope.read_text(encoding="utf-8"))
    roots = scope["include_roots"]
    if not roots or any("/" in root or ".." in root or root.startswith("-") for root in roots):
        parser.error("include_roots must be plain top-level directory names")
    commit = run(args.repo, "rev-parse", "--verify", "--end-of-options", f"{args.commit}^{{commit}}").strip()
    output = run(args.repo, "grep", "-I", "-c", "-e", "^", commit, "--", *roots)

    extensions = set(scope["extensions"])
    excluded_dirs = set(scope["exclude_directory_names"])
    excluded_name = re.compile(scope["exclude_filename_regex"])
    group_by_root = {
        root: group for group, members in scope["groups"].items() for root in members
    }
    totals = defaultdict(lambda: {"files": 0, "physical_lines": 0})
    for record in output.splitlines():
        path_and_count = record.split(":", 1)[1]
        path, count_text = path_and_count.rsplit(":", 1)
        parts = path.split("/")
        if Path(path).suffix.lower() not in extensions:
            continue
        if any(part.lower() in excluded_dirs for part in parts[:-1]):
            continue
        if excluded_name.search(parts[-1]):
            continue
        group = group_by_root[parts[0]]
        totals[group]["files"] += 1
        totals[group]["physical_lines"] += int(count_text)

    result = {
        "commit": commit,
        "method": "git grep -I -c -e '^' over the published scope; blank and comment lines included",
        "groups": dict(sorted(totals.items())),
        "total_files": sum(item["files"] for item in totals.values()),
        "total_physical_lines": sum(item["physical_lines"] for item in totals.values()),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
