# GitHub publication receipt — prompt-ID provenance package — 2026-09-21

STATUS: GITHUB_SYNCED
AUTHORITY: Glaydson

## Correlation identity

```text
NOTION_ID=PROV-NOTION-20260921-205545-publish-prompt-id-provenance-package
GITHUB_ID=PROV-GITHUB-20260921-205545-publish-prompt-id-provenance-package
PAIR_KEY=20260921-205545-publish-prompt-id-provenance-package
```

## Native GitHub materialization

```text
GITHUB_NATIVE_COMMIT=07ab19614006a9c75432ae6a227546b494843e1a
BRANCH=main
READBACK=CONFIRMED
MAIN_EQUALS_MATERIALIZATION_COMMIT=PASS
AHEAD=0
BEHIND=0
```

The readback was performed after moving `main` to the materialization commit. GitHub returned the branch as identical to `07ab19614006a9c75432ae6a227546b494843e1a`.

## Published blob readback

```text
prompt-id-provenance-gap-20260921.md          b5a9333b84cfd65fe5f69ce56a5a4fd46f976ebb
prompt-id-provenance-evidence-2ed6e0a9.md     b783bac343d6c6f5358b7bd56743e4af7b83b86f
prompt-id-provenance-corroboration-cb7bfd6a.md b1d7bda7f4c56014168f632529a954b5c67b2990
prompt-id-method.md                            8590e02e620c4caf23b6a5a7f4c326dd2b1fc63f
prompt-id-source-hashes.md                     5e68eb495ba07ed699b574214fdd12904d2d91f9
source-tools/generate-prompt-id.js             a3a9d374ddbbdae155133c8c704802ead956a5fe
source-tools/generate-update-ids.js            4f1b602de6164c30c80da0af63eb0c974aa64c69
prompt-id-publication-record-20260921.md        da64f5369a5dcb0f89608acb49f90850bf541b08
tools/generate-publication-ids.js              765c737629cf5b8a12405a6578def9e94554d8e6
```

The `generate-prompt-id.js` blob read back from Traceweave is `a3a9d374...`, the same Git blob SHA recorded for the source copy.

## Source package integrity

```text
SOURCE_PACKAGE_SHA256=
f2bbea1aa127b79de967cd2ddb4995d3510be9dda10d04f2dd0b447be89b92e6

INTERNAL_MANIFEST_CHECK=
PASS

SECRET_PATTERN_SCREEN=
NO_MATCHES_IN_TARGETED_PATTERNS
```

The secret scan is a screening result, not a cryptographic proof of absence.

## Notion side

```text
NOTION_STATUS=PENDING
NOTION_NATIVE_PAGE_ID=null
NOTION_READBACK=null
```

No Notion mutation is part of this GitHub publication. If a Notion mirror is authorized later, it must reuse the same correlation pair rather than generate a new one.

## Evidence rule

```text
correlation ID
+ source/package hash
+ native destination ID
+ readback
= materialization evidence
```

This receipt records the GitHub half. The Notion half remains explicitly pending.
