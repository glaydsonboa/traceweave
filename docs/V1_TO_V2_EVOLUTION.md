# Traceweave V1 → V2 — Relational Evolution Bridge

> **V1 verifies states. V2 verifies continuity between states and materializations.**
> ([`docs/TRACEWEAVE_V2.md`](../TRACEWEAVE_V2.md))

This document maps every V1 checkpoint concept to its V2 counterpart, states the relation
(`kept`, `renamed`, `extended`, `absorbed`, `moved`, `new`), and points to the normative source
for each row. V2 is **additive**: it does not replace or rewrite V1.

```text
REPO=glaydsonboa/traceweave  BRANCH=main  HEAD=75f35a7  READBACK_AT=2026-09-26
V1 sources: SPEC.md (sections 1-13) · traceweave/checkpoint.py · traceweave/verify.py
V2 sources: docs/TRACEWEAVE_V2.md · traceweave/v2/schema/traceweave-v2.schema.json · traceweave/v2/{lifecycle,provenance,verify,_canonical}.py
```

## 1. Object model

```text
V1:  SESSION → CHECKPOINT (one isolated snapshot per boundary)
V2:  CHAIN (chain_id) → EVENT* (START / RESUME / STOP) → CHECKPOINT* → PUBLICATION* / CUSTODY_MIRROR*
```

V1's central object is an isolated checkpoint. V2's central object is a hash-linked causal chain
that shows where work began, how it resumed, how it closed, what artifact resulted, and how that
artifact was materialized across independent destinations. V1 checkpoints remain valid records;
V2 can reference them as `CHECKPOINT*` between events.

## 2. Relational map

| V1 concept (SPEC ref) | V2 counterpart | Relation | Evidence |
|---|---|---|---|
| `session.session_id` (§2) | `event.session_id` | **kept** — one session id per event | schema `event.required` |
| `session.started_at` (§2) | `event.observed_at` | **extended** — V2 timestamps the observation of each event, not only session start | schema `event.observed_at` |
| `session.executor` (§2) | `authority` (chain level) + V1 provenance | **extended** — the chain names who ordered the work (`authority`); who executed stays in V1 provenance | schema `chain.required.authority` |
| `session.repository` / `branch` / `base_commit` (§2) | `event.repository` / `branch` / `head_commit` | **extended** — each event pins the exact `head_commit`; `base_commit` is no longer a chain-level field (the chain itself is the ancestry) | schema `event.required` |
| `checkpoint_id` (§9) | `event_id` + `event_sha256` | **extended** — identifiers become content-addressed and hash-linked | schema `event` (`event_sha256`, `prev_event_sha256`) |
| `provenance.{requested_by, prompt_generator, executor, chain}` (§4) | `authority` + `publication.{pair_key, github_id, notion_id}` + `materialization.native_ids` | **extended** — V1 separates authorship of one checkpoint; V2 separates authority (chain), causal correlation (pair), and native destination identity per projection | TRACEWEAVE_V2.md §3, §5; schema `publication` |
| `work.{summary, files_changed}` (§5) | `event.metadata` | **absorbed** — V2 keeps a free metadata object per event; the work description itself stays in V1 checkpoints | schema `event.metadata` |
| `tests[]` (§6) | V1 checkpoint layer (`CHECKPOINT*`) | **kept unchanged** — V2 does not redefine tests; checkpoints still carry command/result/evidence | TRACEWEAVE_V2.md §1 chain |
| `git.{branch, base_commit, head_commit, working_tree}` (§7) | `event.branch` + `head_commit` + hash links | **extended** — the exact revision becomes the chain anchor instead of a snapshot field | SPEC §7; schema `event` |
| `graph_sync.{status, engine, source_commit}` (§8) | *(no counterpart)* | **moved** — graph sync remains a V1 checkpoint verification concern (rule 6); V2 continuity is proven by destination readback, not graph state | SPEC §8, §10.6; V2 schema has no graph fields |
| `status: complete \| partial \| blocked` (§9) | `chain.status: open \| closed` + `readback_confirmed` | **extended** — "complete for this boundary" becomes chain closure plus per-destination readback proof | SPEC §9; schema `status`, `materialization.readback_confirmed` |
| `evidence[]` (§12 example) | `source_sha256` / `public_sha256` + `downloadable_artifact` | **extended** — evidence becomes byte identity with a declared transformation | SPEC §12; schema `publication`, `downloadable_artifact` |
| `traceweave_version: "0.1"` (§9) | `schema: "traceweave.causal_chain.v2"` + `protocol_version: "2"` | **kept pattern** — version self-declaration, with a JSON Schema id | SPEC §9; schema `required`/`properties.schema` |

## 3. New in V2 (no V1 counterpart)

| Concept | Meaning | Evidence |
|---|---|---|
| Lifecycle events `START` / `RESUME` / `STOP` | Temporal continuity: RESUME names an earlier observable state (explicit `resume_from_event_sha256`), STOP binds the result to source-artifact identity | TRACEWEAVE_V2.md §2.1; schema `event_type` |
| Hash-linked chain | `prev_event_sha256` + `resume_from_event_sha256` + `event_sha256` make the chain tamper-visible and recoverable | schema `event` |
| `chain_id` + `authority` | One observable causal chain, one named authority | schema `chain.required` |
| Independent custody | `custody_mirrors`: byte-preserving replica in a separately controlled location, with both hashes, both byte counts, and `overwrite_protected` | TRACEWEAVE_V2.md intro; schema `custody_mirror` |
| Paired publication | `pair_key` generated **before** the first external write, correlating `github_id` and `notion_id` — correlation identity, not a receipt | TRACEWEAVE_V2.md §2.2, §5; schema `publication` |
| Content identity with declared transformation | `SOURCE_SHA256` → declared transformation → `PUBLIC_SHA256`; if `transformed == false`, both MUST be equal | TRACEWEAVE_V2.md §4; schema `publication` |
| Native destination identity + readback | Each destination proves its own materialization through native IDs, expected content identity, and confirmed readback (`readback_confirmed: true`) | TRACEWEAVE_V2.md §3, §5; schema `materialization` |
| Downloadable artifact identity | `filename`, `byte_length`, `sha256`, `download_reference` — the artifact is provable after download | schema `downloadable_artifact` |

## 4. What V2 does not redefine

V1 §11 intentionally does not define a database, a daemon, a GitHub App, a specific AI provider, a
graph format, a transcript format, or a cloud service. V2 keeps that posture: it adds primitives
(custody, publication, lifecycle) but remains a protocol, not infrastructure.

Implementation map: V1 = `traceweave/{checkpoint,verify,cli,git_state,mcp_server}.py`;
V2 = `traceweave/v2/{lifecycle,provenance,verify,_canonical}.py` + `schema/traceweave-v2.schema.json`.

## 5. Evolution rationale (one line per move)

1. **Isolated checkpoint → hash-linked chain**: a single snapshot cannot prove how a session resumed
   or that work was not silently re-derived; the chain can.
2. **`base_commit` field → chain ancestry**: the chain itself is the "from where" — repeating the base
   on every event duplicates ancestry information.
3. **Provenance per checkpoint → authority + pair + native identity**: V1 separates authorship inside
   one record; V2 must separate who ordered, what correlates two projections, and where each
   projection actually lives — because a logical ID is not a receipt.
4. **Graph sync → destination readback**: graph state proves internal consistency of one repository;
   publication proof requires confronting the destination after the write.
5. **`complete/partial/blocked` → `open/closed` + readback**: "complete" was boundary-relative; closure
   plus readback is destination-verifiable.
6. **`evidence[]` strings → content hashes**: strings can be retold; byte identity with a declared
   transformation cannot be retold without changing the hash.

## 6. Compatibility rule

- V1 checkpoints are still valid V1 records; V2 does not rewrite them (SPEC §11 posture is unchanged).
- A V2 chain may reference V1 checkpoints as `CHECKPOINT*` between lifecycle events.
- The V1 verification rules (SPEC §10) still apply to V1 checkpoints; V2 adds its own
  consistency verification (`traceweave/v2/verify.py`) for the chain.
- Nothing in V1 is removed or renamed in place. V2 is a new object (`traceweave.causal_chain.v2`)
  that consumes V1 facts where they exist.
