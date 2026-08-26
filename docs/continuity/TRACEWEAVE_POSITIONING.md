# Traceweave — Continuity-First Positioning

## One-line description

> **Traceweave preserves verifiable engineering continuity across AI-assisted development sessions.**

Secondary line:

> Works with one CLI, several agents, or a human-only workflow.

## Why reposition

The original wording emphasizes coding agents and multi-model workflows. That remains a supported use case, but it is not necessary to prove the core idea.

The stronger and simpler claim is:

> A technical session should be recoverable from evidence instead of conversational memory.

That claim can be demonstrated with one person, one repository and one coding CLI across two sessions.

## Problem

AI-assisted development creates technical state across several layers:

- human intent;
- execution;
- tests;
- Git;
- derived artifacts;
- documentation;
- checkpoints;
- open decisions.

A later session may know what was discussed while still being unable to answer:

- What was actually completed?
- Which commit represents it?
- Which tests really ran?
- What remains open?
- Did the repository change after the last verified checkpoint?
- Is a structural/index artifact still aligned with the Git revision it claims to represent?

Traceweave treats those questions as engineering state, not memory prompts.

## Core loop

```text
session start
    ↓
recover last verified checkpoint
    ↓
inspect current Git/structural state
    ↓
perform bounded work
    ↓
validate
    ↓
record Git/evidence
    ↓
checkpoint
    ↓
session stop
```

## Core protocol

Traceweave remains the protocol layer:

```text
session → provenance → execution → tests → Git → structural state → checkpoint
```

The protocol should continue to require:

- explicit session identity;
- explicit or null provenance;
- explicit test status;
- exact Git state;
- no unsupported promotion of claims to facts;
- explicit structural synchronization state when applicable.

## Product boundary

Traceweave is not an orchestration framework.

It does not need to choose models, route tasks, run autonomous swarms or own an editor.

Its job is narrower:

> preserve and verify the technical boundary between one execution context and the next.

## Public proof

The smallest convincing proof is a two-session continuity demo:

1. create a repository state;
2. record a verified checkpoint;
3. change the repository after the checkpoint;
4. start a new session;
5. recover the checkpoint;
6. compare checkpoint Git state to current Git state;
7. report completed/open work and drift;
8. refuse to invent missing evidence.

## Language

Preferred language:

- verifiable continuity;
- evidence-backed checkpoint;
- recoverable session state;
- Git-aware resume;
- explicit unknown state;
- deterministic handoff;
- inspectable provenance.

Avoid claims that imply more than the tool proves.

## Design principles

1. Evidence beats memory.
2. Unknown is a valid state.
3. Git state must be exact.
4. Tests are facts only when observed.
5. Resume should reconcile, not narrate.
6. Generated artifacts must declare what source state they represent.
7. Small deterministic tools should prove each contract independently.
8. Public tooling should keep protocol boundaries explicit and independently verifiable.
