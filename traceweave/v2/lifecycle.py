"""Lifecycle primitives for Traceweave Protocol V2.

The lifecycle is evidence-first rather than conversational:

    START -> EXECUTION -> RESUME* -> STOP

Each event is hash-linked to the previous event. A RESUME may point to any
previous event in the same chain as its explicit recovery anchor. STOP closes
one observable boundary and may carry the source-artifact identity that later
feeds paired publication provenance.
"""

from __future__ import annotations

import argparse
import json
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import PROTOCOL_VERSION, SCHEMA_ID
from ._canonical import sha256_json


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _new_id(prefix: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{prefix}-{stamp}-{secrets.token_hex(3)}"


def new_chain(authority: str, chain_id: str | None = None, created_at: str | None = None) -> dict[str, Any]:
    if not authority or not authority.strip():
        raise ValueError("authority is required")
    return {
        "schema": SCHEMA_ID,
        "protocol_version": PROTOCOL_VERSION,
        "chain_id": chain_id or _new_id("chain"),
        "authority": authority.strip(),
        "created_at": created_at or utc_now(),
        "events": [],
        "publications": [],
        "status": "open",
    }


def _event_payload(
    chain: dict[str, Any],
    event_type: str,
    *,
    session_id: str,
    repository: str,
    branch: str,
    head_commit: str,
    observed_at: str | None = None,
    resume_from_event_sha256: str | None = None,
    source_artifact: str | None = None,
    source_sha256: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if event_type not in {"START", "RESUME", "STOP"}:
        raise ValueError(f"unsupported lifecycle event: {event_type}")
    if not all([session_id, repository, branch, head_commit]):
        raise ValueError("session_id, repository, branch, and head_commit are required")

    events = chain.get("events")
    if not isinstance(events, list):
        raise ValueError("chain.events must be a list")
    prev = events[-1].get("event_sha256") if events else None

    event: dict[str, Any] = {
        "event_id": _new_id(event_type.lower()),
        "event_type": event_type,
        "observed_at": observed_at or utc_now(),
        "session_id": session_id,
        "repository": repository,
        "branch": branch,
        "head_commit": head_commit,
        "prev_event_sha256": prev,
        "resume_from_event_sha256": resume_from_event_sha256,
        "source_artifact": source_artifact,
        "source_sha256": source_sha256,
        "metadata": metadata or {},
    }
    event["event_sha256"] = sha256_json(event)
    return event


def _append(chain: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    events = chain.setdefault("events", [])
    if not events and event["event_type"] != "START":
        raise ValueError("the first lifecycle event must be START")
    if events and event["event_type"] == "START":
        raise ValueError("START can only be the first lifecycle event")
    events.append(event)
    chain["status"] = "closed" if event["event_type"] == "STOP" else "open"
    return event


def start(
    chain: dict[str, Any],
    *,
    session_id: str,
    repository: str,
    branch: str,
    head_commit: str,
    observed_at: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    event = _event_payload(
        chain,
        "START",
        session_id=session_id,
        repository=repository,
        branch=branch,
        head_commit=head_commit,
        observed_at=observed_at,
        metadata=metadata,
    )
    return _append(chain, event)


def resume(
    chain: dict[str, Any],
    *,
    session_id: str,
    repository: str,
    branch: str,
    head_commit: str,
    resume_from_event_sha256: str,
    observed_at: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    known = {e.get("event_sha256") for e in chain.get("events", []) if isinstance(e, dict)}
    if resume_from_event_sha256 not in known:
        raise ValueError("resume_from_event_sha256 does not identify an earlier event in this chain")
    event = _event_payload(
        chain,
        "RESUME",
        session_id=session_id,
        repository=repository,
        branch=branch,
        head_commit=head_commit,
        observed_at=observed_at,
        resume_from_event_sha256=resume_from_event_sha256,
        metadata=metadata,
    )
    return _append(chain, event)


def stop(
    chain: dict[str, Any],
    *,
    session_id: str,
    repository: str,
    branch: str,
    head_commit: str,
    source_artifact: str,
    source_sha256: str,
    observed_at: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if len(source_sha256) != 64:
        raise ValueError("source_sha256 must be a 64-character SHA-256 hex digest")
    event = _event_payload(
        chain,
        "STOP",
        session_id=session_id,
        repository=repository,
        branch=branch,
        head_commit=head_commit,
        observed_at=observed_at,
        source_artifact=source_artifact,
        source_sha256=source_sha256.lower(),
        metadata=metadata,
    )
    return _append(chain, event)


def write_chain(chain: dict[str, Any], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(chain, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target


def read_chain(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("chain JSON must be an object")
    return data


def _cli() -> int:
    parser = argparse.ArgumentParser(description="Build a local Traceweave V2 lifecycle chain")
    sub = parser.add_subparsers(dest="command", required=True)

    p_start = sub.add_parser("start")
    p_start.add_argument("chain_file", type=Path)
    p_start.add_argument("--authority", required=True)
    p_start.add_argument("--session-id", required=True)
    p_start.add_argument("--repository", required=True)
    p_start.add_argument("--branch", required=True)
    p_start.add_argument("--head", required=True)

    p_resume = sub.add_parser("resume")
    p_resume.add_argument("chain_file", type=Path)
    p_resume.add_argument("--session-id", required=True)
    p_resume.add_argument("--repository", required=True)
    p_resume.add_argument("--branch", required=True)
    p_resume.add_argument("--head", required=True)
    p_resume.add_argument("--from-event", required=True)

    p_stop = sub.add_parser("stop")
    p_stop.add_argument("chain_file", type=Path)
    p_stop.add_argument("--session-id", required=True)
    p_stop.add_argument("--repository", required=True)
    p_stop.add_argument("--branch", required=True)
    p_stop.add_argument("--head", required=True)
    p_stop.add_argument("--source-artifact", required=True)
    p_stop.add_argument("--source-sha256", required=True)

    args = parser.parse_args()
    if args.command == "start":
        chain = new_chain(args.authority)
        event = start(
            chain,
            session_id=args.session_id,
            repository=args.repository,
            branch=args.branch,
            head_commit=args.head,
        )
    else:
        chain = read_chain(args.chain_file)
        if args.command == "resume":
            event = resume(
                chain,
                session_id=args.session_id,
                repository=args.repository,
                branch=args.branch,
                head_commit=args.head,
                resume_from_event_sha256=args.from_event,
            )
        else:
            event = stop(
                chain,
                session_id=args.session_id,
                repository=args.repository,
                branch=args.branch,
                head_commit=args.head,
                source_artifact=args.source_artifact,
                source_sha256=args.source_sha256,
            )
    write_chain(chain, args.chain_file)
    print(event["event_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
