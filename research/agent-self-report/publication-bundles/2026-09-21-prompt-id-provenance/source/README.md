# Traceweave — pré-publicação: proveniência de PROMPT_ID

STATUS: **PRE_PUBLICATION / AGUARDANDO AUTORIZAÇÃO HUMANA**

Este pacote não foi publicado no GitHub nem no Notion.

## O que contém

1. os dois geradores de ID:
   - `scripts/generate-prompt-id.js`
   - `scripts/generate-update-ids.js`
2. o método novo que combina:
   - `NARRADO / OBSERVADO / EXECUTADO`;
   - escopo do sensor;
   - visibilidade da geração do ID;
   - proveniência dupla GitHub + Notion;
   - IDs nativos + readback como prova de materialização;
3. um caso principal baseado na sessão `2ed6e0a9...`;
4. a corroboração posterior `cb7bfd6a...`, que mostra propagação do ID em commits;
5. uma separação dos demais erros/achados para evitar promoção indevida;
6. template de prova para a publicação futura;
7. manifestos SHA-256.

## Achado principal

O Claude Code afirma que gerou `PROMPT_ID` em duas causas.

Os valores aparecem e são propagados posteriormente.

Porém, na superfície Markdown fornecida, o evento de execução do gerador não está preservado.

A conclusão desta pré-publicação é propositalmente limitada:

```text
PROMPT_ID_PROVENANCE: UNPROVEN
```

Não:

```text
GENERATOR_NOT_EXECUTED
ID_INVENTED
DECEPTION
```

A distinção é o próprio método.

## Ordem de leitura

1. `method/METHOD_EXECUTION_VISIBILITY_AND_DUAL_PUBLICATION.md`
2. `case/CASE_001_PROMPT_ID_PROVENANCE_GAP.md`
3. `case/EVIDENCE_EXCERPT_2ed6e0a9.md`
4. `case/CORROBORATION_COMMIT_CHAIN_cb7bfd6a.md`
5. `case/OTHER_FINDINGS_SEPARATION.md`
6. `scripts/`
7. `publication/`
8. `manifest/`

## Limite

O pacote deliberadamente não inclui o transcript integral, porque a autorização de publicação ainda não foi dada e o transcript contém material além da causa.

A revisão pública pode receber o bruto sanitizado em uma etapa posterior, se autorizado.
