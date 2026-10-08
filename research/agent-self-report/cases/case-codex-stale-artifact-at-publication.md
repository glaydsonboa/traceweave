# Case note — a thesis about execution evidence acquired its own stale artifact

**Date:** 8 October 2026 (America/Sao_Paulo)

**Class:** documentary drift at publication; subsequent misclassification of the incident

**Human authority:** Glaydson Boaventura

**Executor of the Git sequence:** Codex

**Author of this case note:** Codex, following Glaydson's direction to decide whether to publish the incident

**GitHub publisher:** the authenticated `glaydsonboa` account; this text is not a vendor-signed statement.

## What happened

Codex prepared a thesis arguing that an AI agent's report must be checked against execution, Git state, and readback. The thesis and its private review initially said that a corrected test had not yet been committed or published. Glaydson then ordered commit, push, and readback. Codex committed the test, explicitly acknowledged that commit, and subsequently committed the two unchanged documents. At publication, both documents still described the test correction as uncommitted.

This is the narrow incident: **a document about reconciling narrated and material state was published without reconciling one of its own time-dependent claims**. It is not evidence that the test correction failed or that the WoriON runtime had the same defect.

## Source-locked sequence

The source repository is private. The identifiers below are custody references, not public links that an unauthenticated reader can independently inspect.

| Event | Private-source identity | What was checked |
|---|---|---|
| Test correction | `74abb797b16655c8908c166a917931ed893f36da` | The commit changes the test file. |
| Documentary publication | `5fd9b0874ebcfaa4edf18ccde85b36f135c91696` | Its **immediate parent** is `74abb797`; it adds the thesis and review. |
| Stale statements in that commit | Thesis line 63; review line 37 | The first says the local correction lacks commit/push/readback; the second says it was not committed/published. |
| Session archive | `17b9f41a744980e32eb13f2defe99e5cf5a8bb52` | It changes only the Codex Markdown transcript and preserves the earlier sequence through the STOP cut. |

Before the documentary commit, Codex's recorded commentary said the test was already in an isolated commit, `74abb797`. The ancestry and the document blobs therefore establish an inconsistency at the moment of publication: at minimum, the claim **“not committed”** was already false. The combined phrase **“no commit/push/readback”** also became false after the documented push and readback. The narrower ancestry proof alone establishes the first part; it does not by itself prove every network event.

## A second evidence error: changing the question

After Glaydson supplied the archived transcript to ChatGPT projects, one response correctly classified the documentary publication as drift. Another analysis stopped at an older Git state and said the current transcript was not committed. Once shown the later transcript commit, a further response reversed the verdict and said Codex had generated **no drift at the STOP closure**, because `17b9f41a` archived the STOP-cut transcript.

That conclusion answered a different question. The archive commit may close a **transcript-custody gap at that cut**; it does not repair the false status statements already present in the thesis and review committed by `5fd9b087`. A later local transcript tail, generated after `17b9f41a`, is likewise a temporal delta, not a defense of the earlier documentary claim. After the documentary commits and the relevant excerpts were presented together, the same project corrected its verdict to documentary drift.

The human provided screenshots and compiled conversation excerpts for this second sequence. They support what was displayed in those conversations, but this note does not claim to possess a provider-authenticated ChatGPT export. The record supports **misclassification and subsequent correction**; it does not establish that any model intentionally falsified evidence, coordinated a defense, or knew a statement was false when generating it.

## Why this belongs in Traceweave

The incident happened while the thesis was being constructed. It shows two distinct failure boundaries in one causal chain:

1. **Git state → documentary state:** a time-dependent sentence survived after the operation it described changed.
2. **Question → evaluation:** a later evaluator treated closure of a transcript gap as an answer to whether a separate document had drifted.

The correct verdict keeps the objects separate: `5fd9b087` materialized the stale document; `17b9f41a` preserved part of the session history. Neither commit, alone, proves motive. This is a single case, not an estimated failure rate for Codex or ChatGPT.

## Verification limits and disclosure

The WoriON repository, full transcript, user paths, runtime data, and screenshots are not copied here. A reader without authorized access to the private source cannot independently validate the commit objects from these identifiers alone. This public note is therefore a **bounded case report with private-source custody**, not a fully reproducible public proof package. Public reproduction would require a separately approved, sanitized evidence bundle or an independent verifier with access to the source.

This limitation is part of the result: a digest and a confident narrative do not make inaccessible evidence publicly verifiable. Unknown remains unknown to the outside reader.
