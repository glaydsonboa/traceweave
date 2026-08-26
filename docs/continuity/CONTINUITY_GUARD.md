# Continuity Guard

## Purpose

Continuity Guard answers one question:

> **Can a technical session resume from the last verified state without depending on the model remembering the previous conversation?**

This is the first adjacent tool because it directly proves Traceweave's strongest near-term value.

## Problem

A coding session ends after commits, tests and decisions. The next session often begins with a large transcript or narrative handoff. Narratives drift.

A resume mechanism should instead determine the last verified checkpoint, the Git revision represented by it, what was completed, what remained open, what changed since the checkpoint, whether the working tree is clean or dirty, and the smallest safe next action.

## Non-goals

Version 0.1 should not call an LLM, summarize arbitrary transcripts, run tests automatically, mutate Git, checkout/reset/rebase, resolve open decisions, infer provenance, or require cloud services.

## Proposed CLI

```bash
traceweave stop \
  --summary "Restore identity contract in agent route" \
  --executor "Claude Code" \
  --open "Freeze lexical continuity baseline"

traceweave resume
```

Optional:

```bash
traceweave status
traceweave verify
```

## `stop` behavior

`traceweave stop` records a compact session boundary.

```text
.traceweave/
├── session.json
├── checkpoints/
│   └── cp-<id>.json
└── latest.json
```

Minimum fields:

```json
{
  "version": "0.1",
  "checkpoint_id": "cp-...",
  "created_at": "ISO-8601",
  "summary": "what was completed",
  "open_items": ["what remains open"],
  "git": {
    "branch": "main",
    "base_commit": "abc",
    "head_commit": "def",
    "working_tree": "clean"
  },
  "tests": [{"command": null, "result": "not_run", "evidence": null}],
  "provenance": {
    "requested_by": null,
    "prompt_generator": null,
    "executor": {"type": null, "name": "Claude Code"}
  },
  "artifacts": [],
  "next_safe_action": "Freeze lexical continuity baseline"
}
```

Unknown values remain `null`.

## `resume` behavior

`traceweave resume` reads the latest checkpoint and current Git state.

```text
CONTINUITY RESUME

Last checkpoint
  id:        cp-20260826-230100-a31c
  branch:    feature/example
  last HEAD: 82aa7f1
  status:    partial

Current repository
  HEAD:      91bb230
  tree:      dirty
  drift:     yes

Completed at checkpoint
  ✓ restore identity contract in agent route

Still open
  ○ freeze lexical continuity baseline

Changed since checkpoint
  ! src/router.js
  ! docs/state.md

Next safe action
  → inspect drift before starting new work
```

## Drift classification

Version 0.1 can classify `none`, `commits_after_checkpoint`, `working_tree_changed`, `branch_changed`, and `unknown`.

It should never say "safe to continue" merely because a checkpoint exists.

## Verification rules

A valid resume must verify that the checkpoint exists and is parseable, records branch/base/head, current Git state is inspectable, differences are explicitly reported, unknown test state remains unknown, and open items are not silently promoted to completed.

## MVP acceptance test

```bash
git init
echo one > app.txt
git add app.txt
git commit -m init
traceweave stop --summary "Initial state" --executor "human" --open "Add validation"

echo two >> app.txt
git add app.txt
git commit -m "change app"
traceweave resume
```

The tool must report checkpoint HEAD, current HEAD, drift, the open item, and no invented test result.

## Why this proves Traceweave

```text
session A ends
→ state is captured
→ repository changes
→ session B reconstructs the verified boundary correctly
```

Continuity Guard should use Traceweave checkpoints directly rather than duplicating protocol concepts.
