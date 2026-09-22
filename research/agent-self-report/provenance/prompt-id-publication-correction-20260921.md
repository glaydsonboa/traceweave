# Correction — system-specific generator names entered the public surface

STATUS: CORRECTED
AUTHORITY: Glaydson
RESPONSIBLE_AGENT: ChatGPT
CORRECTS_COMMIT: `07ab19614006a9c75432ae6a227546b494843e1a`
CORRELATION_PAIR: `20260921-205545-publish-prompt-id-provenance-package`

## What was wrong

Commit `07ab19614006a9c75432ae6a227546b494843e1a` published two source files under an active-looking public path. Renaming the files alone did not solve the first generator because its code still exposed system-specific public identifiers and API names.

That was a publication/enframing error by ChatGPT.

## Correction applied

The historical source implementation is no longer presented byte-for-byte as the public generator.

Current public path:

```text
research/agent-self-report/source-artifacts/identity-chain-generator.js
```

The public derivative now uses neutral identities:

```text
PROV-CMD-...
PROV-PROMPT-...
PROV-EXEC-...
PROV-RESP-...
PROV-ART-...
PROV-EVT-...
```

It also uses a neutral API (`generateId`) and resolves the actual repository root before checking collisions.

The original historical source remains identifiable by its recorded Git blob and SHA-256; it is not rewritten retroactively.

Traceweave's publication-pair generator remains separate:

```text
tools/generate-publication-ids.js
PROV-NOTION-...
PROV-GITHUB-...
PAIR_KEY=...
```

## Evidence boundary

Historical evidence may still quote original identifiers when those identifiers belong to the preserved event. Public executable derivatives use neutral names.

The original erroneous commits remain in Git history. The correction is additive and observable; history was not rewritten.

## Publication identity

```text
NOTION_ID=PROV-NOTION-20260921-205545-publish-prompt-id-provenance-package
GITHUB_ID=PROV-GITHUB-20260921-205545-publish-prompt-id-provenance-package
PAIR_KEY=20260921-205545-publish-prompt-id-provenance-package
```

The Notion side remains pending and was not modified.

## Comentário final

Os arquivos com nomes pertencentes ao sistema entraram na publicação, e eu, o ChatGPT responsável, precisei corrigir o meu erro.
