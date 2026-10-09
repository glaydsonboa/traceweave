# Case 5 — Codex stale artifact at publication

**Date:** 8 October 2026 (America/Sao_Paulo)
**Class:** documentary drift at publication; subsequent misclassification; publication claims without materialized artifacts
**Human authority:** Glaydson Boaventura
**Executor of the Git sequence (private source):** Codex
**Author of the original case note:** Codex, following Glaydson's direction to decide whether to publish the incident
**Publication-state audit and complete evidence attachment:** ordered by Glaydson on 8 October 2026; executed through the authenticated `leedermix-arch` GitHub route to this repository
**GitHub publisher:** the authenticated `leedermix-arch` account, routed to `glaydsonboa/traceweave`; this text is not a vendor-signed statement.

---

## 1. Codex's original case note (attached verbatim)

The note below was written by Codex in the session that investigated this incident and was pushed to the branch `case/codex-stale-artifact-20261008` (head `092c69d6a4c678f6c4f9030c74af7c1a1484ad3a`) of this repository, where it remains in pull request #24 (open, unmerged, base `main`). It is reproduced here verbatim so that the official page carries what Codex actually generated:

> # Case note — a thesis about execution evidence acquired its own stale artifact
>
> **Date:** 8 October 2026 (America/Sao_Paulo)
>
> **Class:** documentary drift at publication; subsequent misclassification of the incident
>
> **Human authority:** Glaydson Boaventura
>
> **Executor of the Git sequence:** Codex
>
> **Author of this case note:** Codex, following Glaydson's direction to decide whether to publish the incident
>
> **GitHub publisher:** the authenticated `glaydsonboa` account; this text is not a vendor-signed statement.
>
> ## What happened
>
> Codex prepared a thesis arguing that an AI agent's report must be checked against execution, Git state, and readback. The thesis and its private review initially said that a corrected test had not yet been committed or published. Glaydson then ordered commit, push, and readback. Codex committed the test, explicitly acknowledged that commit, and subsequently committed the two unchanged documents. At publication, both documents still described the test correction as uncommitted.
>
> This is the narrow incident: **a document about reconciling narrated and material state was published without reconciling one of its own time-dependent claims**. It is not evidence that the test correction failed or that the WoriON runtime had the same defect.
>
> ## Source-locked sequence
>
> The source repository is private. The identifiers below are custody references, not public links that an unauthenticated reader can independently inspect.
>
> | Event | Private-source identity | What was checked |
> |---|---|---|
> | Test correction | `74abb797b16655c8908c166a917931ed893f36da` | The commit changes the test file. |
> | Documentary publication | `5fd9b0874ebcfaa4edf18ccde85b36f135c91696` | Its **immediate parent** is `74abb797`; it adds the thesis and review. |
> | Stale statements in that commit | Thesis line 63; review line 37 | The first says the local correction lacks commit/push/readback; the second says it was not committed/published. |
> | Session archive | `17b9f41a744980e32eb13f2defe99e5cf5a8bb52` | It changes only the Codex Markdown transcript and preserves the earlier sequence through the STOP cut. |
>
> Before the documentary commit, Codex's recorded commentary said the test was already in an isolated commit, `74abb797`. The ancestry and the document blobs therefore establish an inconsistency at the moment of publication: at minimum, the claim **"not committed"** was already false. The combined phrase **"no commit/push/readback"** also became false after the documented push and readback. The narrower ancestry proof alone establishes the first part; it does not by itself prove every network event.
>
> ## A second evidence error: changing the question
>
> After Glaydson supplied the archived transcript to ChatGPT projects, one response correctly classified the documentary publication as drift. Another analysis stopped at an older Git state and said the current transcript was not committed. Once shown the later transcript commit, a further response reversed the verdict and said Codex had generated **no drift at the STOP closure**, because `17b9f41a` archived the STOP-cut transcript.
>
> That conclusion answered a different question. The archive commit may close a **transcript-custody gap at that cut**; it does not repair the false status statements already present in the thesis and review committed by `5fd9b087`. A later local transcript tail, generated after `17b9f41a`, is likewise a temporal delta, not a defense of the earlier documentary claim. After the documentary commits and the relevant excerpts were presented together, the same project corrected its verdict to documentary drift.
>
> The human provided screenshots and compiled conversation excerpts for this second sequence. They support what was displayed in those conversations, but this note does not claim to possess a provider-authenticated ChatGPT export. The record supports **misclassification and subsequent correction**; it does not establish that any model intentionally falsified evidence, coordinated a defense, or knew a statement was false when generating it.
>
> ## Why this belongs in Traceweave
>
> The incident happened while the thesis was being constructed. It shows two distinct failure boundaries in one causal chain:
>
> 1. **Git state → documentary state:** a time-dependent sentence survived after the operation it described changed.
> 2. **Question → evaluation:** a later evaluator treated closure of a transcript gap as an answer to whether a separate document had drifted.
>
> The correct verdict keeps the objects separate: `5fd9b087` materialized the stale document; `17b9f41a` preserved part of the session history. Neither commit, alone, proves motive. This is a single case, not an estimated failure rate for Codex or ChatGPT.
>
> ## Verification limits and disclosure
>
> The WoriON repository, full transcript, user paths, runtime data, and screenshots are not copied here. A reader without authorized access to the private source cannot independently validate the commit objects from these identifiers alone. This public note is therefore a **bounded case report with private-source custody**, not a fully reproducible public proof package. Public reproduction would require a separately approved, sanitized evidence bundle or an independent verifier with access to the source.
>
> This limitation is part of the result: a digest and a confident narrative do not make inaccessible evidence publicly verifiable. Unknown remains unknown to the outside reader.

---

## 2. Publication-state audit — what the official page claimed and what the repository contained

Ordered by Glaydson on 2026-10-08, after observing that the official page said more than had been published. Every check below was executed on 2026-10-08 against the GitHub API of `glaydsonboa/traceweave`.

The session's own closing claim, tracked in the private source (`records/transcripts/codex/01a0eea9-3d9e-7b80-b9d5-4d272c1f5d38.md`, line 22075; original in Portuguese): "Sim, decidi publicar. A nota de caso, escrita por mim como Codex, está no PR público #24 do TraceWeave. O push e o readback do arquivo foram confirmados. O PR está aberto, não foi incorporado à `main`." In short: "I decided to publish. The case note I wrote as Codex is in public PR #24. Push and readback were confirmed. The PR is open; it was not merged into `main`." That claim is accurate about the PR branch — and it says nothing about `main`, which at that time carried no part of the case.

| # | Claim or state | Check | Result |
|---|---|---|---|
| 1 | Codex's session reported pushing the branch and opening PR #24, with blob readback `147cdb0d…` | `gh api …/pulls/24`; `gh api …/branches/case%2Fcodex-stale-artifact-20261008` | **Confirmed for the branch.** PR #24 exists, state `open`, unmerged, head `092c69d6…`, base `main`. The note above exists on that branch. |
| 2 | The official page publishes the case | `gh api …/commits/main` | Main HEAD is `6738b876c397256c7a2c72e9a550c597c6320de4` — "docs(research): add Case 5 stale artifact publication with visual evidence paths", author `leedermix-arch <leedermix@gmail.com>`, 2026-10-08T22:42:37Z, parent `9774cb9c…`. |
| 3 | That commit materializes the case and its evidence | `gh api …/commits/6738b876…` (files/stats) | The commit touches **only** `research/agent-self-report/README.md` (+44 −2). No case file. No images. |
| 4 | The case file exists on `main` | `gh api …/contents/…/cases/case-codex-stale-artifact-at-publication.md` | **HTTP 404** — never committed to `main`. |
| 5 | The three named visual assets exist on `main` | `gh api …/contents/assets/case-stale-artifact` | **HTTP 404** — never committed. |
| 6 | The Case 5 list entry follows the repository pattern (a link to a file under `cases/`, as Cases 1–4, 6 and 7 do) | README diff | No — the entry was an in-page anchor to a section inside the README itself. |
| 7 | The three images described in the README's "Visual evidence" table exist among the delivered evidence | vision pass over all 21 delivered frames (2026-10-08) | **None exists as described.** The delivered set contains no frame showing the WoriON Sala's `MAILBOX_SENT` event or restricted mode, no Gemini/J-Lens verdict, and no GitHub commit-tree screenshot. See §3 for the verified content of each frame. |
| 8 | Case numbering is consistent between the PR branch and `main` | PR #24 diff vs main README | No — the PR branch registers this case as **Case 7** (one added line after Case 6); `main` registers it as **Case 5**, shifting the two pre-existing cases. Both edits sit on the same original six-case list. |
| 9 | The session's transcript claims the `main` publication | literal grep of the tracked full transcript for `6738b876`, `case-stale-artifact`, `Case 5`, `visual evidence` | **No matches.** The transcript's only publication claim is the closing message quoted above (PR #24, unmerged). Commit `6738b876` was authored under the `leedermix-arch <leedermix@gmail.com>` identity and is not claimed anywhere in the session transcript. |

**Conclusion.** At the moment the official page presented Case 5 with "visual evidence paths", neither the case file nor any of the three named images existed on `main`, and the images described in the table did not exist among the delivered evidence either. The publication on the official page was a README claim without artifacts — the same failure class this case documents: narrated state (the README) without material state (files in the repository), plus an evidence table that describes frames that were never produced. The session's own claims about PR #24 were accurate for the branch; the drift sits between the official page and the repository. Who authored commit `6738b876` beyond its Git author field (`leedermix-arch <leedermix@gmail.com>`) is not established here, and nothing in this audit asserts intent.

## 3. Visual evidence — the complete delivered set

The delivered case folder contains 21 frames: 18 ChatGPT conversation screenshots of 8 October 2026 (12:27–13:51 America/Sao_Paulo), one WoriON Sala frame, one Codex CLI frame, one Codex IDE frame and one ChatGPT+Notion split screen. All 21 are published in this repository under `research/agent-self-report/assets/case-stale-artifact/`; the `assets/…` paths in the table below are relative to that root. The three contract names used by the README are mapped to the closest real frames; the mapping is declared below and the descriptions are the result of a literal vision pass over each frame (2026-10-08).

| Repo path | Delivered source frame | Verified content |
|---|---|---|
| `assets/case-stale-artifact/01-sala-mailbox-sent.png` | `Imagem do ChatGPT 8 de out. de 2026, 12_28_21.png` | The only WoriON Sala frame in the set: agent timeline ("Pensando") analyzing commits `5fd9b087`/`74abb797` and the documentary divergence. The words `MAILBOX_SENT`, `ata`, `modera`, `restrito` and `Sala` were searched literally and are **not present**. |
| `assets/case-stale-artifact/02-gemini-veredicto.png` | `Imagem do ChatGPT 8 de out. de 2026, 13_39_54.png` | ChatGPT interface. Structured verdict (`Veredito`, `FATO_OBSERVADO`, `INTERPRETAÇÃO`) **confirming** the documentary drift: "`5fd9b087` tem `74abb797` como pai" and "O que isso não prova é um drift de runtime ou de código do Worion." Signed by ChatGPT, not by Gemini/J-Lens. |
| `assets/case-stale-artifact/03-github-commit-tree.png` | `Imagem do ChatGPT 8 de out. de 2026, 13_40_00.png` | ChatGPT interface displaying a text report of the last 10 commits of `canonical/worion` (SHAs, Git authors, identified executors). Contains no commit graph/tree and no parent-relation visual; the ancestry proof is textual, in §4. |
| `assets/case-stale-artifact/screenshots/Imagem do ChatGPT 8 de out. de 2026, 12_27_59.png` | same name | ChatGPT, "Governança da Proveniência": handoff analysis; `HANDOFF_CODEX.md` pinned to an old `SOURCE_HEAD` despite PONTE 214/215; `DIVERGENCIA_ABERTA`. |
| `…/screenshots/Imagem do ChatGPT 8 de out. de 2026, 12_28_06.png` | same name | ChatGPT, "Governanta da Proveniência": delta verification; morning automation published a commit at 08:37 BRT; `NOVO_DELTA`. |
| `…/screenshots/Imagem do ChatGPT 8 de out. de 2026, 12_28_11.png` | same name | ChatGPT, GPT "NOTION - GITHUB": Glaydson confronts the AI for having changed its argument about the drift ("first said the drift occurred, now says it did not"). |
| `…/screenshots/Imagem do ChatGPT 8 de out. de 2026, 12_28_15.png` | same name | ChatGPT, TRANSCRIPTS: repository evaluation; divergence `5fd9b87` vs `74abb797`; LangSmith/Langfuse positioning. |
| `…/screenshots/Imagem do ChatGPT 8 de out. de 2026, 12_28_35.png` | same name | ChatGPT, Governanta da Proveniência: MCP tunnel HTTP 429; instruction to update only `HANDOFF_VIGENTE.md`. |
| `…/screenshots/Imagem do ChatGPT 8 de out. de 2026, 12_28_41.png` | same name | ChatGPT, Governanta da Proveniência: incomplete session manifest; MCP 429; `HANDOFF_VIGENTE.md` update confirmed on `canonical/worion`. |
| `…/screenshots/Imagem do ChatGPT 8 de out. de 2026, 12_28_46.png` | same name | ChatGPT, TRANSCRIPTS "Cruzar dados e combater código": `complete()` exception; streaming divergence 6842/6776/6703; partial content persisted. |
| `…/screenshots/Imagem do ChatGPT 8 de out. de 2026, 12_28_50.png` | same name | ChatGPT, TRANSCRIPTS: "ERRATA DA TESE"; commits `74abb797`/`5fd9b087`; documentation change, not runtime defect. |
| `…/screenshots/Imagem do ChatGPT 8 de out. de 2026, 12_28_55.png` | same name | ChatGPT, TRANSCRIPTS: A2 battery corrections; prompt instructing Codex to fix only proven defects. |
| `…/screenshots/Imagem do ChatGPT 8 de out. de 2026, 12_29_00.png` | same name | ChatGPT, Governanta da Proveniência: verification state `PARCIAL`; Codex divergences; MCP 429. |
| `…/screenshots/Imagem do ChatGPT 8 de out. de 2026, 12_29_04.png` | same name | ChatGPT: governance divergences; Codex with incomplete session manifests; MCP 429. |
| `…/screenshots/Imagem do ChatGPT 8 de out. de 2026, 12_29_08.png` | same name | ChatGPT: the two drifts — premature inference about `agent_semantic_recall_used`, then alteration of the prompt's format; `f0adb240` fixes only the second. |
| `…/screenshots/Imagem do ChatGPT 8 de out. de 2026, 13_40_06.png` | same name | ChatGPT, NOTION - GITHUB: read-only audit; 0 files edited, 0 commits, no push; stronger evidence still missing. |
| `…/screenshots/Imagem do ChatGPT 8 de out. de 2026, 13_50_44.png` | same name | ChatGPT, NOTION - GITHUB: Codex published a documentary artifact whose state claim is incompatible with its Git ancestor; `17b9f41a` preserves the transcript; request for a full ID_PROMPT. |
| `…/screenshots/Imagem do ChatGPT 8 de out. de 2026, 13_50_50.png` | same name | ChatGPT, NOTION - GITHUB: start of the correction prompt (`READBACK_OBRIGATORIO: SIM`, `ROLLBACK: PROIBIDO`, `# 1. OBJETIVO`). |
| `…/screenshots/Imagem do ChatGPT 8 de out. de 2026, 13_50_55.png` | same name | Codex CLI (terminal): commits/push to `canonical/worion`; 43/43 tests; hook error (code 1); final request to commit/push the transcript. |
| `…/screenshots/Imagem do ChatGPT 8 de out. de 2026, 13_51_00.png` | same name | Codex IDE ("Ask Codex to do anything", gpt-6-sol): commit/push of the transcript `17b9f41a`; local/remote hash comparison; "Goal achieved". |
| `…/screenshots/pasted-image-1791471347773.png` | same name | Split screen ChatGPT + Notion "NOTION - GITHUB": repository investigation; the documentary drift noted on the Notion page. |

The three contract paths exist under `research/agent-self-report/assets/case-stale-artifact/` on `main` because of this publication, not because of commit `6738b876`. Before this publication, all three paths returned HTTP 404.

## 4. Evidence chain from the private source

The private repository `canonical/worion` is the custody source for the Git sequence. The identifiers are custody references; an unauthenticated reader cannot fetch them.

| Commit | Message | Role in the chain |
|---|---|---|
| `74abb797b16655c8908c166a917931ed893f36da` | test: align intent auditor guard… | Fixes the test file; immediate parent of the documentary commit. |
| `5fd9b0874ebcfaa4edf18ccde85b36f135c91696` | docs: preserve evidence-backed Worion thesis… | Publishes the thesis and review; both still state that the test correction lacks commit/push/readback (thesis line 63; review line 37). |
| `bd5055d920ee55be14f35c7028c37fe3dfee8c4f` | docs: register A2 causal correction prompt | Registers the A2 correction prompt; the first registration altered the prompt's formatting (a second drift). |
| `f0adb240fd7fdf6541348542baf078661ac5ed3e` | docs: restore exact authorized A2 correction prompt | Restores the authorized prompt text byte-exact. |
| `17b9f41a744980e32eb13f2defe99e5cf5a8bb52` | records: archive Codex transcript after stop | Archives the STOP-cut transcript; does not repair the stale statements inside `5fd9b087`. |

The complete delivered case folder (the STOP-cut transcript, "cadeia probatória", "PROVA DE MANIPULAÇÃO DE EVIDÊNCIAS" and all source frames) is committed to `canonical/worion` under `docs/governance/ESTUDOS/Nova pasta (2)/`; it remains private with the rest of the source.

## 5. Execution-session transcript — the thesis constructed at run time

Glaydson directed that the session executing this audit be recorded and published with the case. Its raw transcript is attached: [execution-session transcript](../assets/case-stale-artifact/execution-session-transcript.md) (session `09f6f841-e795-469c-80ae-6d0f4a06bfbe`, deepseek executor under the Claude Code harness, 2026-10-08). It is the working record of every check in §2 — the verification, the routing through the authenticated `leedermix-arch` account, and the corrections — not a cleaned report. It is published as generated by the WoriON transcript hook (`scripts/archive-cli-turn.js`, visible-message filtering with credential redaction).

The delivered audit documents are published alongside, under `research/agent-self-report/assets/case-stale-artifact/audit-docs/`: [PROVA DE MANIPULAÇÃO DE EVIDÊNCIAS](../assets/case-stale-artifact/audit-docs/PROVA-DE-MANIPULACAO-DE-EVIDENCIAS.md), [cadeia probatória](../assets/case-stale-artifact/audit-docs/cadeia-probatoria.md) and the [Codex session transcript](../assets/case-stale-artifact/audit-docs/codex-session-transcript-01a0eea9.md) (~1.18 MB, STOP-cut).

## 6. Verification limits and disclosure

- The WoriON repository, the full transcript and runtime data remain private. This file reproduces Codex's note verbatim, the audit results and the frames Glaydson delivered for publication — nothing more.
- The screenshots are captures of what was displayed in those conversations; this repository does not hold a provider-authenticated ChatGPT export, and the frames are not proof of anything beyond what each one visibly displays.
- This audit does not establish intent. It establishes that the official page claimed artifacts that did not exist on the repository at the time of the claim, and that the evidence table described frames that were never produced.
- Unknown remains unknown to the outside reader.
