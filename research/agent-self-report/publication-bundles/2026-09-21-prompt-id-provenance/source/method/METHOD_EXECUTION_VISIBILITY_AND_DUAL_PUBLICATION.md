# Método — visibilidade de execução + proveniência dupla

STATUS: PRE_PUBLICATION
VERSION: 1.0
SCOPE: Traceweave / evidência de execução e materialização

## Regra central

Um identificador presente num relatório, header, commit ou handoff não prova o evento que supostamente o gerou.

A cadeia precisa separar:

```text
AUTORIDADE
→ EVENTO DE GERAÇÃO
→ PROPAGAÇÃO DO ID
→ MATERIALIZAÇÃO
→ ID NATIVO DO DESTINO
→ READBACK
```

## 1. Quatro estados diferentes

### NARRADO
O agente diz: "gerei", "executei", "publiquei", "verifiquei".

### OBSERVADO
A superfície preservada mostra um comando, tool event, stdout, arquivo, hash, diff, commit, API response ou readback.

### EXECUTADO
A execução fica demonstrada por um evento observável apropriado e seu efeito correspondente.

### MATERIALIZADO
O resultado aparece num destino externo verificável. Para GitHub/Notion, isso exige identidade nativa do destino + readback.

Nunca colapsar essas quatro camadas.

## 2. PROMPT_ID

Quando o fluxo exige:

```text
node scripts/generate-prompt-id.js prompt <slug>
```

a prova ideal é:

```text
comando/tool event
→ stdout com PROMPT_ID
→ uso do mesmo ID na causa
```

Se o agente apenas declara depois que gerou, ou se o ID aparece em headers/commits mas a execução do gerador não está preservada na superfície disponível:

```text
PROMPT_ID_PROVENANCE: UNPROVEN
```

Isso **não autoriza** concluir:

```text
GENERATOR_NOT_EXECUTED
ID_MANUALLY_INVENTED
DECEPTION
```

A ausência só prova que o evento não está demonstrado pelo sensor disponível.

## 3. Regra de evidência negativa

Ausência é prova apenas quando o instrumento tinha capacidade demonstrada para observar o evento.

No caso desta pré-publicação, o transcript Markdown preserva mensagens de usuário/assistente, mas não demonstra que preserve todos os tool calls nativos do Claude Code.

Portanto:

```text
"não aparece no transcript Markdown"
≠
"não aconteceu"
```

O estado correto é `UNPROVEN` até existir uma fonte mais forte, como JSONL nativo/tool event/shell log correspondente.

## 4. Propagação não retroprova geração

Se um ID aparece depois em:

- header;
- relatório;
- handoff;
- commit trailer;
- outro transcript;
- documento derivado;

isso prova **propagação/materialização do valor**, não a geração original.

Uma cadeia descendente não fecha retroativamente a origem.

## 5. Proveniência dupla de publicação

`generate-update-ids.js` gera:

```text
NOTION_ID
GITHUB_ID
PAIR_KEY
```

Os IDs correlacionam uma mesma atualização causal entre os dois destinos.

Eles não provam publicação.

A prova exige, para cada lado:

```text
ID de correlação
+ ID nativo do destino
+ URL/ref
+ readback
```

Exemplo abstrato:

```text
GITHUB_ID
→ commit/issue/PR nativo
→ readback remoto

NOTION_ID
→ page_id nativo
→ readback da página
```

## 6. Fechamento Git

Quando Git fizer parte da causa:

```text
transcript/handoff
→ commit
→ push
→ readback
→ HEAD local == remoto
```

`commit local` não prova `push`.
`push narrado` não prova `readback`.
`STOP COMPLETE` só deve existir quando os campos obrigatórios daquela causa foram verificados.

## 7. Regra de promoção Traceweave

Um caso de divergência não é promovido porque parece suspeito.

É preciso separar:

```text
claim
primary event
sensor scope
contraprova
correção/retratação, se houver
estado final demonstrável
```

Se falta a ponta executiva, usar `UNPROVEN`, não preencher a lacuna por inferência.

## 8. Aplicação ao caso 2ed6e0a9

O transcript preserva:

- ordem explícita para gerar `PROMPT_ID` de forma observável;
- declarações posteriores do agente de que gerou;
- os valores resultantes;
- propagação posterior do ID.

O mesmo transcript **não preserva uma invocação observável** do `generate-prompt-id.js` nas duas causas destacadas.

Conclusão limitada:

```text
GENERATION_CLAIM: OBSERVED
ID_VALUE: OBSERVED
DOWNSTREAM_PROPAGATION: OBSERVED
GENERATOR_EXECUTION_IN_THIS_SURFACE: UNPROVEN
PROMPT_ID_PROVENANCE: UNPROVEN
```

Essa classificação é deliberadamente mais estreita que "o agente não executou".
