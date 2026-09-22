# GitHub publication receipt — prompt-ID provenance package — 2026-09-21

STATUS: GITHUB_SYNCED_CORRECTED
AUTHORITY: Glaydson

## Correlation identity

```text
NOTION_ID=PROV-NOTION-20260921-205545-publish-prompt-id-provenance-package
GITHUB_ID=PROV-GITHUB-20260921-205545-publish-prompt-id-provenance-package
PAIR_KEY=20260921-205545-publish-prompt-id-provenance-package
```

## Materialization history

Initial package materialization:

```text
07ab19614006a9c75432ae6a227546b494843e1a
```

Initial readback receipt:

```text
fe153f57cdfa9e8d2bded23e390692c765986700
```

Those commits remain in history.

The first materialization exposed two system-specific generator source files in an active-looking public path. The current correction removes those files from HEAD while preserving their historical hashes and the original Git history.

## Corrected public boundary

Retained as active/public tooling:

```text
tools/generate-publication-ids.js
PROV-NOTION-...
PROV-GITHUB-...
```

Removed from the current public tree:

```text
research/agent-self-report/source-tools/generate-prompt-id.js
research/agent-self-report/source-tools/generate-update-ids.js
```

Historical source identifiers may still appear inside evidence records when they are necessary to describe the original event faithfully.

## Source package integrity

```text
SOURCE_PACKAGE_SHA256=
f2bbea1aa127b79de967cd2ddb4995d3510be9dda10d04f2dd0b447be89b92e6

INTERNAL_MANIFEST_CHECK=
PASS
```

## Notion side

```text
NOTION_STATUS=PENDING
NOTION_NATIVE_PAGE_ID=null
NOTION_READBACK=null
```

No Notion mutation is part of this correction.
