# Traceweave Protocol — Public Specification

> **A public protocol for evidence-governed continuity and provenance in AI-assisted software engineering.**

## 0. Scope

This document defines the **open semantics** of Traceweave.

It defines how public Traceweave artifacts should represent identity, provenance, evidence, Git state, checkpoints and verification.

It does **not** require publication of a production engine, orchestration system, graph implementation, private adapter or commercial capability.

The Python code currently published in this repository is a limited **Reference Demonstration v0.1**. It implements only a subset of this public specification.

## 1. Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** are used in their ordinary specification sense.

The central normative rule is:

> **A Traceweave artifact MUST NOT promote an unobserved claim to fact.**

Corollaries:

- unknown is not false;
- absent evidence is not negative evidence by default;
- a report is not proof merely because it says “resolved”;
- a commit is not proof of runtime acceptance;
- a checkpoint is not a delivery certificate.

## 2. Core model

A technical session should be reconstructable from evidence rather than memory alone.

Minimal conceptual chain:

```text
request
→ instruction
→ execution
→ observed evidence
→ repository state
→ checkpoint
```

A deployment may add more identity links, for example:

```text
request_id
→ prompt_id
→ execution_id
→ evidence_id
→ checkpoint_id
→ delivery_proof_id
```

An implementation MAY use different identifier names, but identities MUST remain stable enough to reconstruct causal relationships.

## 3. Roles and authorship

Traceweave distinguishes roles that are often incorrectly collapsed.

Recommended roles:

| Role | Meaning |
|---|---|
| `requested_by` | authority that requested the work |
| `intellectual_author` | originator of the method, design or decision when known |
| `prompt_generator` | actor that formulated an instruction or prompt |
| `executor` | actor that performed the technical work |
| `verifier` | actor/process that checked evidence |
| `publisher` | actor/process that published the artifact |

Rules:

1. An `executor` MUST NOT be inferred to be the `intellectual_author`.
2. A `prompt_generator` MUST NOT be inferred to be the originator of the underlying idea.
3. A missing role MUST be represented as `null` or omitted according to the schema; it MUST NOT be invented.
4. A public artifact SHOULD preserve attribution when the underlying evidence supports it.

See `docs/principles/AUTHORSHIP_AND_PROVENANCE.md`.

## 4. Session

A **session** is a bounded period of technical work.

Recommended minimum fields:

| Field | Required | Meaning |
|---|---:|---|
| `session_id` | yes | stable session identifier |
| `started_at` | yes | ISO 8601 timestamp |
| `executor` | yes | explicitly declared executor |
| `repository` | yes | repository or project identifier |
| `branch` | yes | branch/ref at session start |
| `base_commit` | yes | starting Git revision |

A session MAY contain multiple checkpoints.

## 5. Checkpoint

A **checkpoint** is an immutable factual snapshot of observed technical state at a meaningful boundary.

Typical boundaries:

- after a coherent change;
- after a test;
- after a commit;
- before a handoff;
- before a session ends;
- after a verified external delivery event.

A checkpoint MUST distinguish:

- observed facts;
- unknown state;
- claims that were not tested;
- unresolved or blocked work.

A checkpoint MUST NOT claim that work is complete merely because an executor stopped.

## 6. Checkpoint status

Public status values SHOULD include:

- `complete`
- `partial`
- `blocked`

Interpretation:

### `complete`

The evidence required by **that checkpoint boundary** is present.

It does not mean the project, feature or deployment is globally finished.

### `partial`

Useful evidence exists, but one or more required facts are missing or unverified.

### `blocked`

Work cannot proceed or cannot be verified under the current conditions.

## 7. Provenance

Provenance records causal participation.

Example:

```json
{
  "requested_by": {"type": "human", "name": "Example User"},
  "intellectual_author": {"type": "human", "name": "Example Author"},
  "prompt_generator": {"type": "ai", "name": "Example Assistant"},
  "executor": {"type": "ai_cli", "name": "Example CLI"},
  "verifier": {"type": "process", "name": "test-suite"}
}
```

Values MUST be explicit observations or explicit declarations.

Implementations MUST NOT infer a person's role from:

- Git username;
- commit author;
- machine username;
- environment variable;
- repository owner;
- model name alone.

## 8. Work record

A checkpoint SHOULD describe the smallest useful factual unit of work.

Example:

```json
{
  "summary": "Add validation for a required configuration value.",
  "files_changed": [
    "src/config.py",
    "tests/test_config.py"
  ]
}
```

The work record is an index of evidence, not a transcript archive.

Sensitive/private content SHOULD NOT be copied into a public checkpoint when a sanitized pointer is sufficient.

## 9. Tests and runtime evidence

Each test or runtime observation SHOULD record:

- what was executed or observed;
- result;
- optional evidence reference;
- timestamp when useful.

Allowed minimal test results:

- `passed`
- `failed`
- `not_run`

`not_run` is a valid factual result.

An implementation MUST NOT substitute `passed` for `not_run`.

## 10. Git state

Git state identifies the repository revision represented by the checkpoint.

Example:

```json
{
  "branch": "feature/config-validation",
  "base_commit": "2f1a83c",
  "head_commit": "7c91b4e",
  "working_tree": "clean"
}
```

Recommended `working_tree` values:

- `clean`
- `dirty`
- `unknown`

If no commit was created during the checkpoint interval, `head_commit` MAY equal `base_commit`.

Git state proves repository identity. It does not, by itself, prove runtime behavior or external delivery.

## 11. Structural state

A Traceweave implementation MAY record structural representations such as a code graph, dependency index or other derived model.

Public minimal states:

- `synced`
- `stale`
- `not_applicable`
- `unknown`

If a structural artifact is marked `synced`, its source revision MUST be traceable to the repository state being claimed.

Example:

```json
{
  "status": "synced",
  "engine": "example-structural-tool",
  "source_commit": "7c91b4e",
  "verified_at": "2026-08-23T18:00:00Z"
}
```

Traceweave does not require a particular graph engine or publish a production synchronization mechanism as part of this specification.

## 12. Evidence states

An implementation SHOULD distinguish at least:

- `confirmed` — directly supported by admissible evidence;
- `derived` — deterministically computed from confirmed evidence;
- `inferred` — reasoned conclusion with explicit basis;
- `unknown` — not established;
- `superseded` — replaced by later evidence/decision.

A system MUST NOT silently convert `unknown` into `false`.

A system MUST NOT silently convert `inferred` into `confirmed`.

## 13. Checkpoint versus delivery proof

A **checkpoint** records technical state.

A **delivery proof** records that an expected delivery boundary was actually reached.

Examples of delivery evidence may include:

- a remote commit readback;
- a published artifact digest;
- a deployed version identifier;
- a verified external state;
- another independently inspectable receipt.

A checkpoint MAY reference a delivery proof.

A checkpoint MUST NOT be interpreted as delivery proof unless that relationship is explicitly recorded.

The public v0.1 Reference Demonstration does not implement a production delivery-proof engine.

## 14. Minimal checkpoint object

An intentionally small public object may look like:

```json
{
  "traceweave_version": "0.1",
  "checkpoint_id": "cp-example",
  "session": {},
  "provenance": {},
  "work": {},
  "tests": [],
  "git": {},
  "structural_state": {},
  "status": "partial"
}
```

This example is illustrative. Public schemas may evolve through documented specification changes.

## 15. Verification rules

A minimal public verifier SHOULD be able to check:

1. required identities exist;
2. repository revisions are explicit;
3. every claimed test has an explicit result;
4. changed files are listed when known;
5. provenance is explicit or unknown;
6. derived structural state points to the claimed source revision;
7. no unsupported claim is promoted to fact;
8. a `complete` status is justified by the evidence required for that boundary.

More advanced validation MAY exist outside the public reference implementation.

## 16. Reconstruction

A valid Traceweave trail should allow a later reviewer to follow a path such as:

```text
checkpoint
→ repository revision
→ changed files
→ tests/runtime evidence
→ provenance
→ optional delivery proof
```

The graph or index is a navigator.

The underlying evidence remains the basis for confirmation.

## 17. Open specification versus implementation

The following are part of the **open protocol surface**:

- evidence semantics;
- provenance roles;
- identity relationships;
- checkpoint semantics;
- public status values;
- reconstruction principles;
- governance and publication rules;
- deliberately limited examples.

The following are **not required to be open-source implementations**:

- production orchestration;
- complete adapters;
- automated ingestion engines;
- advanced validation systems;
- differentiating algorithms or heuristics;
- private infrastructure;
- commercial product integrations.

## 18. Reference Demonstration v0.1

The public Python implementation is deliberately constrained.

Its purpose is to demonstrate that a small executable implementation can:

- read Git state without mutation;
- create explicit factual checkpoints;
- preserve null provenance;
- represent tests as `not_run`;
- validate basic structure.

It should not be interpreted as the complete Traceweave product architecture.

## 19. Public examples

See:

- `examples/checkpoint.json`
- `examples/session-flow.md`
- `docs/method/ENGINEERING_METHOD.md`
- `docs/principles/EVIDENCE_PRINCIPLES.md`
