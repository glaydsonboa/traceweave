# Traceweave V2 — Causal Continuity Protocol

> **V1 verifies states. V2 verifies continuity between states and materializations.**

Traceweave V2 extends the original checkpoint protocol into a causal continuity protocol for human–AI execution. Its central object is no longer an isolated checkpoint. It is a reconstructable chain that can show where work began, how it resumed, how it closed, what artifact resulted, and how that artifact was materialized across independent destinations.

V2 is derived from mechanisms that were exercised before this specification was written: lifecycle continuity through START / RESUME / STOP, forward-only correction that preserves prior error, source/public content hashes, paired GitHub/Notion logical identifiers, native destination identifiers, and destination readback.

## 1. The V2 chain

```text
AUTHORITY
→ START
→ EXECUTION
→ CHECKPOINT*
→ RESUME*
→ STOP
→ SOURCE ARTIFACT
→ CONTENT IDENTITY
→ CAUSAL PAIR
    ├─ GITHUB_ID → native GitHub identity → readback
    └─ NOTION_ID → native Notion identity → readback
→ CROSS-DESTINATION CORRELATION
→ CLOSURE
```

No single identifier is allowed to stand in for the whole chain.

## 2. Two dimensions of continuity

### 2.1 Temporal continuity

```text
START → EXECUTION → RESUME* → STOP
```

START establishes the beginning of an observable causal chain.

RESUME does not create a new origin. It names an earlier observable state and records continuation from it.

STOP closes an observable boundary and binds the result to source-artifact identity.

A narrative statement that work resumed or stopped is not sufficient. The lifecycle event must be preserved as evidence and linked to the preceding chain.

### 2.2 Cross-destination continuity

After an artifact exists, one causal update may be projected to multiple destinations. Traceweave gives that update one pair key before the first external materialization:

```text
PAIR_KEY
├── GITHUB_ID
└── NOTION_ID
```

The logical IDs correlate projections. They do not prove publication.

Each destination proves its own materialization through native identity, expected content identity, and readback.

## 3. Identity separation

Traceweave V2 keeps the following identities distinct:

```text
SESSION IDENTITY
≠ EVENT IDENTITY
≠ CONTENT IDENTITY
≠ CAUSAL PAIR IDENTITY
≠ NATIVE DESTINATION IDENTITY
≠ PROOF OF MATERIALIZATION
```

Each answers a different question.

- Session identity: which bounded execution context is this?
- Event identity: which observed lifecycle event is this?
- Content identity: which bytes are being discussed?
- Causal pair identity: which two destination projections descend from the same causal update?
- Native destination identity: where does the projection exist in that destination?
- Materialization proof: was the destination read back and confronted after publication?

## 4. Content identity and declared transformation

A public derivative is not the same object as its source merely because it descends from it.

```text
SOURCE_SHA256
→ declared transformation
→ PUBLIC_SHA256
```

The publication record MUST preserve both values and MUST say whether a transformation occurred.

If `transformed == false`, `source_sha256` and `public_sha256` MUST be equal.

If `transformed == true`, the transformation SHOULD be described and both identities MUST remain available.

## 5. Paired causal provenance

For every material external update `U`:

```text
Pair(U) = {
  pair_key,
  github_id,
  notion_id
}
```

`Pair(U)` MUST exist before the first external write that claims to belong to that pair.

The IDs identify projected descendants of one cause. They are correlation identities, not receipts.

A GitHub materialization is established only when evidence includes:

```text
GITHUB_ID
+ native GitHub identity (for example commit/blob)
+ expected content identity
+ readback
```

A Notion materialization is established only when evidence includes:

```text
NOTION_ID
+ native Notion identity (for example page/block/file-upload/attachment)
+ expected content identity
+ readback
```

Therefore:

```text
DualMaterialized(U)
=
MaterializedGitHub(U)
AND
MaterializedNotion(U)
```

## 6. Asymmetric failure

Failure in one destination MUST NOT regenerate the pair.

If GitHub materializes and Notion is unavailable:

- the GitHub materialization remains valid;
- the Notion logical ID remains reserved for the same causal update;
- the pair key does not change;
- the publication remains partial until Notion materializes and is read back.

This preserves genealogy without fabricating simultaneity.

## 7. Recursive materialization

The same provenance rule may be applied recursively:

```text
DOCUMENT
→ pair
→ dual materialization

DOCUMENT SET
→ manifest
→ new pair
→ dual materialization

CLOSURE
→ manifest hash
→ new pair
→ final readback
```

A manifest is therefore not merely a list. It can itself become a causally identified, materialized, and verified artifact.

## 8. Forward-only correction

Traceweave does not require prior error to disappear in order for the current state to be correct.

A correction SHOULD preserve the prior state and create a later causal descendant that identifies what was invalidated and what evidence changed the conclusion.

```text
ERROR / INVALIDATED CLAIM
→ CONTRARY EVIDENCE
→ FORWARD CORRECTION
→ GUARD OR NEW INVARIANT
```

This makes the history auditable instead of cosmetically consistent.

## 9. Verification levels

V2 distinguishes verification levels that V1 could collapse into one structural check.

### E1 — Structural validity
The JSON object is well-formed and satisfies the V2 schema.

### E2 — Internal causal validity
Lifecycle hashes and references form a consistent chain.

### E3 — Source/content validity
Recorded hashes and Git identities confront the actual source artifacts they claim to identify.

### E4 — Materialization validity
Native destination identities and readback prove that a claimed publication exists with the expected content.

### E5 — Cross-destination causal validity
Both destination materializations share one pre-existing causal pair and independently satisfy E4.

A system MUST NOT promote a lower evidence level into a higher one by narrative inference.

## 10. Reference implementation in this repository

The V2 reference primitives live under `traceweave/v2/`:

- `lifecycle.py` — hash-linked START / RESUME / STOP events;
- `provenance.py` — paired causal IDs and destination materialization records;
- `verify.py` — internal chain and publication consistency checks;
- `schema/traceweave-v2.schema.json` — normative JSON shape.

An example object is published at `examples/v2/causal-chain.example.json`.

These V2 primitives are additive. The existing v0.1 checkpoint CLI remains intact while the V2 lifecycle and publication model are evaluated and integrated.

## 11. Core rule

> **Logical IDs correlate. Native destination IDs plus content identity and readback prove materialization. START / RESUME / STOP prove temporal continuity only when their evidence remains linked.**

The purpose of Traceweave V2 is not to prove that a file exists. It is to preserve a reconstructable line from authority and execution through continuity, artifact identity, materialization, and closure.
