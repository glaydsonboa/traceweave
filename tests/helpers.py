"""Shared helpers for Traceweave tests.

Every test works against its own temporary Git repository — never against the
Traceweave repository itself.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


def run_git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    return proc.stdout.strip()


def init_repo(repo: Path) -> str:
    """Create a temporary Git repo with one initial commit; returns its hash."""
    repo.mkdir(parents=True, exist_ok=True)
    run_git(repo, "init", "-q")
    run_git(repo, "config", "user.email", "test@example.com")
    run_git(repo, "config", "user.name", "Test User")
    (repo / "README.md").write_text("# test repo\n", encoding="utf-8")
    run_git(repo, "add", "README.md")
    run_git(repo, "commit", "-q", "-m", "initial commit")
    return run_git(repo, "rev-parse", "HEAD")


# Keep TemporaryDirectory objects alive for the whole test run — a TemporaryDirectory
# that goes out of scope is cleaned up immediately, deleting the repo mid-test.
_KEEPALIVE: list[tempfile.TemporaryDirectory] = []


def new_repo() -> Path:
    tmp = tempfile.TemporaryDirectory(prefix="traceweave-test-")
    _KEEPALIVE.append(tmp)
    path = Path(tmp.name)
    init_repo(path)
    return path


def new_empty_repo() -> Path:
    """A Git repository with no commit yet (unborn branch)."""
    tmp = tempfile.TemporaryDirectory(prefix="traceweave-test-empty-")
    _KEEPALIVE.append(tmp)
    path = Path(tmp.name)
    path.mkdir(parents=True, exist_ok=True)
    run_git(path, "init", "-q")
    run_git(path, "config", "user.email", "test@example.com")
    run_git(path, "config", "user.name", "Test User")
    return path
