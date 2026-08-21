"""Checkpoint generation for Traceweave protocol version 0.1.

Builds a checkpoint JSON from read-only Git state, explicit provenance
names and a persisted session record. Provenance fields that are unknown are
represented as ``null`` — never invented, and never typed or chained by
inference from a plain name.

The CLI creates files only inside ``.traceweave/``.
"""

from __future__ import annotations

import json
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from . import TRACEWEAVE_VERSION
from .git_state import GitState


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_session_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"session-{stamp}-{secrets.token_hex(3)}"


def new_checkpoint_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"cp-{stamp}-{secrets.token_hex(3)}"


@dataclass
class CheckpointOptions:
    summary: str | None = None
    executor: str | None = None
    requested_by: str | None = None
    prompt_generator: str | None = None
    session_id: str | None = None
    base_commit: str | None = None
    graph_status: str = "unknown"
    graph_engine: str | None = None
    graph_source_commit: str | None = None
    graph_verified_at: str | None = None
    files_changed: list[str] = field(default_factory=list)


class SessionStore:
    """Persists the session record in ``.traceweave/session.json``."""

    def __init__(self, root: Path):
        self.root = root
        self.path = root / ".traceweave" / "session.json"

    def load(self) -> dict | None:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (FileNotFoundError, OSError, json.JSONDecodeError):
            return None
        return data if isinstance(data, dict) else None

    def save(self, session: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(session, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def get_or_create(self, opts: CheckpointOptions, git: GitState) -> dict:
        existing = self.load()
        if opts.session_id and (not existing or existing.get("session_id") != opts.session_id):
            session = {
                "session_id": opts.session_id,
                "started_at": utc_now(),
                "base_commit": opts.base_commit or git.head_commit,
            }
            self.save(session)
            return session
        if existing:
            return existing
        session = {
            "session_id": new_session_id(),
            "started_at": utc_now(),
            "base_commit": opts.base_commit or git.head_commit,
        }
        self.save(session)
        return session


def _provenance_link(name: str | None) -> dict | None:
    if name is None:
        return None
    # A plain name is kept as a fact. The type is explicit null — never inferred.
    return {"type": None, "name": name}


def build_checkpoint(opts: CheckpointOptions, git: GitState, session: dict) -> dict:
    requested_by = _provenance_link(opts.requested_by)
    prompt_generator = _provenance_link(opts.prompt_generator)
    executor = _provenance_link(opts.executor)

    head_commit = git.head_commit
    base_commit = opts.base_commit or session.get("base_commit") or head_commit
    files_changed = sorted(set(opts.files_changed or git.changed_files))

    if opts.graph_status == "synced":
        graph_sync = {
            "status": "synced",
            "engine": opts.graph_engine,
            "source_commit": opts.graph_source_commit or head_commit,
            "verified_at": opts.graph_verified_at or utc_now(),
        }
    elif opts.graph_status == "unknown":
        graph_sync = {"status": "unknown", "engine": opts.graph_engine,
                      "source_commit": None, "verified_at": None}
    else:
        graph_sync = {"status": "not_applicable", "engine": None,
                      "source_commit": None, "verified_at": None}

    checkpoint = {
        "traceweave_version": TRACEWEAVE_VERSION,
        "checkpoint_id": new_checkpoint_id(),
        "created_at": utc_now(),
        # The v0.1 CLI never ingests test evidence, so a generated checkpoint
        # must not claim a complete evidence boundary.
        "status": "partial",
        "session": {
            "session_id": session["session_id"],
            "started_at": session.get("started_at"),
            "executor": opts.executor,
            "repository": git.repository,
            "branch": git.branch,
            "base_commit": base_commit,
        },
        "provenance": {
            "requested_by": requested_by,
            "prompt_generator": prompt_generator,
            "executor": executor,
        },
        "work": {
            "summary": opts.summary,
            "files_changed": files_changed,
        },
        # No test was run for this checkpoint: one explicit entry with the
        # SPEC result value "not_run". Tests are never auto-discovered or run.
        "tests": [
            {"command": None, "result": "not_run", "evidence": None}
        ],
        "git": {
            "branch": git.branch,
            "base_commit": base_commit,
            "head_commit": head_commit,
            "commit_message": None,
            "working_tree": git.working_tree,
        },
        "graph_sync": graph_sync,
        "evidence": [
            {"type": "git_commit", "value": head_commit},
        ],
    }

    # Session branch is the base session branch; checkpoint git.branch is the
    # current branch at checkpoint time. Keep the session record consistent
    # with the latest checkpoint when they agree on session identity.
    session.setdefault("executor", opts.executor)

    return checkpoint


def write_checkpoint(checkpoint: dict, root: Path) -> Path:
    checkpoints_dir = root / ".traceweave" / "checkpoints"
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    out_path = checkpoints_dir / f"{checkpoint['checkpoint_id']}.json"
    out_path.write_text(
        json.dumps(checkpoint, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return out_path


def load_checkpoint(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
