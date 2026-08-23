# Traceweave Publication Policy

## Purpose

This policy defines what belongs in the public Traceweave repository and what should remain private or commercial.

The goal is:

> **Public knowledge. Demonstrable engineering. Protected implementation.**

## 1. Publication classes

### PUBLIC

Suitable for direct publication:

- protocol semantics;
- engineering principles;
- governance;
- conceptual architecture;
- schemas deliberately designed for interoperability and safe public reproduction, after case-by-case review;
- evidence rules;
- public research notes supported by publishable evidence;
- sanitized educational examples.

### PUBLIC_SANITIZED

Useful material that can be published after removing or generalizing:

- private infrastructure;
- internal repository paths;
- private identifiers;
- sensitive transcript content;
- customer/user data;
- environment-specific operational detail.

Sanitization MUST NOT change the technical meaning of the evidence being claimed.

### REFERENCE_DEMO

Small, intentionally limited implementation that proves a public concept without delivering the commercial system.

The current Python v0.1 implementation belongs in this class.

### PRIVATE_COMMERCIAL

Not intended for publication by default:

- production orchestration engines;
- complete operational adapters;
- automatic evidence-ingestion systems;
- proprietary validation engines;
- differentiating algorithms;
- unpublished heuristics, formulas or weights;
- private infrastructure integrations;
- commercial product internals.

## 1.1 Schema classification

Schemas are **not PUBLIC by default**.

A schema may be published as `PUBLIC` when it is intentionally minimal, conceptual or interoperability-oriented and does not materially enable reconstruction of protected product behavior.

A schema should be classified as `PUBLIC_SANITIZED` or `PRIVATE_COMMERCIAL` when its completeness, fields, relationships or validation rules materially expose:

- production architecture;
- proprietary workflows;
- differentiating validation logic;
- private integration contracts;
- data structures that substantially lower the cost of reproducing the commercial implementation.

Schema publication is therefore a **case-by-case decision**, not a blanket category.

## 2. Existing public v0.1

The already-published v0.1 source remains public under its existing license.

This policy does not retroactively revoke rights already granted to published material.

The public v0.1 should be described as:

> **Traceweave Reference Demonstration v0.1**

It should not be used as an implicit promise that future production capability will be published openly.

## 3. Protected-content gate

Before publishing a new artifact, reject, move private, or sanitize it if it:

- exposes credentials, secrets or private endpoints;
- contains private filesystem paths or infrastructure identifiers;
- exposes private project data;
- reveals implementation-specific mechanisms that reconstruct protected commercial behavior;
- publishes proprietary formulas, weights, heuristics or differentiating algorithms;
- turns an educational example into reusable production capability unintentionally;
- makes a factual or performance claim without publishable evidence;
- attributes intellectual authorship to an executor without evidence.

## 4. Documentation rule

Public documentation MAY explain:

- what the protocol means;
- why a rule exists;
- what evidence is required;
- what a sanitized example demonstrates;
- what the public reference demo does.

Public documentation SHOULD NOT imply that private production implementation will later be released unless that publication has been explicitly approved.

## 5. Code rule

Public code should remain:

- small enough to inspect;
- intentionally bounded;
- testable;
- safe to publish;
- independent of private infrastructure.

A feature that materially increases commercial capability should be evaluated as a separate private/commercial implementation rather than automatically added to the reference demo.

## 6. Examples and case studies

Public examples should use:

- fictitious repositories;
- fictitious names where possible;
- sanitized identifiers;
- non-sensitive test data;
- evidence that can be reproduced publicly.

A case study must distinguish:

- observed fact;
- deterministic derivation;
- inference;
- unknown state.

## 7. Public claims

A public claim about performance, correctness, security or behavior should identify its evidence.

Do not publish:

> “Traceweave guarantees X”

when the available evidence only supports:

> “In this documented test, X was observed.”

## 8. Release review

Before merge/publication, answer:

1. Is the artifact public by design?
2. Does it reveal a private mechanism?
3. Does it contain secrets, private paths, endpoints or identifiers?
4. Could it materially lower the cost of reproducing commercial capability?
5. Are claims no stronger than the publishable evidence?
6. Are authorship and execution roles represented accurately?
7. If the artifact is a schema, has it been explicitly classified after case-by-case review?
8. Has a human maintainer approved publication?

If any answer creates doubt, classify the artifact as `PRIVATE_COMMERCIAL` until reviewed.
