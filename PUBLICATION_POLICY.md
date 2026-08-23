# Traceweave Publication Policy

> Public knowledge. Demonstrable engineering. Protected implementation.

## Purpose

Traceweave documents a way of conducting AI-assisted engineering so that intent, decisions, execution, evidence, verification, and continuity remain distinguishable and auditable.

The public project is intended to explain the method, expose its principles, document observable results, and provide small educational examples without publishing the implementation that constitutes the commercial product.

## Publication classes

Every candidate artifact should be classified before publication.

### PUBLIC

Suitable for open publication:

- engineering principles and methodology;
- conceptual architecture;
- provenance and evidence models;
- session lifecycle and checkpoint concepts;
- governance rules;
- sanitized diagrams;
- limitations and lessons learned;
- case studies whose publication does not expose protected mechanisms.

### PUBLIC — SANITIZED

Material that is useful publicly only after removing:

- private infrastructure names and topology;
- credentials, tokens, paths, endpoints, internal identifiers, and private data;
- implementation-specific algorithms, formulas, heuristics, weights, and operational details;
- details that would allow reconstruction of a protected mechanism.

### SIMPLE DEMO

Small code examples may be public when their purpose is educational or demonstrative and they do not reproduce the commercial implementation.

A public demo should prove a concept, not deliver the product.

### PRIVATE / COMMERCIAL

Not intended for open publication:

- production engines and substantial source code;
- complete operational automation;
- proprietary algorithms and heuristics;
- implementation-level graph engines, validators, adapters, orchestration, and integrations;
- internal formulas, ranking logic, weights, or other differentiating mechanisms;
- anything that materially enables reproduction of the commercial implementation.

## Restricted topics

Certain internal mechanisms belong to other projects or protected research fronts. Their presence in development history does not make them part of Traceweave.

Material associated with restricted internal mechanisms must not be published as Traceweave architecture, implementation, documentation, examples, schemas, posts, or videos unless it has been separately reviewed and explicitly approved for release.

Even when approved, publication must disclose only the minimum necessary concept and must not expose internal purpose, architecture, dimensions, formulas, weights, contracts, implementation details, or operational relationships.

## Public evidence rule

A public claim should be no stronger than its evidence.

Prefer:

- observed;
- measured;
- verified;
- prototype;
- experimental;
- designed;
- implemented in the reference demonstration.

Avoid unsupported claims such as "production ready", "world first", or performance claims without publishable measurement.

## Code rule

The public repository may contain simple reference code. Public source code is not the definition of the complete Traceweave product.

When an implementation crosses from explanation into reusable commercial capability, it should remain private or be distributed under the applicable commercial terms.

## Review gate

Before publication, ask:

1. Does this explain the method without unnecessarily revealing the mechanism?
2. Does it contain private infrastructure or information from another project?
3. Could the material substantially reproduce a protected implementation?
4. Are all factual claims supported by evidence that can itself be published?
5. Is any code intentionally simple and demonstrative?
6. Is authorship/provenance represented accurately?

If any answer creates doubt, classify the artifact as PRIVATE / COMMERCIAL until reviewed.
