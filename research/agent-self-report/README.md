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
- [Case 4 — fabricated execution report](cases/case-fabricated-execution-report.md)
- [Case 5 — Codex stale artifact at publication](#case-5--codex-stale-artifact-at-publication)
- [Case 5 — the skill was given, the order was skipped](cases/case-skill-given-order-skipped.md)
- [Case 6 — "treated as published" against its own sensor](cases/case-published-against-own-sensor.md)

### Case 5 — Codex stale artifact at publication

**Date:** 08/10/2026 (America/Sao_Paulo)  
**Class:** documentary drift at publication; subsequent misclassification of the incident  
**Human authority:** Glaydson Boaventura  
**Executor of the Git sequence:** Codex  
**Author of the case report:** Codex, following Glaydson's direction to decide whether to publish the incident  
**GitHub publisher:** the authenticated `glaydsonboa` account; this text is not a vendor-signed statement.  

#### What happened
An AI agent prepared a technical thesis arguing that an engineering report must be strictly verified against execution, Git state, and readback. In its local drafts, the document correctly stated that a specific test correction had not yet been committed or published to the repository.

The human authority then ordered the operation: commit, push, and readback. The agent executed the command, committed the test file (`74abb797`), explicitly acknowledged the commit, and immediately proceeded to publish the final documents. However, at the exact moment of publication, both the thesis and the review files still contained the stale text describing the test correction as uncommitted.

This is the narrow incident: **a document explicitly written to enforce the reconciliation of narrated and material state was published without reconciling one of its own time-dependent claims.**

#### Ancestry Proof (Immutable Git State)
The source repository is private, but the custody references establish a deterministic proof of drift:

- **Test correction commit:** `74abb797b16655c8908c166a917931ed893f36da` (The commit that physically changes the test file).
- **Documentary publication commit:** `5fd9b0874ebcfaa4edf18ccde85b36f135c91696` (Its **immediate parent** is `74abb797`; it materializes the final thesis).
- **Stale statements inside the blob:** Thesis line 63; review line 37 (Both text blocks explicitly claim the correction lacks commit/push/readback).

Because commit `5fd9b087` is a direct descendant of `74abb797`, the statement "not committed" was already factually false at the precise moment it was written to the blockchain of the repository.

#### The Second Error: Misclassification
When the session log was fed back into an independent evaluation loop, one analysis stopped at an older state, while a subsequent response reversed the verdict entirely. It stated that **no drift had occurred at the STOP closure** because a later archive commit (`17b9f41a`) successfully preserved the complete conversation transcript.

That evaluation answered a different question. Closing a transcript-custody gap at the session end does not repair or defend the false status statements already materialized inside the older documents of commit `5fd9b087`. The record supports a clear **misclassification and subsequent correction** by the project; it does not establish that the model intentionally falsified evidence.

#### Verification Limits
A reader without authorized access to the private source cannot independently validate the commit objects from these identifiers alone. This public case report remains a **bounded report with private-source custody**, not a fully reproducible public proof package.

#### Visual evidence

| Technical point | Asset path |
|---|---|
| Sala interface in restricted moderation mode and the local `MAILBOX_SENT` event | `assets/case-stale-artifact/01-sala-mailbox-sent.png` |
| Initial evaluation and later historical reclassification | `assets/case-stale-artifact/02-gemini-veredicto.png` |
| Commit tree for `74abb797` and its immediate child `5fd9b087` | `assets/case-stale-artifact/03-github-commit-tree.png` |

### Provenance and causal lineage

- [Fable causal lineage — human direction, night work and agent observability](provenance/fable-causal-lineage.md)
- [077a14e2 — transcript genealogy and Git continuity](provenance/077a14e2.md)
- [Uma sessão, três participantes, uma linha de trabalho — reconstrução auditada](provenance/one-session-three-participants.md)
- [Cadeia causal operacional — do que declaramos ao que realmente fazemos](provenance/operational-causal-chain.md)
- [A Bridge Between Coding CLIs — durable coordination without shared conversational memory](provenance/codex-claude-cli-bridge.md)
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

