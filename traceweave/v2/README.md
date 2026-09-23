# Traceweave V2 reference primitives

This package is the additive reference implementation for the **Traceweave V2 — Causal Continuity Protocol**.

V2 extends the current checkpoint model with two linked dimensions:

```text
Temporal continuity:
START → RESUME* → STOP

Cross-destination continuity:
SOURCE → PAIR_KEY → GitHub / Notion → native IDs → readback → closure

Independent custody:
SOURCE BYTES → independently controlled replica → byte/hash readback
```

The implementation deliberately keeps identity layers separate:

```text
session identity
≠ event identity
≠ content identity
≠ causal pair identity
≠ native destination identity
≠ proof of materialization
```

## Python

- `lifecycle.py` — creates hash-linked `START`, `RESUME`, and `STOP` events.
- `provenance.py` — generates paired causal publication IDs and records destination-native materializations.
- `provenance.py` — compares exact bytes and records independently identified custody mirrors.
- `verify.py` — verifies internal lifecycle and publication consistency.
- `_canonical.py` — deterministic JSON serialization and SHA-256 helpers.

Example pair generation:

```bash
python -m traceweave.v2.provenance "publish-transcript"
```

Example lifecycle start:

```bash
python -m traceweave.v2.lifecycle start chain.json \
  --authority "Example Human" \
  --session-id session-001 \
  --repository owner/repo \
  --branch main \
  --head <git-commit>
```

`resume` requires an earlier event SHA as its explicit recovery anchor. `stop` requires a source artifact path and SHA-256.

## JSON

- `schema/traceweave-v2.schema.json` — normative JSON Schema for the causal-chain object.
- `../../examples/v2/causal-chain.example.json` — complete example including lifecycle, paired provenance, native destination identities, and confirmed readback.

## Evidence boundary

The Python verifier proves internal consistency of the object it receives. It does **not** independently fetch GitHub or Notion. External materialization reaches the stronger evidence level only when native destination identities and readback evidence are actually collected by an observer capable of seeing those destinations.

A custody record and a publication pair are intentionally independent. See
[`../../docs/continuity/DUAL_PROVENANCE_BOUNDARY.md`](../../docs/continuity/DUAL_PROVENANCE_BOUNDARY.md).

Full protocol: [`../../docs/TRACEWEAVE_V2.md`](../../docs/TRACEWEAVE_V2.md).
