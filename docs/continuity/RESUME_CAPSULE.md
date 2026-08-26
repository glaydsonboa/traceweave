# Resume Capsule

## Purpose

Resume Capsule creates a compact, portable technical handoff that preserves verified continuity without copying a chat transcript.

## Problem

Large transcripts are expensive and noisy. Small summaries are easy to hallucinate or oversimplify.

A useful handoff needs to carry goal, verified current state, exact Git revision, completed work, open work, explicit decisions, do-not-reopen constraints, evidence pointers, and the next safe action. It should not depend on hidden conversational history.

## Proposed CLI

```bash
traceweave capsule make
traceweave capsule show
traceweave capsule verify
```

Optional:

```bash
traceweave capsule make --from-checkpoint .traceweave/checkpoints/cp-....json
```

## Artifact

```text
.traceweave/
└── capsules/
    └── capsule-<id>.yaml
```

Proposed schema:

```yaml
version: "0.1"
capsule_id: capsule-...
created_at: 2026-08-26T23:00:00Z

goal: >
  Restore continuity without reopening solved work.

verified_state:
  branch: feature/example
  head_commit: abc123
  working_tree: clean
  checkpoint_id: cp-...

completed:
  - statement: "Identity propagation fixed"
    evidence:
      - "commit:abc123"
      - "test:identity 6/6"

open:
  - statement: "Freeze lexical baseline"
    evidence: []

decisions:
  - "Do not move corpus before baseline"

do_not_reopen:
  - "Do not reintroduce shadow observer"

unknown:
  - "Runtime proof for external artifact persistence"

next_safe_action: "Freeze lexical baseline"
```

## Contract

A capsule is a projection of verified state, not a replacement for the checkpoint that produced it. Statements without evidence remain explicitly unverified. `do_not_reopen` records a decision boundary at the checkpoint; later contradictory evidence can supersede it.

## Verification

`traceweave capsule verify` should check schema validity, checkpoint existence when referenced, Git revision format, evidence pointer shape, and whether repository drift occurred after the capsule was created.

Drift does not rewrite the capsule. It is reported separately so the historical boundary remains stable.

## Relationship to Traceweave

```text
checkpoint = factual technical record
capsule    = compact handoff projection
```

The checkpoint preserves the evidence boundary. The capsule makes that boundary portable to the next executor or session.
