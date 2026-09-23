# Proven Governance — Pair Closure

## Causal identity

- `PAIR_KEY`: `20260923-153843-governanca-comprovada-arquivos-genericos`
- `GITHUB_ID`: `PROV-GITHUB-20260923-153843-governanca-comprovada-arquivos-genericos`
- `NOTION_ID`: `PROV-NOTION-20260923-153843-governanca-comprovada-arquivos-genericos`
- IDs were generated before the first external materialization of this causal update.

## Forward-only genealogy

The prior public package commit remains unchanged:

- prior GitHub-only package: `9e3d42a6da46c7742eb2dd048e4ed4e5532c28c2`
- paired-materialization commit: `f532c7f26853d3bf3fe07776c9ab0417a3f1afd2`

The paired manifest intentionally remains a record of the `PARTIAL` state at first materialization. This closure records the later readback result instead of rewriting that earlier state.

## Provenance correction

- documents 01 and 02: governance artifacts supplied under `<user name>` authority, transformed into English/sanitized public derivatives by ChatGPT;
- document 03: **formulated by ChatGPT under `<user name>`'s authority and direction**, then generalized for public release;
- no historical ID was retroactively inserted into the earlier GitHub-only publication.

## Native destination identities

### GitHub

- repository: `glaydsonboa/traceweave`
- branch: `main`
- materialization commit: `f532c7f26853d3bf3fe07776c9ab0417a3f1afd2`
- remote readback: `CONFIRMED`

### Notion

- native page ID: `3b354a24-a0f0-8191-a0d2-d00c53d02780`
- page readback: `CONFIRMED`

Notion attachment identities:

- 01: `3e454a24-a0f0-8107-9845-00b2b0202bb3`
- 02: `3e454a24-a0f0-81c5-9216-00b2f6ba623a`
- 03: `3e454a24-a0f0-8135-b54d-00b2e9893639`
- manifest: `3e454a24-a0f0-818f-9f9f-00b2f53e5004`

## Byte readback

| Artifact | Git blob | Bytes GitHub | Bytes Notion | SHA-256 GitHub / Notion | Result |
|---|---|---:|---:|---|---|
| `01_DUAL_PROVENANCE_AND_HEADER_LAW.md` | `65934a9ca4979286296add0a8556efe7f9509566` | 5705 | 5705 | `a836bd24047271bd6d59c5be6710ddf7979b98315d32deaf0c1d6b8a1ea4f83a` | `SAME_BYTES` |
| `02_ADVERSARIAL_GOVERNANCE_AUDITOR.md` | `a5c994ada9c354add0e6f5562fc147b3b21459a0` | 11335 | 11335 | `53997228c13274f57683ac354cd1ae8ff2ca7fd81a0d3e617cfda59dd945990f` | `SAME_BYTES` |
| `03_DAILY_PROVENANCE_GOVERNOR.md` | `dd4c4aaf9af552972d16230c3fe5498f3d2e3ead` | 23173 | 23173 | `af153f6d1cf47b8f032699c9c39c8ff5ab78f6ca35e683ca8063b78489f8fb58` | `SAME_BYTES` |
| `04_PAIRED_PUBLICATION_MANIFEST.md` | `8fd38d00a452cc9315539daa5f73d5364da94ff9` | 3349 | 3349 | `21c23066db941a819e4b8fab4cdff8354bc1344c9257e9043f92362a72902af4` | `SAME_BYTES` |

No line-ending normalization or extra trailing bytes were observed in the attachment readback.

## Component verdicts

```text
PAIR_IDS_PRESENT: CONFIRMED
GITHUB_MATERIALIZATION: CONFIRMED
NOTION_MATERIALIZATION: CONFIRMED
PAIR_CONTENT_EQUAL: CONFIRMED — 4/4 artifacts
PAIR_METADATA_CONSISTENT: CONFIRMED
PAIR_CAUSAL_ORDER_PROVEN: CONFIRMED
PAIR_READBACK_INDEPENDENT: CONFIRMED
PAIR_STATUS: CONFIRMED
```

## Boundary

This closure proves the paired publication and the recorded provenance correction for this public governance package. It does not retroactively convert the earlier GitHub-only commit into a paired publication and does not claim runtime/effect proof beyond the publication operation itself.
