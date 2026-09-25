# Traceweave

> **Verifiable engineering continuity for AI-assisted development.**

**Resume engineering work from evidence, not conversational memory.**

## Featured public evidence

**If you arrived from a publication, start here.**

### 1 — [Agent Self-Report Evidence](research/agent-self-report/README.md)

The main research publication: evidence model, promotion rules, limitations, exemplar cases, provenance, causal lineage, and reproducibility questions.

### 2 — [A Bridge Between Coding CLIs](research/agent-self-report/provenance/codex-claude-cli-bridge.md)

A current operational case on durable coordination between Codex CLI and Claude Code without shared conversational memory.

### 3 — [Proven Governance](traceweave/Governan%C3%A7a%20comprovada/README.md)

The public governance package: dual provenance, independent adversarial audit, and the daily provenance governor.

### More public evidence

- **[Operational Causal Chain](research/agent-self-report/provenance/operational-causal-chain.md)** — from human authority through instruction, execution, lifecycle evidence, Git, readback, and closure.
- **[One Session, Three Participants](research/agent-self-report/provenance/one-session-three-participants.md)** — an audited longitudinal reconstruction of a human-guided, multi-model engineering session.
- **[Traceweave V2 — Causal Continuity Protocol](docs/TRACEWEAVE_V2.md)** — START / RESUME / STOP, content identity, paired publication, destination-native identity, and readback.

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

## Traceweave V2 — causal continuity

Traceweave V2 extends checkpoint verification into a causal continuity model across lifecycle and publication boundaries:

```text
START → RESUME* → STOP → source artifact → causal pair → destination-native identities → readback → closure
```

V2 keeps temporal continuity, content identity, causal pair identity, destination-native identity, and proof of materialization separate. The draft includes Python reference primitives plus a normative JSON Schema under [`traceweave/v2/`](traceweave/v2/).

See [`docs/TRACEWEAVE_V2.md`](docs/TRACEWEAVE_V2.md).

V2 also separates two mechanisms that are often both called “dual provenance”:

```text
independent byte-preserving custody mirror
≠
paired GitHub / Notion publication
```

See [`docs/continuity/DUAL_PROVENANCE_BOUNDARY.md`](docs/continuity/DUAL_PROVENANCE_BOUNDARY.md).

## Current implementation

The repository contains a small Python reference implementation for Git-aware checkpoints and verification.

```bash
pip install -e ".[test]"            # traceweave + tzdata; pytest for the test extra

# inside any Git repository with at least one commit
python -m traceweave checkpoint --executor human --summary "checkpoint created"
# → prints .traceweave/checkpoints/<checkpoint_id>.json

# structural verification (SPEC.md §10, including rule 7)
python -m traceweave verify .traceweave/checkpoints/<checkpoint_id>.json

# plus a reality check of the Git claims against the repository
python -m traceweave verify .traceweave/checkpoints/<checkpoint_id>.json --repo .

# tests — both runners see the whole suite, V2 included
python -m unittest discover -s tests
pytest
```

**See it catch a lie:** `python examples/lie-detection/demo.py` plants four lies an AI agent could
write into a checkpoint and shows which check catches each one ([details](examples/lie-detection/README.md)).

`verify` alone proves the record is well-formed. `--repo` also checks that `head_commit` and
`base_commit` exist, that the base is an ancestor of the head, and that `working_tree` matches the
repository. Those are the claims a hash chain would otherwise seal even when they were false at the
moment of recording. A checkpoint that declares `complete` must carry evidence for every test and a
clean working tree (SPEC.md §10 rule 7).

The implementation is intentionally conservative: local execution, deterministic output, explicit evidence, and no requirement for cloud services or telemetry.

## MCP server — read / write / publish

Traceweave now includes an MCP server that exposes repository evidence and controlled mutation as explicit capabilities:

```text
read    → inspect, search, hash, Git readback
write   → create/replace/append repository files
publish → exact-path commit + non-force push + remote SHA readback
```

See [docs/MCP.md](docs/MCP.md).

## Conduct

Contributors, human or AI agent, follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). It covers conduct
toward people and conduct of evidence: no claim without evidence, and "done" means verified at the
destination.

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

- [Traceweave V2 — Causal Continuity Protocol](docs/TRACEWEAVE_V2.md)
- [Dual provenance boundary](docs/continuity/DUAL_PROVENANCE_BOUNDARY.md)
- [Continuity-first positioning](docs/continuity/TRACEWEAVE_POSITIONING.md)
- [Protocol specification](SPEC.md)
- [Model interoperability recipes](docs/model-interop/README.md)
- [Multi-model prompt pipeline](docs/model-interop/PROMPT_PIPELINE.md)
- [Examples](examples/)

## Status

Traceweave is experimental and evolving. The current reference implementation is intentionally small so the evidence model and verification behavior can be inspected directly.

## License

Apache License 2.0. See [LICENSE](LICENSE).
