#!/usr/bin/env python3
"""Verify an authorized private E2E bundle against the public custody index.

This program prints hashes and counts only. It never prints artifact contents.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path


ANCHOR_PATHS = {
    "run_descriptor": "RUN_DESCRIPTOR.json",
    "manifest": "MANIFEST.json",
    "checksum_list": "SHA256SUMS",
    "saved_console": "evidence/console/TESTE_E2E_console_salvo_por_glaydson.md",
    "final_ui_screenshot": "evidence/screenshots-glaydson/Imagem_do_ChatGPT_14_de_out._de_2026_18_07_34.png",
    "research_console_screenshot": "evidence/screenshots-glaydson/Imagem_do_ChatGPT_14_de_out._de_2026_18_07_43.png",
}
CHECKSUM_LINE = re.compile(r"^([0-9a-f]{64}) \*\./(.+)$")


def safe_file(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError(f"missing or out-of-bundle artifact: {relative}")
    return path


def fingerprint(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def check(root: Path, relative: str, expected: dict) -> None:
    actual_hash, actual_size = fingerprint(safe_file(root, relative))
    if actual_hash != expected["sha256"] or actual_size != expected["bytes"]:
        raise ValueError(f"hash or byte count mismatch: {relative}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", required=True, type=Path)
    parser.add_argument("--index", type=Path, default=Path(__file__).with_name("public-evidence-index.json"))
    args = parser.parse_args()
    root = args.bundle.resolve(strict=True)
    index = json.loads(args.index.read_text(encoding="utf-8"))
    if index.get("schema") != "traceweave.worion-e2e.public-index.v1":
        parser.error("unsupported index schema")

    for role, relative in ANCHOR_PATHS.items():
        check(root, relative, index["anchors"][role])
    if index["anchors"]["run_descriptor"]["sha256"] != index["run_sha256"]:
        raise ValueError("run identity differs from descriptor hash")

    artifact_count = 0
    for turn in index["turns"]:
        for role, expected in turn["artifacts"].items():
            check(root, f"evidence/turns/{turn['label']}/{role}", expected)
            artifact_count += 1

    lines = safe_file(root, "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    if len(lines) != index["private_bundle_file_count"]:
        raise ValueError("checksum list length differs from the public index")
    for line in lines:
        match = CHECKSUM_LINE.fullmatch(line)
        if not match:
            raise ValueError("malformed SHA256SUMS entry")
        expected_hash, relative = match.groups()
        actual_hash, _ = fingerprint(safe_file(root, relative))
        if actual_hash != expected_hash:
            raise ValueError(f"SHA256SUMS mismatch: {relative}")

    print(json.dumps({
        "status": "VERIFIED",
        "run_sha256": index["run_sha256"],
        "turns": len(index["turns"]),
        "indexed_turn_artifacts": artifact_count,
        "bundle_files_checked": len(lines),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
