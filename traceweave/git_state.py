"""Read-only Git state collection for Traceweave.

Uses Git itself as the source of truth. Only safe, read-only commands are run:

- ``git rev-parse HEAD``
- ``git branch --show-current``
- ``git status --porcelain=v1 -z``
- ``git remote get-url origin``

Nothing here commits, pushes, checks out, resets, cleans or rebases.
"""

from __future__ import annotations

import re
import subprocess
from urllib.parse import urlsplit
from dataclasses import dataclass, field
from pathlib import Path


class GitError(RuntimeError):
    """Raised when a required Git command fails or no repository is found."""


@dataclass
class GitState:
    branch: str | None
    head_commit: str | None
    working_tree: str  # "clean" | "dirty" | "unknown"
    changed_files: list[str] = field(default_factory=list)
    repository: str | None = None


def _run_git(repo_root: Path, args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo_root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
        check=False,
    )


def _sanitize_repository_remote(remote: str, root: Path) -> str:
    """Return a non-secret repository identifier derived from origin.

    Userinfo, query strings and fragments are never persisted. Local/file
    remotes fall back to the repository directory name to avoid leaking
    machine-local paths.
    """
    value = remote.strip()
    if not value:
        return root.name

    # Local filesystem / UNC / file:// remotes can expose private paths.
    if (
        value.startswith(("/", "./", "../", "\\"))
        or re.match(r"^[A-Za-z]:[\\/]", value)
        or value.lower().startswith("file://")
    ):
        return root.name

    parsed = urlsplit(value)
    if parsed.scheme in {"http", "https", "ssh", "git"} and parsed.hostname:
        host = parsed.hostname
        if parsed.port:
            host = f"{host}:{parsed.port}"
        path = parsed.path.lstrip("/")
        return f"{host}/{path}" if path else host

    # SCP-style SSH remote, e.g. git@github.com:owner/repo.git.
    # Drop the username entirely; only host + repository path are retained.
    match = re.match(r"^(?:[^@/:\s]+@)?([^/:\s]+):(.+)$", value)
    if match and "\\" not in value:
        host, path = match.groups()
        path = path.lstrip("/")
        return f"{host}/{path}" if path else host

    return root.name


def repo_root_from(path: Path | None = None) -> Path:
    """Resolve the repository root; raises GitError when not inside a repo."""
    start = path or Path.cwd()
    proc = _run_git(start, ["rev-parse", "--show-toplevel"])
    if proc.returncode != 0:
        raise GitError(
            f"Not a Git repository: {start}. "
            f"stderr: {proc.stderr.strip()[:200]}"
        )
    root = proc.stdout.strip()
    if not root:
        raise GitError(f"git rev-parse --show-toplevel returned nothing for {start}")
    return Path(root)


def collect(repo_root: Path | None = None) -> GitState:
    """Collect the current Git state of the repository."""
    root = repo_root_from(repo_root)
    state = GitState(branch=None, head_commit=None, working_tree="unknown")

    branch_proc = _run_git(root, ["branch", "--show-current"])
    if branch_proc.returncode == 0 and branch_proc.stdout.strip():
        state.branch = branch_proc.stdout.strip()

    head_proc = _run_git(root, ["rev-parse", "HEAD"])
    if head_proc.returncode == 0 and head_proc.stdout.strip():
        state.head_commit = head_proc.stdout.strip()

    remote_proc = _run_git(root, ["remote", "get-url", "origin"])
    if remote_proc.returncode == 0 and remote_proc.stdout.strip():
        state.repository = _sanitize_repository_remote(remote_proc.stdout, root)
    else:
        # Fall back to the repository name — a fact, not an inference.
        state.repository = root.name

    status_proc = _run_git(root, ["status", "--porcelain=v1", "-z"])
    if status_proc.returncode == 0:
        records = [record for record in status_proc.stdout.split("\0") if record]
        state.working_tree = "clean" if not records else "dirty"
        index = 0
        while index < len(records):
            record = records[index]
            if len(record) >= 3 and record[2] == " ":
                xy = record[:2]
                path = record[3:]
                state.changed_files.append(path)
                if "R" in xy or "C" in xy:
                    # In -z mode, the next NUL record is the source path.
                    index += 1
            index += 1
    else:
        state.working_tree = "unknown"

    return state
