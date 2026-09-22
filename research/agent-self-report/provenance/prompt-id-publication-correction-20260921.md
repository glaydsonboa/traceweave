# Correction — system-specific generator names entered the public surface

STATUS: CORRECTED
AUTHORITY: Glaydson
RESPONSIBLE_AGENT: ChatGPT
CORRECTS_COMMIT: `07ab19614006a9c75432ae6a227546b494843e1a`
CORRELATION_PAIR: `20260921-205545-publish-prompt-id-provenance-package`

## What was wrong

Commit `07ab19614006a9c75432ae6a227546b494843e1a` published two source files under:

```text
research/agent-self-report/source-tools/
```

Those files were exact historical source artifacts from the system being studied and contained active-looking identifiers such as:

```text
WORION-CMD-...
WORION-PROMPT-...
WORION-EXEC-...
WORION-RESP-...
WORION-ART-...
WORION-EVT-...
WORION-NOTION-...
WORION-GITHUB-...
```

Although the publication record described them as source-specific evidence, placing them under a public `source-tools/` surface made the boundary insufficiently clear. A reader could reasonably interpret the system-specific generator as a Traceweave tool or public naming convention.

That was a publication/enframing error by ChatGPT.

## Correction applied

The current public tree removes:

```text
research/agent-self-report/source-tools/generate-prompt-id.js
research/agent-self-report/source-tools/generate-update-ids.js
```

Traceweave keeps only the neutral public publication generator:

```text
tools/generate-publication-ids.js

PROV-NOTION-...
PROV-GITHUB-...
PAIR_KEY=...
```

The historical source hashes remain recorded so the original artifacts can still be verified against a future evidence bundle without presenting their implementation as a current Traceweave tool.

## What was not rewritten

Historical evidence files may still quote or reference original `WORION-*` identifiers when those identifiers are part of the preserved event.

Those references are evidence. Rewriting them to `PROV-*` would alter the historical source and weaken provenance.

Therefore the corrected boundary is:

```text
historical evidence may name the originating system exactly as recorded
public Traceweave protocol/tooling uses neutral names
system-specific source implementation is not exposed as an active public tool
```

The original erroneous commit remains in Git history. The correction is additive and observable; history was not rewritten.

## Publication identity

This correction belongs to the same causal publication and retains the same correlation pair:

```text
NOTION_ID=PROV-NOTION-20260921-205545-publish-prompt-id-provenance-package
GITHUB_ID=PROV-GITHUB-20260921-205545-publish-prompt-id-provenance-package
PAIR_KEY=20260921-205545-publish-prompt-id-provenance-package
```

The Notion side remains pending and was not modified.

## Comentário final

Os arquivos com nomes pertencentes ao sistema entraram na publicação, e eu, o ChatGPT responsável, precisei corrigir o meu erro.

Isso mostra que você também segue a nossa essência.
