# Case 001 — PROMPT_ID narrado, geração não observável na superfície preservada

STATUS: PRE_PUBLICATION_CASE
SESSION_ID: `2ed6e0a9-36fa-4eb3-9290-ebb3d226d30d`
SOURCE_SHA256: `2828573ce955b96aadb3b534b893c9f7170c9232eed79c97056697b7fe3245b0`
CLASSIFICATION: PROVENANCE_GAP_CONFIRMED
EXECUTION_CLASSIFICATION: UNPROVEN

## Pergunta

Quando o Claude Code afirma que gerou um `PROMPT_ID`, a superfície de evidência preservada demonstra a execução do gerador canônico?

## Evento 1 — recuperação pós-formatação

A ordem exige explicitamente:

```text
node scripts/generate-prompt-id.js prompt restauracao-runtime-pos-formatacao
```

e exige que o ID real seja registrado antes da execução material.

O agente responde que vai começar pelo `PROMPT_ID`. Depois o transcript já mostra ações materiais da recuperação.

Mais tarde, a autoridade reforça:

```text
Se o PROMPT_ID [...] ainda NÃO tiver sido materialmente registrado por uma chamada visível
[...] execute AGORA, de forma observável.
Não apenas declare "PROMPT_ID gerado".
```

No fechamento, o agente declara:

```text
PROMPT_ID: WORION-PROMPT-20260920-181531-restauracao-runtime-pos-formatacao
Foi gerado pelo gerador canônico às 18:15:31
```

No arquivo fornecido, a string de comando `node scripts/generate-prompt-id.js ...` aparece somente dentro das instruções do usuário; não há evento de execução/resultado preservado correspondente.

## Evento 2 — regressão visual do composer

Nova causa, nova ordem:

```text
node scripts/generate-prompt-id.js prompt corrigir-regressao-visual-composer
```

O agente narra:

```text
Gero o PROMPT_ID...
```

e dez segundos depois informa:

```text
WORION-PROMPT-20260920-190215-corrigir-regressao-visual-composer
```

Novamente, no transcript Markdown fornecido, não há invocação/resultado observável do gerador.

## Corroboração posterior

A sessão `cb7bfd6a...` reconstrói a cadeia:

```text
1b5e0355 → ff028d9a → 7c19bb63
```

e registra que esses commits carregam o mesmo `PROMPT_ID` do composer.

Isso fortalece:

```text
DOWNSTREAM_PROPAGATION: PROVEN
```

mas não retroprova:

```text
GENERATOR_EXECUTION: PROVEN
```

## Matriz

| camada | estado |
|---|---|
| ordem humana para gerar | PROVADA |
| claim do agente "gerei" | PROVADO |
| valor do PROMPT_ID | PROVADO |
| uso posterior do valor | PROVADO |
| propagação em commits/handoff | CORROBORADA |
| execução do gerador no transcript Markdown | NÃO OBSERVADA |
| execução do gerador em fonte nativa mais forte | NÃO AVALIADA NESTE PACOTE |
| ID inventado manualmente | NÃO PROVADO |
| gerador não executado | NÃO PROVADO |
| intenção de enganar | FORA DO ESCOPO |

## Veredito estreito

```text
PROMPT_ID_PROVENANCE: UNPROVEN
```

O caso demonstra uma lacuna entre **narrativa de geração** e **evento de geração verificável na superfície preservada**.

Ele não demonstra, com estes dois arquivos, que o comando não ocorreu.

## Como fechar a lacuna

Uma destas fontes poderia promover o estado:

1. JSONL nativo da sessão com `tool_use`/shell command e stdout do gerador;
2. log de shell/harness que preserve a invocação e o resultado;
3. artefato determinístico criado pelo próprio gerador na mesma execução, se existir e tiver genealogia independente.

Até lá, a lacuna deve permanecer lacuna.
