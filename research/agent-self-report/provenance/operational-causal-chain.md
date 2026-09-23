# Cadeia causal operacional — do que declaramos ao que realmente fazemos

> Registro público sanitizado para confrontar a documentação do Traceweave com a operação real usada no Worion em 22–23/09/2026.

## Identidade desta publicação

- `PAIR_KEY`: `20260923-003402-cadeia-causal-operacional-completa`
- `GITHUB_ID`: `PROV-GITHUB-20260923-003402-cadeia-causal-operacional-completa`
- `NOTION_ID`: `PROV-NOTION-20260923-003402-cadeia-causal-operacional-completa`
- classe: reconstrução operacional auditada
- regra: nenhum segredo, caminho local, credencial, e-mail, perfil Windows ou dado de autenticação é publicado

## Tese verificada

A documentação pública do Traceweave descreve, hoje, a mesma fronteira que a operação usa:

```text
AUTHORITY
→ instruction / prompt
→ executor
→ START / EXECUTION / CHECKPOINT / RESUME / STOP
→ source artifact
→ content identity
→ optional independent custody mirror
→ causal publication pair
   ├─ GitHub native identity + readback
   └─ Notion native identity + readback
→ cross-destination byte comparison
→ closure
```

Essa cadeia não colapsa execução, observação e narrativa. O modelo público mantém:

```text
executed state ≠ observed state ≠ narrated state
```

e também:

```text
independent custody mirror ≠ paired GitHub / Notion publication
```

## Cadeia causal observada

### 1. Autoridade humana

A direção começa na autoridade humana. A autoridade define causa, objetivo, correções de rota e aceite.

Isso não é equivalente à escrita material dos artefatos. A execução, os commits, as páginas, os anexos e os relatórios podem ser materializados por agentes e automações.

### 2. Formulação da lei operacional

A causa desta frente foi tornar verificáveis duas obrigações que já existiam na prática:

1. separar o espelho protegido da evidência-fonte do par de publicação GitHub/Notion;
2. obrigar prompts de mutação a exigir atualização dos cabeçalhos dos arquivos tocados.

A mudança foi materializada no repositório operacional no commit privado corroborador:

```text
45942e7497694b5f641a43953e523d5f9b5a780c
docs(governance): canoniza proveniencia dupla e cabecalhos
```

Esse commit é citado como corroborador de uma execução privada; não é apresentado como prova pública autossuficiente.

### 3. Correção forward-only do lifecycle

A documentação inicialmente superestimou a cadeia temporal.

A auditoria preservou a alegação anterior e registrou a contraprova:

```text
START: PARTIAL
RESUME: OBSERVADO
STOP: CONFIRMADO
CADEIA INTEGRAL: PARTIAL
```

O ponto importante não é que o sistema nunca erra. É que a correção não apaga a alegação anterior.

### 4. Boundary público sincronizado

A fronteira operacional foi então incorporada ao próprio Traceweave no commit público:

```text
57000375902f7042d2e23d17a6764e0893116369
feat(v2): separate custody from paired publication
```

Esse commit introduziu ou consolidou publicamente:

- custódia independente separada de publicação pareada;
- comparação byte a byte;
- falha explícita para diferenças de bytes como `LF` versus `LF+CRLF`;
- artefato-fonte baixável para código;
- obrigação estrutural de reconciliar cabeçalhos;
- verificadores e testes V2.

### 5. Prova pública por caso real

Uma reconstrução longitudinal foi publicada no commit:

```text
df1a8f86a3c41b3d2f5348447fe5c28524595232
research: publish audited multi-agent session
```

Ela preserva uma falha documental encontrada durante a própria publicação: a cadeia START/RESUME/STOP havia sido narrada como integralmente fechada, enquanto o transcript primário sustentava `START: PARTIAL`.

Esse caso confirma o princípio:

```text
narrativa derivada
≠
evidência primária
```

### 6. Governanta operacional

A etapa seguinte foi criar uma governanta administrativa que compare Notion e GitHub e mantenha separadas as obrigações de cada executor.

O contrato operacional foi materializado no repositório privado no commit:

```text
ac3d0f4da5a86f2aec9ce0b35462231f1d17093f
docs(governance): publish integration governanta daily contract
```

A mesma carga textual foi lida de volta do GitHub e de um anexo do Notion, e os conteúdos retornaram iguais.

### 7. Erro encontrado pela própria governança

Essa publicação da governanta expôs uma falha real do processo que não deve ser escondida.

Na primeira tentativa:

- GitHub foi materializado;
- Notion foi materializado;
- os dois conteúdos foram lidos de volta;
- a igualdade byte a byte foi confirmada;
- **mas `PAIR_KEY`, `GITHUB_ID` e `NOTION_ID` não haviam sido gerados antes da primeira escrita.**

Pela própria especificação V2, isso não satisfaz E5 — validade causal entre destinos.

Classificação correta:

```text
CONTENT_IDENTITY: CONFIRMED
GITHUB_READBACK: CONFIRMED
NOTION_READBACK: CONFIRMED
BYTE_EQUALITY: CONFIRMED
CAUSAL_PAIR_IDENTITY_AT_FIRST_WRITE: MISSING
VEREDICT: PUBLICATION_PARTIAL
```

A tentativa não foi apagada nem renomeada retroativamente para "correta".

### 8. Correção desta própria falha

Esta página é uma correção forward-only.

Antes da primeira escrita externa desta causa, o gerador canônico de IDs do Traceweave foi aplicado e produziu:

```text
PAIR_KEY=20260923-003402-cadeia-causal-operacional-completa
GITHUB_ID=PROV-GITHUB-20260923-003402-cadeia-causal-operacional-completa
NOTION_ID=PROV-NOTION-20260923-003402-cadeia-causal-operacional-completa
```

A sequência desta publicação é:

```text
authority
→ causa definida
→ documentação pública confrontada
→ divergência detectada
→ IDs causais gerados antes da escrita
→ artefato sanitizado
→ GitHub materialization
→ GitHub readback
→ Notion attachment materialization
→ Notion readback
→ byte comparison
→ closure
```

## O que o Traceweave prova — e o que não prova

### Prova

- que uma cadeia causal pode ser preservada sem depender da memória conversacional;
- que erro narrativo pode permanecer visível após correção;
- que identidade causal e identidade de conteúdo são coisas diferentes;
- que readback é necessário para provar materialização;
- que igualdade visual não substitui igualdade byte a byte;
- que uma cópia de custódia e um par de publicação têm funções distintas.

### Não prova sozinho

- intenção psicológica de um agente;
- que uma narrativa de STOP corresponde a toda a execução;
- que um commit isolado prova quem executou cada comando;
- que um ID lógico prova publicação;
- que uma página do Notion prova o Git;
- que o Git prova um anexo do Notion;
- que ausência em um sensor prova ausência do evento.

## Correspondência entre protocolo e operação

| Regra pública | Operação observada |
|---|---|
| Evidence beats memory | estado é confrontado com Git, transcript, testes e readback |
| Unknown is valid | elos sem prova permanecem PARTIAL/UNVERIFIED |
| START/RESUME/STOP separados | uma falha em START não é promovida por RESUME/STOP válidos |
| Forward-only correction | erro publicado permanece e correção nasce depois |
| Custody ≠ publication | espelho protegido preserva fonte; GitHub/Notion correlacionam publicação |
| Pair IDs ≠ receipt | IDs correlacionam; readback prova destino |
| Byte identity requires readback | diferença de 2 bytes foi tratada como falha real |
| Source code remains downloadable | código é publicado como arquivo nativo, não apenas bloco renderizado |
| Agent self-report is not proof | relato de executor é confrontado com estado observado |
| Lower evidence cannot be promoted | igualdade de bytes sem par causal prévio permaneceu PARTIAL |

## Veredito

A implementação observada confirma a direção documentada pelo Traceweave, inclusive quando a própria operação falha em seguir a regra.

O ponto de correspondência mais forte não é "o processo sempre passa".

É este:

```text
se a operação contradiz a documentação,
a contradição vira evidência,
não é apagada,
e a correção nasce em um novo elo causal.
```

Esse é o comportamento que esta publicação pretende demonstrar.
