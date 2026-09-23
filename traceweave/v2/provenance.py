"""Custody and paired-publication provenance for Traceweave Protocol V2.

Logical IDs correlate two destination projections of the same causal update.
They are not publication receipts. Materialization requires native destination
identity plus content identity and confirmed readback.

A custody mirror is a different object: it preserves the same source bytes in
an independently controlled location. Custody does not prove publication, and
publication does not prove independent custody.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import unicodedata
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

SAO_PAULO = ZoneInfo("America/Sao_Paulo")


def sanitize_slug(raw: str) -> str:
    text = unicodedata.normalize("NFD", str(raw or ""))
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn").lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")[:40]
    if not text:
        raise ValueError("empty slug after sanitization")
    return text


def generate_pair(slug: str, *, now: datetime | None = None, namespace: str = "PROV") -> dict[str, str]:
    instant = now.astimezone(SAO_PAULO) if now is not None else datetime.now(SAO_PAULO)
    key = f"{instant:%Y%m%d-%H%M%S}-{sanitize_slug(slug)}"
    return {
        "pair_key": key,
        "notion_id": f"{namespace}-NOTION-{key}",
        "github_id": f"{namespace}-GITHUB-{key}",
        "generated_at_timezone": "America/Sao_Paulo",
    }


def record_materialization(
    publication: dict[str, Any],
    *,
    destination: str,
    native_ids: dict[str, str],
    public_sha256: str,
    readback_confirmed: bool,
    reference: str | None = None,
    downloadable_artifact: dict[str, Any] | None = None,
) -> dict[str, Any]:
    destination = destination.lower()
    if destination not in {"github", "notion"}:
        raise ValueError("destination must be github or notion")
    if not native_ids or not all(isinstance(v, str) and v for v in native_ids.values()):
        raise ValueError("at least one non-empty native destination ID is required")
    if len(public_sha256) != 64:
        raise ValueError("public_sha256 must be a 64-character SHA-256 hex digest")

    materialization = {
        "native_ids": dict(sorted(native_ids.items())),
        "public_sha256": public_sha256.lower(),
        "reference": reference,
        "readback_confirmed": bool(readback_confirmed),
    }
    if downloadable_artifact is not None:
        required = {"filename", "byte_length", "sha256", "download_reference"}
        if not required.issubset(downloadable_artifact):
            raise ValueError("downloadable_artifact requires filename, byte_length, sha256, and download_reference")
        artifact_sha = downloadable_artifact["sha256"]
        if not isinstance(artifact_sha, str) or artifact_sha.lower() != public_sha256.lower():
            raise ValueError("downloadable_artifact sha256 must match public_sha256")
        if not isinstance(downloadable_artifact["byte_length"], int) or downloadable_artifact["byte_length"] < 0:
            raise ValueError("downloadable_artifact byte_length must be a non-negative integer")
        if not downloadable_artifact["filename"] or not downloadable_artifact["download_reference"]:
            raise ValueError("downloadable_artifact filename and download_reference must be non-empty")
        descriptor = dict(downloadable_artifact)
        descriptor["sha256"] = artifact_sha.lower()
        materialization["downloadable_artifact"] = descriptor
    publication.setdefault("materializations", {})[destination] = materialization
    return materialization


def dual_materialized(publication: dict[str, Any]) -> bool:
    mats = publication.get("materializations")
    if not isinstance(mats, dict):
        return False
    for destination in ("github", "notion"):
        item = mats.get(destination)
        if not isinstance(item, dict):
            return False
        if not item.get("readback_confirmed"):
            return False
        native_ids = item.get("native_ids")
        if not isinstance(native_ids, dict) or not native_ids:
            return False
        if not item.get("public_sha256"):
            return False
        if publication.get("artifact_kind") == "source":
            artifact = item.get("downloadable_artifact")
            if not isinstance(artifact, dict):
                return False
            if artifact.get("sha256") != item.get("public_sha256"):
                return False
            if not artifact.get("filename") or not artifact.get("download_reference"):
                return False
            if not isinstance(artifact.get("byte_length"), int) or artifact["byte_length"] < 0:
                return False
    return True


def compare_bytes(source: bytes, replica: bytes) -> dict[str, Any]:
    """Compare exact bytes, including line endings and trailing bytes."""
    if not isinstance(source, bytes) or not isinstance(replica, bytes):
        raise TypeError("source and replica must be bytes")
    source_sha = hashlib.sha256(source).hexdigest()
    replica_sha = hashlib.sha256(replica).hexdigest()
    return {
        "same_bytes": source == replica,
        "source_sha256": source_sha,
        "replica_sha256": replica_sha,
        "source_bytes": len(source),
        "replica_bytes": len(replica),
    }


def record_custody_mirror(
    *,
    source_artifact: str,
    replica_artifact: str,
    source: bytes,
    replica: bytes,
    native_ids: dict[str, str],
    readback_confirmed: bool,
    overwrite_protected: bool,
) -> dict[str, Any]:
    """Record an independently located byte-preserving custody copy."""
    if not source_artifact or not replica_artifact:
        raise ValueError("source_artifact and replica_artifact are required")
    if not native_ids or not all(isinstance(v, str) and v for v in native_ids.values()):
        raise ValueError("custody mirror requires non-empty native_ids")
    comparison = compare_bytes(source, replica)
    return {
        "source_artifact": source_artifact,
        "source_sha256": comparison["source_sha256"],
        "source_bytes": comparison["source_bytes"],
        "replica_artifact": replica_artifact,
        "replica_sha256": comparison["replica_sha256"],
        "replica_bytes": comparison["replica_bytes"],
        "native_ids": dict(sorted(native_ids.items())),
        "readback_confirmed": bool(readback_confirmed),
        "overwrite_protected": bool(overwrite_protected),
    }


def custody_mirrored(record: dict[str, Any]) -> bool:
    """Return true only for an exact, read-back, independently identified copy."""
    return bool(
        isinstance(record, dict)
        and record.get("source_sha256") == record.get("replica_sha256")
        and record.get("source_bytes") == record.get("replica_bytes")
        and record.get("readback_confirmed") is True
        and record.get("overwrite_protected") is True
        and isinstance(record.get("native_ids"), dict)
        and record["native_ids"]
    )


def _cli() -> int:
    parser = argparse.ArgumentParser(description="Generate a Traceweave V2 causal publication pair")
    parser.add_argument("slug")
    parser.add_argument("--namespace", default="PROV")
    args = parser.parse_args()
    pair = generate_pair(args.slug, namespace=args.namespace)
    print(f"NOTION_ID={pair['notion_id']}")
    print(f"GITHUB_ID={pair['github_id']}")
    print(f"PAIR_KEY={pair['pair_key']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
