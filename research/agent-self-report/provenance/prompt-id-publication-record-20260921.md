# Publication record — prompt-ID provenance package — 2026-09-21

STATUS: GITHUB_PUBLICATION_IN_PROGRESS
AUTHORITY: Glaydson
SOURCE_PACKAGE: `TRACEWEAVE_PREPUBLICATION_PROMPT_ID_PROVENANCE_20260921 (1).zip`
SOURCE_PACKAGE_SHA256: `f2bbea1aa127b79de967cd2ddb4995d3510be9dda10d04f2dd0b447be89b92e6`

## Correlation identity

```text
NOTION_ID=PROV-NOTION-20260921-205545-publish-prompt-id-provenance-package
GITHUB_ID=PROV-GITHUB-20260921-205545-publish-prompt-id-provenance-package
PAIR_KEY=20260921-205545-publish-prompt-id-provenance-package
```

The public correlation namespace is neutral (`PROV-*`). Source artifacts that contain `WORION-*` are preserved unchanged because they are evidence of the originating system, not Traceweave branding.

Generator used for this publication pair:

```text
tools/generate-publication-ids.js
SHA-256: 7737417ec46fc82bb7d1d233b260aa569bb84fb08f5774b249ec74c1a0cc5483
```

## Package verification

The uploaded revised package contains 13 entries. Its internal `MANIFEST.json` was checked against the extracted files: every listed byte count and SHA-256 matched.

The earlier duplicate package and the revised package differ only in `manifest/SOURCE_HASHES.md` and the corresponding manifest/hash records. The revised package removed an obsolete note about an older `generate-update-ids.js` hash. This publication uses the revised package.

A targeted secret-pattern scan found no GitHub token, OpenAI key, Anthropic key, Supabase personal token, JWT, AWS access key, or private-key header in the package. This is a screening result, not a proof that no sensitive information exists.

## Public material in this commit

The publication makes the following reviewable as plain text:

- prompt-ID provenance gap case;
- selected evidence excerpt;
- downstream commit-chain corroboration;
- execution-visibility / dual-publication method;
- exact source copy of `generate-prompt-id.js`;
- exact source copy of `generate-update-ids.js`;
- source hashes.

The source-specific generators are preserved byte-for-byte from the supplied package. Traceweave's public publication identity uses the neutral `PROV-*` namespace above.

## Relationship to the Codex lifecycle record

The prior public note:

`research/agent-self-report/provenance/codex-session-lifecycle-20260921.md`

records a later Codex session where prompt-ID generation was preserved observably before mutation and where a deterministic STOP path reached transcript → report → handoff → commit → push → remote readback.

That later execution is not used to retroactively prove the missing generator event in the earlier Claude Markdown surface. It demonstrates the corrected evidence discipline.

## Destination state

```text
GitHub: this commit materializes the package; native commit SHA is recorded by repository history and verified by readback.
Notion: PENDING — not modified by this commit.
```

A later Notion materialization, if authorized, must reuse the same `NOTION_ID`, `GITHUB_ID`, and `PAIR_KEY`; it must not regenerate the pair.
