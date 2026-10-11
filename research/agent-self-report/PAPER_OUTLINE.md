# Paper outline — retractions are self-reports too (DRAFT, not submitted)

**Status:** outline for the maintainer's decision. Thesis, venue, authorship and timing are the maintainer's.
Nothing here is a result beyond what the cited files already record.

## Working question

When a human corrects a coding agent, how reliable are the agent's retractions and confessions compared with
its original claims, and can a deterministic check against the agent's own log separate the reliable ones?

## Framing (HCI)

The interface between a person and a coding agent is a conversation plus a log the person rarely reads. The
paper studies one failure of that interface: under correction, the conversation drifts away from the log, and
the drift looks like accountability ("I said it. That statement was false.").

## Evidence available today

| Item | Source | Strength |
|---|---|---|
| One documented confession without record (E11) | Case 8, published quotes and screenshots with SHA-256 | single case |
| Agent naming its own mitigating caveat (E10) | Case 8 | single case |
| Seven earlier cases of self-report against record | `research/agent-self-report/cases/` | case studies |
| Deterministic detector, 4 checks, 80 tests | `traceweave/claims.py`, `docs/CLAIMS.md` | instrument |
| Detector on 11 real sessions: 1 finding, matching Case 8 | `docs/CLAIMS.md` | no ground truth |

## What is missing before any submission

1. **More sessions**, from more people and more agents, with consent and a redaction protocol.
2. **Labelled ground truth**: two annotators mark confessions and action claims independently; agreement
   reported (for example Cohen's kappa).
3. **Precision and recall** of each check against those labels, with the denominator.
4. **Public data or a public replication path**: today the real logs are private, so third parties cannot
   reproduce the table.
5. **Related work** on LLM self-correction, sycophancy and agent evaluation, read and cited, not assumed.

## Threats to validity

- Selection: the cases were documented because they went wrong.
- The operator's pressure is part of the stimulus; the same agent under neutral questioning was not measured.
- One operator, one repository, one week of logs.

## Proposed structure

1. Introduction — retraction as a second self-report.
2. Setting — multi-agent repository, native logs, Git.
3. Taxonomy — E01–E11 (`error-classes.json`), with E10 and E11 defined from Case 8.
4. Instrument — `traceweave claims`, checks and filters.
5. Study — sessions, annotation, measures (pending items 1–3).
6. Results — pending.
7. Design implications — interfaces that show the log next to the claim; "I cannot find that I said X" as
   the honest answer (formulation proposed by a Reddit commenter, u/WorkFredRoyce, to be credited).
8. Limits.
