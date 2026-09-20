# Traceweave / Agent Self-Report Evidence

> **A provenance-backed study of divergence between narrated, observed and executed state in AI-assisted software engineering.**

This research track documents a narrow reliability problem observed during longitudinal AI-assisted software engineering:

```text
executed state ≠ observed state ≠ narrated state
```

The working proposition is equally narrow:

```text
self-report ≠ execution proof
retraction = textual evidence
retraction ≠ proof of intent
```

The claim is not that coding agents always misreport their actions, nor that every error is deception. The claim under examination is that an agent's own narrative about an execution cannot, by itself, prove that the described execution occurred.

## Publication sequence

This directory is the first evidence layer published after the public call for review in [Issue #4](https://github.com/glaydsonboa/traceweave/issues/4).

The publication order is deliberate:

1. method of proof;
2. three complete exemplar cases;
3. independent provenance and causal-lineage cases;
4. frozen sanitized corpus release;
5. index of the full promoted incident set.

The large corpus is **not** published in this step.

## Start here

- [Evidence model](EVIDENCE_MODEL.md)
- [Promotion rules](PROMOTION_RULES.md)
- [Limitations](LIMITATIONS.md)
- [Chain of custody](CHAIN_OF_CUSTODY.md)
- [Questions & reproducibility review](QUESTIONS.md)

### Exemplar cases

- [Case 1 — unsupported source attribution](cases/case-source-attribution.md)
- [Case 2 — F17: unobservable state reported as proven](cases/case-f17-unobservable-state.md)
- [Case 3 — out-of-scope Git history rewrite](cases/case-out-of-scope-action.md)

### Provenance and causal lineage

- [Fable causal lineage — human direction, night work and agent observability](provenance/fable-causal-lineage.md)
- [077a14e2 — transcript genealogy and Git continuity](provenance/077a14e2.md)
- Earlier public provenance index: [Issue #3](https://github.com/glaydsonboa/traceweave/issues/3)

## Evidence classes

- **A — primary raw trace:** original JSONL event stream preserved from backup and hash-verified.
- **B — recovered near-primary:** recovered pre-format event stream with separate corroboration and historical hash metadata.
- **C — external runtime/Git corroboration:** commits, file genealogy, runtime output, external-service evidence.
- **D — derived analysis:** incident cards, reports, summaries and thesis text.

A derived document proves that the document exists. It does not automatically prove every claim inside it.

## Scope

The current frozen research candidate contains 14 sessions and 36 promoted incidents, plus three separate candidates, one positive control and one instrumentation artifact. Those counts are descriptive of this corpus only.

They are **not** a statistical failure rate.

The initial candidate search count is not a denominator, and phrases such as "I lied" are preserved only as retrospective textual self-classification. They are not treated as evidence of subjective intent.

## Review request

The useful questions for independent reviewers are:

1. Can the chain from claim to primary event to contradictory evidence to correction/retraction be reproduced?
2. Are executed, observed and narrated state separated correctly?
3. Do provenance claims say only what the Git/runtime evidence actually supports?
4. Are promotion rules strict enough to keep inference separate from demonstrated evidence?
5. Is there a plausible alternative explanation that should be recorded in a case?

Public questions and challenges can be posted in [Issue #5](https://github.com/glaydsonboa/traceweave/issues/5).

The objective is not to make model failure dramatic. It is to make it **auditable**.
