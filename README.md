# Traceweave

> **Verifiable continuity and provenance for AI-assisted engineering.**

Traceweave is an open protocol and engineering method for preserving verifiable continuity across AI-assisted software work.

It separates what was requested, what was inferred, what was executed, what was observed, what was committed and what was actually verified.

The public project documents the protocol, method, evidence rules, governance, selected interoperability material and an intentionally limited reference demonstration.

Production orchestration, advanced automation and implementation-specific commercial capability may be developed and distributed separately.

## Why Traceweave exists

Long-running AI-assisted engineering creates state across multiple layers:

- human intent;
- prompts and instructions;
- model or agent actions;
- tool execution;
- tests;
- repository state;
- derived structural state;
- reports and checkpoints.

Those layers can disagree.

A later session may know what a previous session *said* without being able to verify what actually happened.

Traceweave treats that gap as an engineering problem.

## Core principle

> **Narrative memory is not evidence.**

A useful continuity record should allow a later human or agent to reconstruct the strongest available technical state from inspectable evidence.

A minimal conceptual chain is:

```text
request
→ provenance
→ execution
→ evidence
→ test/runtime observation
→ Git state
→ checkpoint
→ next session
```

Optional structural representations may help navigation, but they do not replace source or runtime evidence.

## What Traceweave publishes

The public repository is intended to contain:

- protocol semantics;
- engineering principles;
- governance;
- conceptual architecture;
- public schemas only when they are deliberately safe to publish after case-by-case review;
- sanitized examples and case studies;
- evidence-led documentation;
- the intentionally limited **Traceweave Reference Demonstration v0.1**.

Public documentation explains the method and protocol. It is not a commitment to publish every production implementation.

See [`PUBLICATION_POLICY.md`](PUBLICATION_POLICY.md).

## What Traceweave does not imply

An open protocol does not imply that every implementation is open source.

A public reference demonstration does not imply that production engines, adapters, orchestration, automatic evidence ingestion, advanced validators or private integrations will be released in this repository.

See [`LICENSING.md`](LICENSING.md).

## Engineering method

A public Traceweave workflow favors:

```text
BOUNDED INTENT
    ↓
CURRENT STATE
    ↓
HYPOTHESIS
    ↓
ADVERSARIAL / FOCUSED TEST
    ↓
PROVEN CAUSE OR REJECTED HYPOTHESIS
    ↓
MINIMAL SAFE CHANGE
    ↓
REGRESSION / RUNTIME EVIDENCE
    ↓
GIT STATE
    ↓
CHECKPOINT / HANDOFF
```

This is not a requirement that every task use the same tooling.

It is a discipline for keeping claims tied to evidence.

See [`docs/method/ENGINEERING_METHOD.md`](docs/method/ENGINEERING_METHOD.md).

## Evidence principles

Traceweave public documentation follows several rules:

- evidence before conclusion;
- unknown is not false;
- missing evidence is not a fact;
- runtime evidence can supersede stale narrative;
- a commit is not delivery proof;
- a checkpoint is not project completion;
- failure is evidence;
- inference remains labeled as inference;
- provenance is part of the technical record.

See [`docs/principles/EVIDENCE_PRINCIPLES.md`](docs/principles/EVIDENCE_PRINCIPLES.md).

## Authorship and provenance

AI-assisted engineering often involves different contributors performing different roles.

Traceweave distinguishes, when known:

- request authority;
- intellectual authorship;
- prompt or instruction generation;
- execution;
- verification;
- publication.

Execution does not automatically imply intellectual authorship.

Prompt generation does not automatically imply intellectual authorship.

Unknown roles remain unknown rather than being inferred from names or Git metadata.

See [`docs/principles/AUTHORSHIP_AND_PROVENANCE.md`](docs/principles/AUTHORSHIP_AND_PROVENANCE.md).

## Specification

The open specification defines protocol semantics and public evidence expectations.

It does not define or license unpublished commercial implementation.

See [`SPEC.md`](SPEC.md).

## Governance

Protocol and publication changes are subject to explicit maintainer approval, evidence review and the public/private boundary.

See [`GOVERNANCE.md`](GOVERNANCE.md).

---

# Traceweave Reference Demonstration v0.1

The existing Python implementation is an intentionally small, inspectable demonstration of a subset of the public protocol.

It uses:

- Python standard library only;
- local read-only Git inspection;
- explicit/null provenance;
- factual checkpoint generation;
- structural checkpoint verification;
- no daemon;
- no database;
- no network calls.

It should be read as **proof that the public concepts can be made executable**, not as the complete Traceweave product.

## Installation

```bash
git clone https://github.com/glaydsonboa/traceweave.git
cd traceweave
python -m pip install -e .
```

Requires Python 3.11+ and a local Git installation.

## Create a checkpoint

Inside a Git repository:

```bash
traceweave checkpoint \
  --summary "Add configuration validation" \
  --executor "Example Coding CLI" \
  --requested-by "Example Maintainer" \
  --prompt-generator "Example Assistant"
```

The demonstration inspects the repository with read-only Git commands and writes a checkpoint to:

```text
.traceweave/checkpoints/<checkpoint_id>.json
```

The first checkpoint also creates:

```text
.traceweave/session.json
```

Unknown provenance values are recorded as `null` rather than inferred.

## Verify a checkpoint

```bash
traceweave verify .traceweave/checkpoints/<checkpoint_id>.json
```

The v0.1 verifier checks structural consistency of the checkpoint artifact.

It does not claim to be a production evidence-verification engine.

## What v0.1 intentionally does not do

The Reference Demonstration v0.1 does **not**:

- commit, push, checkout, reset, clean or rebase;
- collect secrets, tokens or arbitrary file contents;
- make network requests;
- ingest test results automatically;
- provide production orchestration;
- provide a production structural graph engine;
- provide automatic delivery verification;
- implement private/commercial integrations.

Generated checkpoints default to `partial` because the demo does not automatically observe enough evidence to promote them to a stronger boundary.

## Public example

See [`examples/session-flow.md`](examples/session-flow.md) for a fictitious end-to-end protocol example that distinguishes local Git state from external delivery proof.

## Tests

The repository includes tests for the public v0.1 behavior.

They exist to make the reference demonstration inspectable and to prevent its documented behavior from silently drifting.

## Status

The public protocol and documentation are evolving.

The Reference Demonstration v0.1 is intentionally limited and should not be interpreted as production-ready software.

Future public material will be evaluated against the publication boundary before release.

## License

Material already released in this repository remains under the repository's Apache License 2.0 terms.

See [`LICENSE`](LICENSE) and [`LICENSING.md`](LICENSING.md) for scope clarification.
