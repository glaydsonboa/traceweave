# Traceweave Protocol — Minimal Specification

> **Traceweave** is a lightweight protocol for preserving verifiable continuity across AI-assisted coding sessions.

This specification defines the smallest useful unit of Traceweave: a **session** that produces one or more **checkpoints** containing provenance, execution evidence, Git state, and code-graph synchronization state.

The protocol does not require a specific AI model, CLI, Git host, or graph engine.

## 1. Core idea

A coding session should be reconstructable from evidence instead of memory.

Minimal chain:

`session start → provenance → execution → test → Git state → graph sync → checkpoint`

A valid checkpoint answers five questions:

1. What session is this?
2. Who or what caused the work?
3. What changed and what was tested?
4. What Git state represents the result?
5. Is the structural graph synchronized with that Git state?

## 2. Session

A **session** is one bounded period of technical work performed by a human, an AI coding agent, or a combination of both.

Minimum session fields:

| Field | Required | Meaning |
|---|---:|---|
| `session_id` | yes | Stable unique identifier for the session |
| `started_at` | yes | ISO 8601 timestamp |
| `executor` | yes | Human, CLI, agent, or model that performed the work |
| `repository` | yes | Repository being modified |
| `branch` | yes | Git branch used for the work |
| `base_commit` | yes | Commit from which the session started |

A session may contain multiple checkpoints.

## 3. Checkpoint

A **checkpoint** is an immutable factual snapshot of the session at a meaningful boundary.

Typical checkpoint moments:

- after a coherent change;
- after tests;
- after a commit;
- before handoff;
- before stopping a long session.

A checkpoint MUST record:

- session identity;
- provenance;
- work performed;
- tests and their result;
- Git state;
- graph synchronization state.

A checkpoint MUST NOT claim success for evidence that was not observed.

## 4. Provenance

**Provenance** records the causal chain behind the work.

Minimal provenance chain:

`human → prompt generator → executor → change`

Any link that did not exist MUST be represented as `null`, not invented.

Recommended structure:

```json
{
  "requested_by": {"type": "human", "name": "Example User"},
  "prompt_generator": {"type": "ai", "name": "ChatGPT"},
  "executor": {"type": "ai_cli", "name": "Codex CLI"}
}
```

Traceweave distinguishes request authority, prompt authorship, execution authorship, and evidence.

## 5. Work record

A checkpoint SHOULD list the smallest useful factual description of the work.

```json
{
  "summary": "Add input validation to the config loader.",
  "files_changed": [
    "src/config.js",
    "tests/config.test.js"
  ]
}
```

Do not copy an entire transcript into the checkpoint. The checkpoint is an index of verifiable facts, not a conversation archive.

## 6. Tests

Each test entry records:

- command;
- result;
- optional evidence.

Allowed result values:

- `passed`
- `failed`
- `not_run`

A checkpoint with failed tests is still valid. Traceweave records state; it does not rewrite failure as success.

## 7. Git state

**Git state** identifies the exact repository revision associated with the checkpoint.

```json
{
  "branch": "feature/config-validation",
  "base_commit": "2f1a83c",
  "head_commit": "7c91b4e",
  "working_tree": "clean"
}
```

Allowed `working_tree` values:

- `clean`
- `dirty`
- `unknown`

If no commit was created yet, `head_commit` MAY equal `base_commit`.

## 8. Graph sync

**Graph sync** records whether the structural code graph corresponds to the checkpoint's Git state.

Minimal states:

- `synced`
- `stale`
- `not_applicable`
- `unknown`

Example:

```json
{
  "status": "synced",
  "engine": "graphify",
  "source_commit": "7c91b4e",
  "verified_at": "2026-08-21T19:43:00Z"
}
```

For `synced`, `source_commit` MUST identify the same revision represented by `git.head_commit`, unless the implementation explicitly documents why it differs.

## 9. Minimal checkpoint object

```json
{
  "traceweave_version": "0.1",
  "checkpoint_id": "cp-...",
  "session": {},
  "provenance": {},
  "work": {},
  "tests": [],
  "git": {},
  "graph_sync": {},
  "status": "complete"
}
```

Minimal checkpoint status values:

- `complete`
- `partial`
- `blocked`

`complete` means the checkpoint contains the evidence required by the current session boundary. It does not mean the entire project is finished.

## 10. Verification rules

A minimal Traceweave consumer can verify a checkpoint with these rules:

1. `session_id` and `checkpoint_id` exist.
2. `base_commit` and `head_commit` are recorded.
3. Every claimed test has an explicit result.
4. Every changed file is listed.
5. Provenance links are explicit or `null`.
6. If `graph_sync.status == "synced"`, the graph revision matches the Git revision being claimed.
7. No unsupported claim is promoted to fact.

## 11. What version 0.1 does not define

Version `0.1` intentionally does not define:

- a database;
- a daemon;
- a GitHub App;
- a specific AI provider;
- a graph format;
- a transcript format;
- a cloud service.

The minimal protocol only defines enough structure for one session to leave a verifiable continuity record.

## 12. Example

See:

- [`examples/checkpoint.json`](examples/checkpoint.json)
- [`examples/session-flow.md`](examples/session-flow.md)
