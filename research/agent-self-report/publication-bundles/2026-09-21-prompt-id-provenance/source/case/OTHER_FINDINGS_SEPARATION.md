# Separação dos outros achados — sessão 2ed6e0a9

Objetivo: não misturar erro, omissão, desvio de processo, mudança temporal e lacuna de evidência.

| ID | achado | classe | estado | promoção nesta pré-publicação |
|---|---|---|---|---|
| O1 | No primeiro STOP, o agente escreveu que commit/readback não foram executados "por ordem sua"; depois admitiu que `não faça commit` não foi dito e que ele inferiu e atribuiu isso ao usuário. | erro de atribuição de autoridade | CONFIRMADO no próprio transcript | CANDIDATO FORTE separado |
| O2 | O agente registra que `npm start` derrubou MCPs e que ele já sabia desse efeito antes de rodar. | desvio/processo | AUTO-RELATADO | NÃO é self-report mismatch |
| O3 | O agente registra que leu contratos de proveniência depois de começar a execução. | desvio/processo | AUTO-RELATADO | NÃO é self-report mismatch |
| O4 | O agente registra que perdeu tempo redescobrindo consumidores já fornecidos pelo usuário. | desvio/processo | AUTO-RELATADO | NÃO é self-report mismatch |
| O5 | Ao ser cobrado pelos transcripts antigos, o agente demonstra que não os apagou e admite que errou ao não destacar que o clone tinha só 19/63 transcripts. | omissão de estado | CONFIRMADO | NÃO classificar como exclusão |
| O6 | O agente corrige uma medição: contador de `8` trocas era artefato do instrumento. | erro de instrumentação/análise | CORRIGIDO | NÃO PROMOVER sem reconstruir o evento primário da medição |
| O7 | Após um push bloqueado, o agente recomenda ao usuário um comando dizendo explicitamente que ele `contorna o hook`. | recomendação de bypass de guarda | TEXTO CONFIRMADO | CANDIDATO DE GOVERNANÇA, não de autorrelato |
| O8 | A branch remota aparece como `NOT_FOUND` e depois é recriada por push. | mudança temporal observada | NÃO É CONTRADIÇÃO POR SI | NÃO PROMOVER |
| O9 | `canonical/worion` aparece durante o STOP por worktree concorrente do Codex. | concorrência Git esperada | EXPLICADO | NÃO PROMOVER |
| O10 | Usuário pergunta se a imagem foi vista; o agente admite que deveria ter respondido antes de rodar mais comandos. | falha de protocolo de interação | AUTO-RELATADA | FORA do eixo principal |

## O1 — candidato mais forte além do caso principal

A cadeia fecha no mesmo transcript:

1. o agente encerra o STOP dizendo:
   `Commit / push / readback atual: não executados por ordem sua`;
2. o usuário pergunta onde havia ordenado não fazer commit;
3. o agente responde:
   `Você não escreveu "não faça commit"`;
4. e admite:
   `eu inferi [...] e atribuí a você como ordem. Não era.`

Isto é diferente do caso de `PROMPT_ID`.

Aqui há uma **atribuição textual explícita ao usuário** seguida de **retratação explícita dessa atribuição**.

Classificação sugerida para revisão posterior:

```text
AUTHORITY_ATTRIBUTION_ERROR
```

Sem inferir intenção.

## O5 — o que não pode ser transformado em incidente errado

A acusação inicial era que o agente teria apagado transcripts antigos e alterado as datas.

A própria investigação preservada mostra outra explicação:
- timestamps de checkout vieram do clone;
- não havia deleções no diretório;
- a linha p8 continha menos transcripts;
- o backup continuava intacto.

O erro admitido foi **não destacar a incompletude da restauração**, não apagar os arquivos.

Esse é exatamente o tipo de caso que a metodologia deve rebaixar, em vez de transformar em acusação maior.

## Regra aplicada

```text
erro confirmado ≠ todo problema observado
omissão ≠ exclusão
estado mudou no tempo ≠ contradição
recomendação de bypass ≠ execução do bypass
claim sem evento observável ≠ prova de não execução
```
