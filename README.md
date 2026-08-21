# Traceweave

> **Verifiable continuity and provenance for AI coding agents.**

Traceweave is a protocol and tooling direction for preserving continuity across AI-assisted coding sessions by linking session state, provenance, technical checkpoints, Git history, execution evidence and structural code-graph synchronization.

AI coding sessions frequently lose operational context between executions. Reports, commits, prompts, transcripts and structural state can diverge. Traceweave treats that continuity as an engineering problem rather than relying on conversational memory alone.

## Problem

Long-running AI-assisted software engineering creates state across multiple layers: human intent, prompts, model actions, tool execution, tests, Git history and structural representations of the codebase.

When those layers drift apart, a later agent or session may know *what was said* without being able to verify *what actually happened*.

Traceweave is designed to make that operational history inspectable and recoverable.

## Approach

The core continuity loop is:

```text
session → provenance → execution → tests → Git → graph synchronization → checkpoint
```

Instead of treating a chat transcript or commit as sufficient evidence, Traceweave connects execution state to verifiable artifacts and explicit checkpoints.

## Architecture

A Traceweave workflow is organized around a small set of contracts:

1. **Session start** — recover the last verified technical state before new work begins.
2. **Provenance** — preserve the chain between human intent, model reasoning context, executor actions and resulting mutations.
3. **Execution evidence** — record relevant commands, tests and outcomes rather than relying only on generated summaries.
4. **Git linkage** — associate verified work with repository state and commits.
5. **Graph synchronization** — keep structural code representations aligned with verified Git changes.
6. **Checkpoint** — leave a compact, inspectable state for the next session or agent.

## Core ideas

- session start and stop contracts
- human / model / executor provenance
- Git-linked execution evidence
- sanitized session transcripts
- checkpointed technical journals
- code-graph synchronization
- push guards against stale structural state

## Provenance model

A canonical execution chain can be represented as:

```text
human → prompt-generating AI → executing AI/CLI → mutation → test → commit → evidence
```

The goal is not to preserve every token produced by an AI system. The goal is to preserve enough evidence to establish where a change came from, what executed it, how it was validated and which repository state resulted from it.

## Example lifecycle

```text
START SESSION
    ↓
Recover last checkpoint
    ↓
Inspect Git + structural state
    ↓
Define bounded change
    ↓
Execute
    ↓
Validate / test
    ↓
Commit verified state
    ↓
Synchronize code graph
    ↓
Write checkpoint
    ↓
STOP SESSION
```

## Key properties

**Verifiable** — conclusions should be backed by execution evidence.

**Git-aware** — continuity is tied to concrete repository state rather than narrative memory alone.

**Agent-compatible** — the protocol is intended for workflows involving coding agents, CLIs and multiple models.

**Inspectable** — orchestration and provenance should remain understandable to a human operator.

**Minimal-impact** — agents should determine the smallest safe change path before mutation when structural information is available.

## Engineering principles

- Evidence before conclusion.
- Minimal-impact changes.
- Provenance is part of the implementation.
- Runtime behavior outranks documentation.
- Security must preserve operational continuity.
- A commit is not proof until the resulting system is verified.
- AI orchestration must remain inspectable.

## Status

**Prototype / early specification.**

Traceweave currently describes an engineering direction and protocol. Interfaces, schemas and reference tooling will evolve as reproducible implementations are published.

It should not be interpreted as production-ready software at this stage.

## Reference implementation — version 0.1

A minimal, inspectable CLI that implements the protocol above. It is intentionally
small: Python standard library only, no dependencies, no daemon, no database, no
network calls.

### Installation

```bash
git clone https://github.com/glaydsonboa/traceweave.git
cd traceweave
python -m pip install -e .
```

Requires Python 3.11+ and a local Git installation.

### Usage

Inside any Git repository:

```bash
traceweave checkpoint \
  --summary "Add configuration validation" \
  --executor "DeepSeek"
```

This inspects the repository with read-only Git commands and writes a checkpoint to:

```text
.traceweave/checkpoints/<checkpoint_id>.json
```

The first checkpoint also creates the session record at `.traceweave/session.json`;
later checkpoints reuse the same session and base commit.

Supported options:

| Option | Meaning |
|---|---|
| `--summary` | one-line description of the work performed |
| `--executor` | human, CLI, agent or model that performed the work (required by SPEC.md §2) |
| `--requested-by` | who or what requested the work |
| `--prompt-generator` | who or what generated the instruction |
| `--session-id` | stable session identifier (default: auto-created and persisted) |
| `--base-commit` | commit from which the session started (default: session base or current HEAD) |
| `--graph-status` | `unknown` (default) or `not_applicable` — `synced`/`stale` are reserved for a future graph integration |
| `--path` | repository path to inspect (default: current directory) |

Any provenance option that is not provided is recorded as `null` — never inferred
from Git username, commit author, environment variables or repository metadata.

Provenance names are the explicit values supplied on the command line. The CLI
never infers an actor type or a causal role from a name: each provenance link
records `{"type": null, "name": "<explicit name>"}` and no `chain` field is
generated.

Verify a checkpoint:

```bash
traceweave verify .traceweave/checkpoints/<checkpoint_id>.json
```

Exits `0` when the checkpoint passes, non-zero when it fails. Verification covers:
session and checkpoint ids, `base_commit`/`head_commit`, explicit test results,
explicit-or-null provenance links, and `graph_sync.source_commit == git.head_commit`
whenever `graph_sync.status` is `synced`.

### What version 0.1 intentionally does not do

- it does **not** commit, push, checkout, reset, clean or rebase — only read-only Git commands;
- it does **not** collect secrets, tokens, environment variable values, transcripts or arbitrary file contents;
- it does **not** integrate Graphify — `graph_sync` supports only `not_applicable` and `unknown` (default);
- it does **not** ingest test results automatically — when no test was run, `tests` is one explicit entry `{"command": null, "result": "not_run", "evidence": null}`, never an invented pass;
- generated checkpoints default to `"status": "partial"` — the CLI does **not** promote a checkpoint to `complete` without sufficient evidence (all `complete`/`partial`/`blocked` values from SPEC.md remain supported by the protocol);
- it does **not** make network requests or send telemetry.

### Minimal runnable example

```bash
mkdir /tmp/tw-demo && cd /tmp/tw-demo
git init -q && git config user.email demo@example.com && git config user.name Demo
echo "config" > app.txt && git add . && git commit -qm init

traceweave checkpoint \
  --summary "Add configuration validation" \
  --executor "DeepSeek" \
  --requested-by "Glaydson" \
  --prompt-generator "ChatGPT"

traceweave verify .traceweave/checkpoints/*.json
```

## Limitations

- The protocol and artifact schemas are not yet stable.
- The version 0.1 reference implementation is minimal — tests are not auto-ingested and graph integration is absent by design.
- Code-graph integration depends on the structural tooling used by a project.
- Provenance quality ultimately depends on what executors and surrounding infrastructure can observe and record.

## Roadmap

- Define the minimal session/checkpoint schema.
- Publish a reference directory and journal format.
- Define Git-linked provenance records.
- Add an executable session start/stop example.
- Demonstrate code-graph synchronization after verified changes.
- Add validation and stale-state guards.
- Publish a reproducible end-to-end example.

## License

Licensed under the [Apache License 2.0](LICENSE).
