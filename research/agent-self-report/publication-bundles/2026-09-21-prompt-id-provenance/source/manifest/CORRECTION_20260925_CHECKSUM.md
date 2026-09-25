# Correction — one checksum in this manifest is wrong (25/09/2026)

This note is added forward-only. `SHA256SUMS.txt`, `MANIFEST.json` and `SOURCE_HASHES.md` are **not**
rewritten, so that the error stays visible.

## What is wrong

| file | hash in `SHA256SUMS.txt` | hash of the published bytes |
|---|---|---|
| `case/CORROBORATION_COMMIT_CHAIN_cb7bfd6a.md` | `a36e948ccf9cc9b0…` | `a5d289da…` (recompute below) |

Nine other listed files were re-verified here and match their published bytes. The two scripts
(`scripts/generate-prompt-id.js`, `scripts/generate-update-ids.js`) are published under a different path, mapped
in `DUAL_PUBLICATION_MANIFEST.json`, and were not re-verified by this note.

## What was measured

- The file has had exactly one version since it was published (commit `45a3ab8`, 21/09/2026). It was not
  altered afterwards.
- The manifest hash does not match the published bytes, nor the same text with CRLF line endings, without a
  final newline, or with a UTF-8 BOM. The manifest was therefore wrong from the start, not made stale by a
  later edit.
- The divergence was reported by an external review on 24/09/2026 and reproduced independently on
  25/09/2026 from the Git blobs, which avoids checkout line-ending changes.

## Verify it yourself

```bash
git show HEAD:research/agent-self-report/publication-bundles/2026-09-21-prompt-id-provenance/source/case/CORROBORATION_COMMIT_CHAIN_cb7bfd6a.md | sha256sum
```

## Limit

This note does not explain which bytes produced `a36e948c…`. It records that the published file and the
manifest disagree, and which one is the published content.
