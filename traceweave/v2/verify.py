"""Structural and causal verification for Traceweave Protocol V2."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from . import SCHEMA_ID
from ._canonical import sha256_json


@dataclass
class VerificationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def verify_chain(chain: dict[str, Any]) -> VerificationResult:
    result = VerificationResult()
    if not isinstance(chain, dict):
        result.errors.append("chain must be a JSON object")
        return result

    if chain.get("schema") != SCHEMA_ID:
        result.errors.append(f"schema must be {SCHEMA_ID!r}")
    if not chain.get("chain_id"):
        result.errors.append("chain_id is required")
    if not chain.get("authority"):
        result.errors.append("authority is required")

    events = chain.get("events")
    if not isinstance(events, list) or not events:
        result.errors.append("events must contain at least one lifecycle event")
        return result
    if not isinstance(events[0], dict) or events[0].get("event_type") != "START":
        result.errors.append("the first event must be START")

    previous_hash: str | None = None
    known_hashes: set[str] = set()
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            result.errors.append(f"events[{index}] must be an object")
            continue
        claimed = event.get("event_sha256")
        unhashed = dict(event)
        unhashed.pop("event_sha256", None)
        actual = sha256_json(unhashed)
        if claimed != actual:
            result.errors.append(f"events[{index}].event_sha256 does not match canonical event content")
        if event.get("prev_event_sha256") != previous_hash:
            result.errors.append(f"events[{index}].prev_event_sha256 breaks the hash chain")

        if event.get("event_type") == "RESUME":
            anchor = event.get("resume_from_event_sha256")
            if not anchor or anchor not in known_hashes:
                result.errors.append(f"events[{index}] RESUME does not point to an earlier event")
        if event.get("event_type") == "STOP":
            source_sha = event.get("source_sha256")
            if not isinstance(source_sha, str) or len(source_sha) != 64:
                result.errors.append(f"events[{index}] STOP requires source_sha256")
            if not event.get("source_artifact"):
                result.errors.append(f"events[{index}] STOP requires source_artifact")

        if isinstance(claimed, str):
            known_hashes.add(claimed)
            previous_hash = claimed

    closed = chain.get("status") == "closed"
    if closed and events[-1].get("event_type") != "STOP":
        result.errors.append("a closed chain must end with STOP")
    if not closed and events[-1].get("event_type") == "STOP":
        result.errors.append("a chain ending in STOP must have status=closed")

    publications = chain.get("publications", [])
    if not isinstance(publications, list):
        result.errors.append("publications must be a list")
        return result

    for index, pub in enumerate(publications):
        if not isinstance(pub, dict):
            result.errors.append(f"publications[{index}] must be an object")
            continue
        key = pub.get("pair_key")
        gid = pub.get("github_id")
        nid = pub.get("notion_id")
        if not key or not gid or not nid:
            result.errors.append(f"publications[{index}] requires pair_key, github_id, and notion_id")
        else:
            if not str(gid).endswith(str(key)):
                result.errors.append(f"publications[{index}].github_id does not share pair_key")
            if not str(nid).endswith(str(key)):
                result.errors.append(f"publications[{index}].notion_id does not share pair_key")

        source_sha = pub.get("source_sha256")
        public_sha = pub.get("public_sha256")
        transformed = pub.get("transformed")
        if not isinstance(source_sha, str) or len(source_sha) != 64:
            result.errors.append(f"publications[{index}].source_sha256 is invalid")
        if not isinstance(public_sha, str) or len(public_sha) != 64:
            result.errors.append(f"publications[{index}].public_sha256 is invalid")
        if transformed is False and source_sha and public_sha and source_sha != public_sha:
            result.errors.append(f"publications[{index}] says transformed=false but hashes differ")
        if transformed is True and source_sha == public_sha:
            result.warnings.append(f"publications[{index}] says transformed=true but hashes are equal")

        mats = pub.get("materializations", {})
        if not isinstance(mats, dict):
            result.errors.append(f"publications[{index}].materializations must be an object")
            continue
        for destination in ("github", "notion"):
            mat = mats.get(destination)
            if mat is None:
                continue
            if not isinstance(mat, dict):
                result.errors.append(f"publications[{index}].materializations.{destination} must be an object")
                continue
            native = mat.get("native_ids")
            if not isinstance(native, dict) or not native:
                result.errors.append(f"publications[{index}] {destination} materialization lacks native_ids")
            if mat.get("public_sha256") != public_sha:
                result.errors.append(f"publications[{index}] {destination} materialization hash differs from public_sha256")
            if mat.get("readback_confirmed") is not True:
                result.warnings.append(f"publications[{index}] {destination} is not readback-confirmed")

    return result
