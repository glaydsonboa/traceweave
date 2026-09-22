"""Paired causal provenance for Traceweave Protocol V2.

Logical IDs correlate two destination projections of the same causal update.
They are not publication receipts. Materialization requires native destination
identity plus content identity and confirmed readback.
"""

from __future__ import annotations

import argparse
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
    return True


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
