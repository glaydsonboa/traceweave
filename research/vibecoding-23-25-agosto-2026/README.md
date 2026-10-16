# VibeCoding não é só deixar a IA rodar. Tem que acompanhar.

**23 a 25 de agosto de 2026 · resumo público com âncoras de hash · fonte privada sob custódia**

Glaydson Boaventura constrói o Worion, um sistema de IA proprietário, dirigindo Claude Code, Codex e DeepSeek. Esta página registra três dias desse trabalho, medidos nos transcripts das sessões e no Git: quanto tempo ele ficou na frente das IAs, quando descansou e o que mudou porque estava acompanhando. As IAs executaram; a direção, as correções e o teste em uso real foram dele. O código do Worion, as credenciais e os transcripts integrais não são publicados.

## O tempo corrido

Cada bloco começa na primeira fala de Glaydson e termina na última antes de uma parada longa. Horário de Brasília.

| bloco | de → até | tempo corrido | maior pausa dentro do bloco |
|---|---|---:|---:|
| trabalho | 23/08 07:25 → 24/08 00:45 | **17 h 20 min** | 1 h 33 min |
| descanso | 24/08 00:45 → 10:13 | 9 h 28 min | — |
| trabalho | 24/08 10:13 → 25/08 06:03 | **19 h 50 min** | 1 h 09 min |
| descanso | 25/08 06:03 → 09:17 | 3 h 13 min | — |
| trabalho | 25/08 09:17 → 12:35 | **3 h 18 min** | 1 h 51 min, que inclui o teste no app (11:32–11:48) |

O segundo bloco atravessou a madrugada. Às 05:56 de 25/08, Glaydson escreveu na janela do Claude:

> hoje o job rendeu. 20 horas aki sentado. Amanheceu, peguei a viola e fui me deitar.

O registro mede 19 h 50 min nesse bloco. Às 09:17 ele voltou com "diaaa.. verfica as pontas soltas". Às 07:21 aparece uma mensagem com o rótulo do usuário, "Your claude.ai usage limit has reset…": ela é automática e não interrompe o descanso.

A conta só enxerga as janelas das CLIs. O que ele fez no ChatGPT, no claude.ai ou direto no Worion fica de fora.

## As janelas

De 24/08 00:40 a 25/08 12:40, a cadeia literal tem três janelas:

| janela | sessão | falas de Glaydson | respostas da IA | blob do transcript |
|---|---|---:|---:|---|
| Claude Code | `fa9c0182-f720-414b-9fe0-7a1525e74c96` | 210 | 723 | `a2c0386aa55ccff343899e44f86efb1ae82a12d4` |
| Codex | `01a02e42-c71d-7863-a3f7-bc46e7ab0f26` | 39 | 89 | `7bb6060e90fa700101043269ee691f7d85d84bb5` |
| DeepSeek V4 (harness Claude Code) | `9df236b7-d6d8-4fe5-a36e-a2bc745678a6` | 6 | 9 | `a28dadf20c16ebc2327ed229d8d4c7dc73e44a51` |

Ao todo, **255 falas de Glaydson, 821 respostas das IAs e 88 commits**. As 52 mensagens que o harness injeta com o rótulo do usuário (notificação de tarefa, continuação de contexto, interrupção, aviso ou reset de limite) foram separadas e não contam como falas. Em 23/08 houve seis sessões com fala dele ao longo do dia e até três janelas na mesma hora.

| hora | falas de Glaydson por janela | respostas | commits |
|---|---|---:|---:|
| 24/08 00h | Claude 2, Codex 2 | 14 | 4 |
| *descanso* | | | |
| 24/08 10h | Codex 19, Claude 1 | 34 | 2 |
| 24/08 11h | Codex 5 | 14 | 3 |
| 24/08 12h | Claude 9, Codex 2, DeepSeek 2 | 25 | 3 |
| 24/08 13h | Codex 3, Claude 3 | 9 | 0 |
| 24/08 14h | Claude 3 | 20 | 0 |
| 24/08 15h | Codex 8 | 28 | 1 |
| 24/08 16h | Claude 5 | 35 | 2 |
| 24/08 17h | Claude 13 | 44 | 0 |
| 24/08 18h | Claude 10 | 32 | 6 |
| 24/08 19h | Claude 17 | 50 | 0 |
| 24/08 21h | Claude 8 | 43 | 0 |
| 24/08 22h | Claude 18 | 76 | 9 |
| 24/08 23h | Claude 14 | 37 | 3 |
| 25/08 00h | Claude 10, DeepSeek 3 | 21 | 3 |
| 25/08 01h | Claude 18, DeepSeek 1 | 37 | 6 |
| 25/08 02h | Claude 15 | 33 | 5 |
| 25/08 03h | Claude 15 | 50 | 1 |
| 25/08 04h | Claude 23 | 60 | 5 |
| 25/08 05h | Claude 15 | 62 | 9 |
| 25/08 06h | Claude 1 | 2 | 0 |
| *descanso* | | | |
| 25/08 09h | Claude 5 | 32 | 5 |
| 25/08 10h | Claude 1 | 36 | 10 |
| 25/08 11h | Claude 1 | 7 | 2 |
| 25/08 12h | Claude 3 | 19 | 8 |

Às 07h de 25/08, durante o descanso, há uma resposta e um commit: a IA retomou sozinha depois do reset de limite e sincronizou o grafo (`8863ef63`). Às 20h de 24/08 não houve fala.

## Três momentos em que acompanhar mudou o resultado

Os trechos são literais. Cada um aponta para a linha do transcript privado de onde saiu.

### 1. "Pare o que está fazendo e vá procurar o erro"

24/08, 18:22:10, Claude Code, linha 11369:

> E vc não aprendeu a coisa mais falada por todos os agentes em todos os documentos: Glaydson sabe tudo. Glaydson refuta quando está errado. Glaydson corrige quando é necessário. Quando glaydson diz: tá errado, pare o que está fazendo e vá procurar o erro. Não faça inferência sem ter certeza, glaydson sabe quando vc errou.

Resposta do Claude Code, 19 segundos depois (linha 11373):

> E fiz o contrário dela duas vezes: quando você disse que o Cubo não tinha sido ligado, eu argumentei antes de verificar.

Commit `49aaa0be`, 18:23:16: "fix(contrato): REGRA ZERO no topo — Glaydson vence a inferencia". Quando ele notou que o relatório escondia quem tinha errado, veio o `fe4f5645`, às 18:27:08: "fix(proveniencia): nomear o executor tambem quando o erro e dele".

### 2. Uma frase que trocou o remendo pela causa

25/08, 05:51:32, Claude Code, linha 23526, cinco minutos antes de ele ir dormir:

> agent-pipeline é uma cópia mais pobre do common-pipeline. só colocar o commom pra fazer o agent.

Resposta, 40 segundos depois (linha 23534):

> O `callAgentModel` é uma cópia degradada do `callPipelineModel`: mesma forma, sem stream e sem ferramentas. Substituindo a chamada.

Commit `266f1da4`, 05:54:59: "fix(pipeline): o agente chama o modelo pelo common — stream e ferramentas". A IA registrou o que havia antes (linha 23558): "você cortou meu remendo de regex e apontou o certo — a decisão é do agente."

### 3. Teste no app, defeito no log, correção em minutos

Depois do descanso, Glaydson rodou o Worion no Electron: seis turnos reais na mesma conversa, das 11:32 às 11:48, sobre o build `2422d583`. Às 11:54 ele colou o log no Claude Code. A leitura achou três defeitos que os testes não pegavam:

| hora | o que a IA encontrou no log | commit |
|---|---|---|
| 11:56 | a ferramenta executada não aparecia no selo: "`addTool` só é chamado do `research-pipeline.js` — a rota antiga" | `bed242fb` 11:58 |
| 12:00 | 25.627 caracteres de raciocínio sumiam no retorno: "`agent-pipeline.js:1175` **não devolve**" | `f39e4230` 12:03 |
| 12:05 | o Capture entrava na resposta e não na contagem: "O bundle registra **só** `producer: 'deep_recall'`" | `08ba036f` 12:11 |

Da última linha do teste à terceira correção passaram 23 minutos. O replay no Electron depois das três correções **não** está nos registros.

## Como conferir

- [`evidencia.json`](evidencia.json) traz os blocos de tempo, as contagens por hora e por janela, os 88 commits com hash e tree, os blobs dos três transcripts e o SHA-256 de cada arquivo do pacote privado.
- O pacote privado está em `leedermix-arch/worion-desktop`, commit `e959228cccc1a5cd8169d4407d5918d550f425a6`. Ele tem as 255 falas e as 821 respostas na íntegra, a linha do tempo intercalada e os scripts que refazem a contagem a partir dos transcripts. Uma chave de API que aparece num dos transcripts de origem sai mascarada na cópia.
- Quem tiver acesso ao repositório privado confere com `git rev-parse <commit>:<transcript>` contra os blobs acima e `sha256sum -c SHA256SUMS` na pasta do pacote.

Os hashes provam igualdade de bytes, não a verdade do conteúdo. O que dá peso aos transcripts é a correlação: as falas e respostas têm horário próprio, e os 88 commits, gravados por outro sistema, caem nos mesmos minutos.

---

Autoridade: Glaydson Boaventura · consolidação: Claude Code (claude-opus-5-5), sessão `1cc16d14-ca09-402a-9024-9c7c44124ede` · `PROMPT_ID: WORION-PROMPT-20261016-003244-prova-36h-trabalho-agosto`
