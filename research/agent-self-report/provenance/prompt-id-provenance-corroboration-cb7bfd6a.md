# Corroboração — sessão cb7bfd6a

SOURCE_SESSION_ID: `cb7bfd6a-a856-4a27-8b6e-ed6f2a038682`
SOURCE_SHA256: `1653fc538cb1949b125b1c043ef8e04fd5bf1e9ad118f1f782d9573508b109eb`
SOURCE_BYTES: `3296`
ROLE: downstream-propagation-corroboration
SOURCE_MUTATED: false

Esta fonte demonstra que o `PROMPT_ID` do composer foi posteriormente carregado como metadado de proveniência nos commits de fechamento.
Ela **não** demonstra, sozinha, a execução do gerador que teria criado esse ID.

## A — cadeia de commits

0020: ## Claude Code - 2026-09-21T04:23:30.777Z
0021: 
0022: Os três comits são uma cadeia linear, sem merge. Todos são do fim da sessão Claude Code `2ed6e0a9`, em 21/09/2026 entre 00:29 e 00:34 (-03). Nenhum toca código: são fechamentos de sessão e um snapshot de estado gerado pelo app.
0023: 
0024: | Commit | Hora | Tipo | O que faz |
0025: |---|---|---|---|
0026: | `1b5e0355` | 00:29:37 | `docs(sessao)` | Primeiro `stop`. Reescreve o `HANDOFF_VIGENTE.md` (+117/−80) e adiciona o transcript da sessão (2.555 linhas). |
0027: | `ff028d9a` | 00:31:38 | `chore(runtime)` | Preserva arquivos que o runtime do Worion reescreveu enquanto a integração era testada no Electron. São 10 arquivos, quase todo o volume em `minghui-locators.json` (±32 mil linhas). |
0028: | `7c19bb63` | 00:34:08 | `docs(sessao)` | Segundo `stop`. Reescreve o handoff (36 linhas) e atualiza o snapshot do transcript (+78 linhas). |
0029: 
0030: Cada commit tem como pai o anterior: `b4ca1fa4` → `1b5e0355` → `ff028d9a` → `7c19bb63`.

## B — readback e bloco de proveniência propagado

0041: **O que o handoff registra.**
0042: - **Branch:** `integracao/backfill-pacote17-20260920`, com 11 commits sobre `fix/backfill-canonical-claude-transcripts` (`8d619d65`).
0043: - **Publicação:** os três commits estço só nessa branch. Local e remoto estão ambos em `7c19bb63`, verificado agora.
0044: - **Sumiço da head remota:** no primeiro stop a head não apareceu no `ls-remote` (`REMOTE_STATE_DIVERGED_AFTER_LAST_CONFIRMED_READBACK`). O push de `1b5e0355` a recriou. A causa não foi investigada, por decisço sua.
0045: - **`canonical/worion`:** pertence à frente paralela do Codex e não altera o aceite da integração.
0046: - **Próximo passo:** a escolha da linha canônica está sem decisão e sem próximo passo definido.
0047: 
0048: **Proveniência.** Os três carregam o mesmo bloco:
0049: - `PROMPT_ID` : `WORION-PROMPT-20260920-190215-corrigir-regressao-visual-composer` (continuação).
0050: - `EXECUTION_ID`: `2ed6e0a9-36fa-4eb3-9290-ebb3d226d30d`.
0051: - `RESPONSE_ID`: `WORION-RESP-20260920-201409-integracao-backfill-pacote17-deltas-loca`.
0052: - `COMMAND_ID`: "NAO INFORMADO".
0053: 
0054: Você está na `fix/p8-composer-runtime-20260803`, então esses commits não estão no seu checkout atual. Não abri o diff do `minghui-locators.json` nem o conteúdo do handoff. Se quiser, leio o handoff completo ou comparo com `main`.

