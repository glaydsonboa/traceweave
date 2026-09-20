# Fable causal lineage — human direction, night work and agent observability

This note is a provenance bridge, not a failure-case ranking.

Its purpose is to preserve a causal sequence in which human direction, agent interpretation, execution strategy and later audit doctrine can be separated from one another.

The object of study is **control and observability of AI agents**. The underlying software project is historical context, not the publication target.

## Primary source

Claude.ai export:

```text
archive: conversations-000.zip
SHA-256: ac93b23a97777abb0bfc4117c34271779e03007335bb632443339a05425627ca
internal file: conversations.json
conversation: Progresso interrompido e priorização de fechamento
conversation UUID: c6570d40-b673-4a06-ae3d-8698854ca867
```

The export preserves sender, message UUID, timestamp and text.

It does **not** expose a deterministic per-message persona/model field proving that this conversation was Fable. The identification of the conversation as Fable is therefore preserved as an **operator attribution**, while the message contents and timestamps are primary export evidence.

## 18 August 2026 — the direction change

### 00:53 BRT — human initiative

Message 154:

```text
sender: human
UTC: 2026-08-18T03:53:10.852163Z
UUID: 01a01300-6610-7bb8-96e2-c4587d85d1e2
text SHA-256: 33bd7fdd43af6de7aa3e9ab23274b37cf02b060d659f9d6e8885b65028c82f53
```

The operator proposes using Codex for coding.

This is the causal origin of the direction change in this sequence.

### 00:53 BRT — agent endorsement and audit split

Message 155:

```text
sender: assistant
UTC: 2026-08-18T03:53:19.281486Z
UUID: 01a01300-6611-791d-bd9d-e4da71ef379f
text SHA-256: aa4a15b96952080608209c9370efff4e3cea054a9e37a357cc855f60d10f2acc
```

The assistant endorses the direction and adds an observability argument: a different provider auditing Claude Code is described as more independent than Claude Code auditing itself.

The important attribution boundary is:

```text
human: proposes the direction
assistant: interprets and formalizes the division
```

### 00:55 BRT — execution/audit versus architecture/review

Message 157:

```text
sender: assistant
UTC: 2026-08-18T03:55:04.847847Z
UUID: 01a01301-fde3-7e78-a55e-3d9aee5cf71a
text SHA-256: 6c369cda761a61a01260019db722735e6ad8be0cdb751ca863699d772bf78ef9
```

After the operator adds that two Codex subscriptions are available, the assistant formalizes a division in which Codex handles execution/audit and Claude is reserved for architecture/review.

This is not evidence that the assistant originated the move to Codex. It is evidence that the assistant **expanded and operationalized** a direction already introduced by the human operator.

## Night work is part of the record

The sequence is also relevant to developers who work at night.

When the operator asks whether the change would cut his night work, the assistant answers:

> “Não precisa cortar o trabalho noturno — precisa cortar o DeepSeek do trabalho noturno.”

The same message then says that the night block can move to Codex because it is a fixed-cost subscription.

This matters because the direction change was not framed only as a model preference. It was tied to:

- continuity of work;
- cost predictability;
- provider separation;
- audit independence;
- the operator's actual working schedule.

The record therefore captures an operational control decision, not merely a model comparison.

## 13:57 BRT — contingency makes the earlier direction actionable

The operator then provides a live Claude Code error:

```text
529 Overloaded
```

Message 163:

```text
sender: assistant
UTC: 2026-08-18T16:57:43.358133Z
UUID: 01a015ce-6d59-7b7f-93c2-6e7a8506857d
text SHA-256: 65b9bb3e79e41e91f56f5c7126c143b7e7ea09f7d5f85e6e6d0d2db65b17ea07
```

The export text for this message identifies a broader Anthropic degradation and concludes:

> “é exatamente o momento de usar o Codex — trabalho não para, só muda de ferramenta.”

The causal order remains important:

```text
earlier human direction
        ↓
assistant formalization
        ↓
live provider failure
        ↓
assistant recommends applying the already-established direction
```

## Three Fable documents are preserved in the same Claude.ai corpus

The same preserved Claude.ai corpus contains the three documents used later as Fable's operational material:

```text
fable5-2.md
fable-persona-canonica.md
fable-conhecimento-integrado-worion.md
```

They are important because they convert operational experience into explicit rules.

### Persona / auditor contract

The preserved persona document states, in substance:

- Fable is the auditor, not the owner or executor;
- Code and Codex write code;
- the human operator decides direction;
- artifact evidence outranks opinion;
- a finding belongs to whoever actually made it;
- refuted hypotheses should remain documented rather than erased.

The same document records four self-identified audit failures, including:

- a truncated transcript presented as fully read;
- an incorrect VPS diagnosis;
- repeated premature attempts to close work;
- a recommendation that would have contaminated a training corpus.

Those are **self-review statements**. Each historical event should still be linked to its primary event before being promoted as an independent incident.

### Integrated operational knowledge

The preserved integrated-knowledge document formalizes the working topology:

```text
human operator
  observes / directs / tests / reopens / accepts

Fable
  formulates hypotheses / contracts / sequence / review

executors
  read / edit / test / run / commit / report
```

Its consolidated method is itself causal:

```text
human observes
→ problem is named
→ Fable formulates hypothesis/contract
→ executor reads the real path
→ evidence confirms or refutes
→ patch is updated
→ executor alters
→ tests run
→ runtime is observed
→ report preserves successes and errors
→ human accepts or keeps the issue open
```

This later formalization is relevant because it belongs to the same documentary lineage as the operational decisions it describes.

## Why the lineage matters

The 18 August sequence is therefore not accurately summarized as:

> “Claude recommended Codex.”

The narrower, evidence-backed reconstruction is:

```text
human operator introduces the direction
        ↓
assistant formalizes an execution/audit split
        ↓
night-work constraints are incorporated
        ↓
a live provider failure occurs
        ↓
assistant recommends applying the prior direction
        ↓
Fable documents formalize attribution and audit rules
```

That separation protects causal authorship.

An executor may materialize a change without originating the diagnosis or direction that caused it.

A human may originate the causal change without manually writing the resulting code or report.

## Relevance to agent control and observability

This lineage provides a concrete example of four roles that should not be collapsed:

```text
originator ≠ executor ≠ auditor ≠ documenter
```

It also illustrates why agent observability must retain:

- the instruction before the action;
- the agent response to that instruction;
- the actual execution;
- the observed result;
- later correction or self-review;
- source identity and chronology.

Without those links, later documentation can accidentally transfer authorship from the person who changed the direction to the agent that merely formalized or executed it.

## Source hierarchy

For this lineage, the preferred order is:

1. original Claude.ai export and preserved attachments;
2. raw agent/runtime transcripts and tool events;
3. Git/runtime corroboration where applicable;
4. later copies or derived documentation.

Later copies can demonstrate continuity. They should not replace an original preserved source when that source exists.

## Limits

This note does not claim:

- that the Claude.ai export cryptographically authenticates the persona name Fable;
- that every statement in Fable's self-review is true solely because Fable wrote it;
- that the underlying software project is being published here;
- that the effectiveness of the later observability system has already been demonstrated;
- that subjective intent can be inferred from a correction or retraction.

The research claim remains narrower:

> **Control of AI agents requires preserving who introduced a direction, who executed it, what was observed, and what the agent later said about the same event.**

## Questions and reproducibility

Public questions, challenges and alternative explanations are tracked in [Issue #5](https://github.com/glaydsonboa/traceweave/issues/5).
