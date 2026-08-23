# Traceweave Governance

## Purpose

Traceweave governance exists to keep the public protocol credible, attributable and independently inspectable while preserving a clear boundary between public knowledge and private/commercial implementation.

## 1. Human authority

Protocol decisions are accepted through explicit maintainer approval.

AI systems, coding agents and CLIs may:

- propose;
- draft;
- implement;
- test;
- review;
- challenge.

They do not silently acquire authority over authorship, scope or publication policy merely by executing work.

## 2. Evidence standard

A public technical claim should be backed by evidence that a reviewer can inspect.

Preferred evidence includes:

- immutable repository revisions;
- test output;
- runtime observations;
- reproducible examples;
- public artifact digests;
- explicit provenance.

Narrative summaries are useful indexes, not final proof when a stronger source exists.

## 3. Conflict resolution

When sources conflict, public Traceweave documentation should prefer the strongest current evidence.

A typical precedence is:

```text
runtime/test evidence
→ repository state/diff
→ immutable artifact
→ closing report
→ transcript
→ backlog or historical summary
```

This ordering is contextual, not absolute. The important rule is that stale narrative must not override stronger later evidence without explanation.

## 4. Authorship

Traceweave separates:

- intellectual authorship;
- request authority;
- prompt/instruction generation;
- execution;
- verification;
- publication.

A contribution record should not attribute an architectural idea to an executor merely because the executor wrote the code.

See `docs/principles/AUTHORSHIP_AND_PROVENANCE.md`.

## 5. Specification changes

A public specification change should:

1. state the problem;
2. identify the evidence or use case motivating it;
3. describe the semantic change;
4. describe compatibility impact;
5. avoid committing the project to publication of protected implementation;
6. receive maintainer approval.

## 6. Reference implementation changes

The public Reference Demonstration is intentionally limited.

Changes are acceptable when they improve:

- clarity;
- correctness;
- security;
- testability;
- educational value;
- conformance to the public specification.

A change should be rejected or moved to a private/commercial implementation when it materially adds production orchestration, advanced automation or differentiating implementation capability beyond the intended public demo.

## 7. Publication boundary

Every proposed public artifact should be classified before publication:

- `PUBLIC`
- `PUBLIC_SANITIZED`
- `REFERENCE_DEMO`
- `PRIVATE_COMMERCIAL`

See `PUBLICATION_POLICY.md`.

## 8. Security and privacy

Public artifacts must not expose:

- credentials or tokens;
- private endpoints;
- private filesystem paths;
- customer/user data;
- private infrastructure identifiers;
- unpublished proprietary mechanisms;
- sensitive transcripts.

Sanitization must not fabricate evidence. When a value cannot be published, prefer a redacted or generalized value with an explicit note.

## 9. Independent review

Important protocol or publication changes should support adversarial review.

A reviewer should be able to disagree without editing the original evidence.

Recommended review output:

```text
AGREEMENTS
DISAGREEMENTS
RISKS
REQUIRED CHANGES
GO / NO-GO
```

## 10. Versioning

Public releases should identify:

- protocol/specification version;
- reference-demo version when applicable;
- immutable Git revision;
- relevant artifact digest for release packets when useful.

A protocol version and a commercial product version do not need to be the same.

## 11. Historical material

Historical documents remain useful for provenance but do not automatically define current architecture or current policy.

When a historical statement is superseded, mark or contextualize it rather than silently treating it as current.
