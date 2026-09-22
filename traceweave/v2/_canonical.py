"""Canonical JSON helpers used by Traceweave V2."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize JSON deterministically for hashing.

    UTF-8, sorted keys, compact separators, and no ASCII escaping are used so
    the same semantic object produces the same digest across runs.
    """

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()
