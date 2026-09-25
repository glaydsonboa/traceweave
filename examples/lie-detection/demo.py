"""Watch Traceweave catch four lies an AI agent could write into a checkpoint.

Run it (after ``pip install -e .``)::

    python examples/lie-detection/demo.py

It builds a throwaway Git repository, records one honest checkpoint, then plants four lies
taken from a real external bench test (24/09/2026). Each lie is checked twice:

* ``verify``         — structural rules only (SPEC.md §10). It never touches Git.
* ``verify --repo``  — also checks the Git claims against the real repository.

The point is the gap between the two columns: a well-formed record can still be false. A hash
chain would seal lies 1 and 2 with perfect integrity; only a check against reality catches them.
"""

from __future__ import annotations

import contextlib
import copy
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from traceweave.cli import main as traceweave
from traceweave.verify import verify, verify_against_repo


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def honest_checkpoint(repo: Path) -> dict:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        traceweave(["checkpoint", "--path", str(repo), "--executor", "demo-agent",
                    "--summary", "honest checkpoint"])
    return json.loads(Path(out.getvalue().strip()).read_text(encoding="utf-8"))


def lies(cp: dict, repo: Path):
    """Yield (claim, forged checkpoint, side effect on the repo)."""
    c1 = copy.deepcopy(cp)
    c1["git"]["head_commit"] = "deadbeef" * 5
    yield "1. \"I committed it\" - head_commit that does not exist", c1, None

    c2 = copy.deepcopy(cp)
    c2["git"]["working_tree"] = "clean"
    yield "2. \"Nothing left uncommitted\" - working tree claimed clean", c2, \
        lambda: (repo / "forgotten.txt").write_text("uncommitted work\n", encoding="utf-8")

    c3 = copy.deepcopy(cp)
    c3["status"] = "complete"
    yield "3. \"Done\" - status complete while tests were not run", c3, None

    c4 = copy.deepcopy(cp)
    c4["status"] = "complete"
    c4["tests"] = [{"command": "pytest", "result": "passed", "evidence": None}]
    c4["git"]["working_tree"] = "clean"
    yield "4. \"Tests passed\" - passed with no evidence at all", c4, None


def mark(ok: bool) -> str:
    return "accepted (missed)" if ok else "REJECTED (caught)"


def run() -> list[tuple[str, bool, bool]]:
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        git(repo, "init", "-q")
        git(repo, "-c", "user.email=demo@example.invalid", "-c", "user.name=demo",
            "commit", "-q", "--allow-empty", "-m", "initial")
        cp = honest_checkpoint(repo)
        rows.append(("0. honest checkpoint", verify(cp).ok, verify_against_repo(cp, repo).ok))
        for claim, forged, effect in lies(cp, repo):
            if effect:
                effect()
            rows.append((claim, verify(forged).ok, verify_against_repo(forged, repo).ok and verify(forged).ok))
    return rows


def report(rows) -> None:
    width = max(len(r[0]) for r in rows)
    print(f"{'claim':<{width}}  {'verify':<18}  verify --repo")
    print("-" * (width + 40))
    for claim, structural, reality in rows:
        if claim.startswith("0."):
            print(f"{claim:<{width}}  {'passes':<18}  passes")
        else:
            print(f"{claim:<{width}}  {mark(structural):<18}  {mark(reality)}")
    print()
    print("Lies 1-2 are well-formed records: only the check against the repository catches them.")
    print("Lies 3-4 break SPEC.md section 10 rule 7: 'complete' needs evidence for every test and a clean tree.")


if __name__ == "__main__":
    results = run()
    report(results)
    honest_ok = results[0][1] and results[0][2]
    all_caught = all(not reality for _, _, reality in results[1:])
    sys.exit(0 if honest_ok and all_caught else 1)
