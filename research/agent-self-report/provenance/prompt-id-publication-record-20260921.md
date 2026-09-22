# Publication record — prompt-ID provenance package — 2026-09-21

STATUS: GITHUB_PUBLICATION_CORRECTED
AUTHORITY: Glaydson
SOURCE_PACKAGE: `TRACEWEAVE_PREPUBLICATION_PROMPT_ID_PROVENANCE_20260921 (1).zip`
SOURCE_PACKAGE_SHA256: `f2bbea1aa127b79de967cd2ddb4995d3510be9dda10d04f2dd0b447be89b92e6`

## Correlation identity

```text
NOTION_ID=PROV-NOTION-20260921-205545-publish-prompt-id-provenance-package
GITHUB_ID=PROV-GITHUB-20260921-205545-publish-prompt-id-provenance-package
PAIR_KEY=20260921-205545-publish-prompt-id-provenance-package
```

The public correlation namespace is neutral (`PROV-*`).

## Package verification

The uploaded revised package contains 13 entries. Its internal `MANIFEST.json` was checked against the extracted files: every listed byte count and SHA-256 matched.

The earlier duplicate package and the revised package differ only in `manifest/SOURCE_HASHES.md` and the corresponding manifest/hash records. The revised package removed an obsolete note about an older `generate-update-ids.js` hash.

A targeted secret-pattern scan found no GitHub token, OpenAI key, Anthropic key, Supabase personal token, JWT, AWS access key, or private-key header in the package. This is a screening result, not a proof that no sensitive information exists.

## Public material retained

The current public tree retains:

- prompt-ID provenance gap case;
- selected evidence excerpt;
- downstream commit-chain corroboration;
- execution-visibility / dual-publication method;
- source hashes;
- both historical generator source artifacts under abstract evidence filenames;
- neutral Traceweave publication generator;
- publication record, correction and readback receipt.

## Correction to the first materialization

Commit `07ab19614006a9c75432ae6a227546b494843e1a` exposed two historical generators under active-looking `source-tools/` names.

Those paths were removed. The exact same source bytes are now published under:

```text
research/agent-self-report/source-artifacts/identity-chain-generator.js
research/agent-self-report/source-artifacts/paired-publication-id-generator.js
```

Their original hashes and historical identifiers remain unchanged. The path correction prevents the system-specific source artifacts from looking like Traceweave's active tooling while preserving the evidence itself.

See:

`research/agent-self-report/provenance/prompt-id-publication-correction-20260921.md`

## Relationship to the Codex lifecycle record

`research/agent-self-report/provenance/codex-session-lifecycle-20260921.md` records a later Codex session where prompt-ID generation was preserved observably before mutation and where a deterministic STOP path reached transcript → report → handoff → commit → push → remote readback.

That later execution is not used to retroactively prove the missing generator event in the earlier Claude Markdown surface. It demonstrates the corrected evidence discipline.

## Destination state

```text
GitHub: corrected public tree; historical source bytes restored under abstract evidence names.
Notion: PENDING — not modified.
```

A later Notion materialization, if authorized, must reuse the same `NOTION_ID`, `GITHUB_ID`, and `PAIR_KEY`.
