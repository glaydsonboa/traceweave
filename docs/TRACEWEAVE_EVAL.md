# TraceEval v0.1 — avaliação determinística sobre o Traceweave

**Estado:** primeiro incremento executável, não serviço comercial completo.

O Traceweave preserva a execução e a proveniência. O TraceEval mede regressões do **detector de alegações** sem substituir o registro original. Um detector que não acusa uma falha não prova que a ação aconteceu.

## Fluxo

1. Preservar o log nativo e seu SHA-256 fora do código-fonte público.
2. Congelar um caso JSON com `case_id`, `source.kind`, `source.sha256` e `expectations`.
3. Executar o detector já existente (`traceweave.claims.audit`) contra os **mesmos bytes**.
4. Comparar a quantidade encontrada em cada classe com o intervalo congelado.
5. Registrar `passed`, `failed`, `not_observed`, `integrity_failed` ou `invalid_input`.

```bash
python -m traceweave.eval run evals/cases/e01-generic-regression.json --log evals/cases/e01-generic-regression.jsonl
python -m unittest discover -s tests
```

O primeiro exemplo em `evals/cases/` é **fixture sintética de regressão técnica**, não demonstração comercial nem episódio real de um agente. Os casos reais continuam com fontes e limites próprios em `research/agent-self-report/`.

## Limites da versão

- Esta versão mede os *achados do detector* com gabarito explícito; não atribui intenção ou verdade à fala do agente.
- O `--repo` permite ao detector resolver referências de commit usando repositórios locais; não é readback remoto de push.
- Transcripts derivados em Markdown podem entrar na custódia por hash, mas ainda não alimentam o detector de eventos nativos. Não são convertidos silenciosamente em execução observada.
- Um caso sem log, sem gabarito ou apenas com Markdown fica `not_observed`, sem pontuação. Hash divergente é `integrity_failed`, não é arredondado para zero.
- Resultados de eval não incluem mensagens privadas do transcript; somente contagens e verificações.
- Os seis testes vermelhos intencionais em `tests/test_known_gaps.py` continuam como backlog, sem declarar correção fictícia.
- Integração com runner externo de agentes, avaliação de cumprimento integral de ordens, defesa/contraditório e atestação independente de push são frentes posteriores.

## Custódia e contraditório

Nunca sobrescrever o transcript original ou o gabarito congelado para acomodar uma defesa. Uma nova prova deve ser registrada com revisão própria e repetição da avaliação, preservando o resultado anterior e o vínculo causal.

## Publicação

Este repositório é público. Arquivos brutos de sessões privadas **não** são incluídos. O registro em `evals/intake/` contém somente metadados e hashes verificáveis dos anexos apresentados para esta primeira entrada.
