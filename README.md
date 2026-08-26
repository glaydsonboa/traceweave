# Traceweave

> **Verifiable engineering continuity for AI-assisted development.**

**Resume engineering work from evidence, not conversational memory.**

Traceweave is a protocol and tooling project for preserving recoverable technical state across development sessions. It links checkpoints to exact Git state, explicit test evidence, provenance, open work, and structural synchronization without requiring a model to remember the previous conversation.

It works with one CLI, several coding agents, or a human-only workflow.

## The problem

AI-assisted development creates state across human intent, execution, tests, Git, generated artifacts, documentation, checkpoints, and open decisions.

A later session may know what was discussed while still being unable to verify:

- what was actually completed;
- which commit represents it;
- which tests really ran;
- what remains open;
- whether the repository changed after the last verified checkpoint;
- whether derived artifacts still represent the current source state.

Traceweave treats those questions as engineering state rather than memory prompts.

## Core principle

> **A technical session should be recoverable from evidence instead of conversational memory.**

Unknown is a valid state. If a test result, provenance field, or synchronization state was not observed, Traceweave should preserve that uncertainty instead of promoting it to a fact.

## Core loop

```text
session start
    ↓
recover last verified checkpoint
    ↓
inspect current Git / structural state
    ↓
perform bounded work
    ↓
validate
    ↓
record Git / evidence
    ↓
checkpoint
    ↓
session stop
```

The underlying protocol remains:

```text
session → provenance → execution → tests → Git → structural state → checkpoint
```

## Current implementation

The repository contains a small Python reference implementation for Git-aware checkpoints and verification.

```bash
python -m traceweave checkpoint \
  --session-id demo-session \
  --executor human \
  --tests passed \
  --structural-state synced \
  --note "checkpoint created"

python -m traceweave verify
```

The implementation is intentionally conservative: local execution, deterministic output, explicit evidence, and no requirement for cloud services or telemetry.

## Continuity-first direction

The next public proof is a two-session continuity workflow:

```bash
traceweave stop
traceweave resume
```

`stop` records a compact verified boundary. `resume` compares that boundary with the repository as it exists now and reports drift, completed work, open work, and unknown evidence.

The project is also exploring small adjacent tools that preserve the same evidence-first contract:

- **Resume Capsule** — portable technical handoff without copying a transcript.
- **Causal Commit Guard** — separate current causal work from unrelated repository changes.
- **Stale Artifact Guard** — detect generated artifacts that no longer match the source revision they claim to represent.
- **Header Contract Linter** — validate structural source-header contracts without pretending to understand semantics it cannot prove.

## Design principles

1. Evidence beats memory.
2. Unknown is a valid state.
3. Git state must be exact.
4. Tests are facts only when observed.
5. Resume should reconcile, not narrate.
6. Generated artifacts should declare the source state they represent.
7. Small deterministic tools should prove each contract independently.

## Documentation

- [Continuity-first positioning](docs/continuity/TRACEWEAVE_POSITIONING.md)
- [Protocol specification](SPEC.md)
- [Examples](examples/)

## Status

Traceweave is experimental and evolving. The current reference implementation is intentionally small so the evidence model and verification behavior can be inspected directly.

## License

Apache License 2.0. See [LICENSE](LICENSE).
