"""Traceweave MCP server."""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
from pathlib import Path
from typing import Iterable

from mcp.server import MCPServer

mcp = MCPServer("Traceweave")


def _root() -> Path:
    configured = os.environ.get("TRACEWEAVE_ROOT")
    root = Path(configured).expanduser() if configured else Path.cwd()
    root = root.resolve()
    if not (root / ".git").exists():
        raise RuntimeError(f"TRACEWEAVE_ROOT is not a Git repository: {root}")
    return root


def _scopes() -> set[str]:
    raw = os.environ.get("TRACEWEAVE_MCP_SCOPES", "read")
    return {item.strip().lower() for item in raw.split(",") if item.strip()}


def _require(scope: str) -> None:
    if scope not in _scopes():
        raise PermissionError(
            f"Traceweave MCP scope '{scope}' is not authorized. Current scopes: {sorted(_scopes())}"
        )


def _safe_path(relative_path: str, *, must_exist: bool = False) -> Path:
    if not relative_path or relative_path in {".", "./"}:
        raise ValueError("A repository-relative file path is required.")
    candidate = (_root() / relative_path).resolve()
    root = _root()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError("Path escapes TRACEWEAVE_ROOT.") from exc
    if candidate == root / ".git" or (root / ".git") in candidate.parents:
        raise ValueError("Access to .git internals is forbidden.")
    if must_exist and not candidate.exists():
        raise FileNotFoundError(relative_path)
    return candidate


def _relative(path: Path) -> str:
    return path.resolve().relative_to(_root()).as_posix()


def _run_git(args: Iterable[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(_root()), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit={result.returncode}"
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return result


def _reject_option(value: str, name: str) -> str:
    """Refuse a caller-supplied value that git would parse as an option.

    Without this, a value such as ``--output=<file>`` or ``--open-files-in-pager=<cmd>``
    turns a read-only tool into a file write or a command execution.
    """
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} is required.")
    if value.lstrip().startswith("-"):
        raise ValueError(f"{name} must not start with '-': {value!r}")
    return value


def _allowed_remote(remote: str) -> str:
    """Accept only a configured remote name whose URL points at the allowed repository."""
    _reject_option(remote, "remote")
    configured = _run_git(["remote"]).stdout.split()
    if remote not in configured:
        raise ValueError(f"Unknown remote {remote!r}. Configured remotes: {configured}")
    allowed = os.environ.get("TRACEWEAVE_ALLOWED_REMOTE", "").strip().lower()
    if allowed:
        url = _run_git(["remote", "get-url", remote]).stdout.strip().lower()
        normalized = url.removesuffix(".git").rstrip("/")
        if not (normalized.endswith("/" + allowed) or normalized.endswith(":" + allowed)):
            raise PermissionError(
                f"Remote {remote!r} points to {url!r}, not to the allowed repository {allowed!r}."
            )
    return remote


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _assert_expected(path: Path, expected_sha256: str | None) -> None:
    if not expected_sha256:
        return
    if not path.exists():
        raise FileNotFoundError(
            f"Expected existing file with sha256={expected_sha256}, but {_relative(path)} does not exist."
        )
    actual = _sha256_file(path)
    if actual.lower() != expected_sha256.lower():
        raise RuntimeError(
            f"Optimistic write rejected for {_relative(path)}: expected sha256={expected_sha256}, actual={actual}"
        )


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.traceweave.tmp")
    temp.write_text(content, encoding="utf-8", newline="\n")
    os.replace(temp, path)


@mcp.resource("traceweave://status", mime_type="application/json")
def traceweave_status_resource() -> dict:
    """Current repository identity and authorized MCP capabilities."""
    _require("read")
    return traceweave_status()


@mcp.tool()
def traceweave_status() -> dict:
    """Return repository HEAD, branch, worktree status and authorized scopes."""
    _require("read")
    branch = _run_git(["branch", "--show-current"]).stdout.strip()
    head = _run_git(["rev-parse", "HEAD"]).stdout.strip()
    porcelain = _run_git(["status", "--porcelain=v1"]).stdout.splitlines()
    return {
        "root": str(_root()),
        "branch": branch,
        "head": head,
        "dirty": bool(porcelain),
        "changes": porcelain,
        "scopes": sorted(_scopes()),
    }


@mcp.tool()
def traceweave_read_text(path: str, max_chars: int = 200_000) -> dict:
    """Read one UTF-8 repository file without modifying it."""
    _require("read")
    file_path = _safe_path(path, must_exist=True)
    if not file_path.is_file():
        raise ValueError(f"Not a file: {path}")
    data = file_path.read_bytes()
    text = data.decode("utf-8")
    truncated = len(text) > max_chars
    return {
        "path": _relative(file_path),
        "sha256": _sha256_bytes(data),
        "bytes": len(data),
        "truncated": truncated,
        "content": text[:max_chars],
    }


@mcp.tool()
def traceweave_list(path: str = ".", max_entries: int = 500) -> dict:
    """List files/directories under a repository-relative directory."""
    _require("read")
    base = _root() if path in {".", "./", ""} else _safe_path(path, must_exist=True)
    if not base.is_dir():
        raise ValueError(f"Not a directory: {path}")
    entries = []
    for item in sorted(base.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
        if item.name == ".git":
            continue
        entries.append({
            "path": _relative(item),
            "type": "directory" if item.is_dir() else "file",
            "bytes": item.stat().st_size if item.is_file() else None,
        })
        if len(entries) >= max_entries:
            break
    return {"path": "." if base == _root() else _relative(base), "entries": entries}


@mcp.tool()
def traceweave_search_text(query: str, glob: str = "*.md", max_results: int = 50) -> dict:
    """Search tracked repository text with git grep."""
    _require("read")
    if not query:
        raise ValueError("query is required")
    # `-e` binds the query as the pattern, so a query starting with '-' is searched, not parsed.
    args = ["grep", "-n", "-I", "--no-color", "-F", "-e", query, "--"]
    if glob:
        args.append(glob)
    result = _run_git(args, check=False)
    if result.returncode not in (0, 1):
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"git grep failed: {detail}")
    all_lines = result.stdout.splitlines()
    lines = all_lines[:max_results]
    return {
        "query": query,
        "glob": glob,
        "count": len(lines),
        "results": lines,
        "truncated": len(all_lines) > max_results,
    }


@mcp.tool()
def traceweave_sha256(path: str) -> dict:
    """Calculate SHA-256 for one repository file."""
    _require("read")
    file_path = _safe_path(path, must_exist=True)
    if not file_path.is_file():
        raise ValueError(f"Not a file: {path}")
    return {"path": _relative(file_path), "sha256": _sha256_file(file_path), "bytes": file_path.stat().st_size}


@mcp.tool()
def traceweave_git_readback(ref: str, path: str) -> dict:
    """Read a file exactly as stored in a Git ref and return its blob id and SHA-256."""
    _require("read")
    _reject_option(ref, "ref")
    file_path = _safe_path(path)
    relative = _relative(file_path)
    blob = _run_git(["rev-parse", "--verify", "--end-of-options", f"{ref}:{relative}"]).stdout.strip()
    data = subprocess.run(
        ["git", "-C", str(_root()), "show", f"{ref}:{relative}"],
        capture_output=True,
        check=False,
    )
    if data.returncode != 0:
        raise RuntimeError(data.stderr.decode("utf-8", errors="replace").strip())
    return {
        "ref": ref,
        "path": relative,
        "blob": blob,
        "sha256": _sha256_bytes(data.stdout),
        "bytes": len(data.stdout),
        "content": data.stdout.decode("utf-8"),
    }


@mcp.tool()
def traceweave_write_text(path: str, content: str, expected_sha256: str | None = None) -> dict:
    """Create or replace one UTF-8 file. Optional expected_sha256 prevents stale overwrites."""
    _require("write")
    file_path = _safe_path(path)
    _assert_expected(file_path, expected_sha256)
    before = _sha256_file(file_path) if file_path.exists() and file_path.is_file() else None
    _atomic_write(file_path, content)
    return {
        "path": _relative(file_path),
        "before_sha256": before,
        "sha256": _sha256_file(file_path),
        "bytes": file_path.stat().st_size,
    }


@mcp.tool()
def traceweave_append_text(path: str, content: str, expected_sha256: str | None = None) -> dict:
    """Append UTF-8 text to a repository file."""
    _require("write")
    file_path = _safe_path(path)
    _assert_expected(file_path, expected_sha256)
    before = file_path.read_bytes() if file_path.exists() else b""
    addition = content.encode("utf-8")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("ab") as handle:
        handle.write(addition)
    return {
        "path": _relative(file_path),
        "before_sha256": _sha256_bytes(before) if before else None,
        "sha256": _sha256_file(file_path),
        "appended_bytes": len(addition),
        "bytes": file_path.stat().st_size,
    }


@mcp.tool()
def traceweave_git_commit(paths: list[str], message: str) -> dict:
    """Stage only explicit paths and create one commit. Never stages the whole repository."""
    _require("publish")
    if not paths:
        raise ValueError("At least one explicit path is required.")
    if not message.strip():
        raise ValueError("Commit message is required.")
    safe_paths = [_relative(_safe_path(path)) for path in paths]
    pre_staged = _run_git(["diff", "--cached", "--name-only"]).stdout.splitlines()
    if pre_staged:
        raise RuntimeError(
            f"Refusing to commit while another execution has staged paths: {pre_staged}"
        )
    _run_git(["add", "--", *safe_paths])
    staged = _run_git(["diff", "--cached", "--name-only"]).stdout.splitlines()
    unexpected = sorted(set(staged) - set(safe_paths))
    if unexpected:
        raise RuntimeError(f"Unexpected paths are staged: {unexpected}")
    if not staged:
        raise RuntimeError("No staged changes to commit.")
    # No `git diff --cached --check`: it refuses trailing whitespace, which in transcripts and
    # quoted human speech is literal content that must be preserved byte for byte.
    _run_git(["commit", "-m", message])
    head = _run_git(["rev-parse", "HEAD"]).stdout.strip()
    return {"commit": head, "paths": staged, "message": message}


@mcp.tool()
def traceweave_git_push(remote: str = "origin", branch: str | None = None) -> dict:
    """Push the current branch without force. Requires publish scope."""
    _require("publish")
    _allowed_remote(remote)
    current = _run_git(["branch", "--show-current"]).stdout.strip()
    target = branch or current
    if not current:
        raise RuntimeError("Detached HEAD is not publishable.")
    _reject_option(target, "branch")
    if target != current:
        raise RuntimeError(f"Refusing to push a different branch: current={current}, requested={target}")
    _run_git(["push", remote, f"HEAD:{target}"])
    local = _run_git(["rev-parse", "HEAD"]).stdout.strip()
    remote_head = _run_git(["ls-remote", "--heads", remote, target]).stdout.strip().split()
    observed = remote_head[0] if remote_head else None
    return {
        "remote": remote,
        "branch": target,
        "local_head": local,
        "remote_head": observed,
        "readback_match": observed == local,
    }


def main(argv: list[str] | None = None) -> int:
    """Run Traceweave MCP over stdio (default) or Streamable HTTP."""
    parser = argparse.ArgumentParser(prog="traceweave-mcp")
    parser.add_argument("--transport", choices=("stdio", "streamable-http"), default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args(argv)

    if args.transport == "stdio":
        mcp.run()
    else:
        mcp.run(
            transport="streamable-http",
            host=args.host,
            port=args.port,
            json_response=True,
            stateless_http=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
