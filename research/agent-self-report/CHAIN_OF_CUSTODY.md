# Chain of custody

This page describes the evidence path used for the research candidate before the large corpus is released.

## 1. Backup inputs

Backup inputs are inventoried and SHA-256 hashed before transformation.

The rebuilt candidate has a deterministic source snapshot:

```text
SOURCE_SNAPSHOT_SHA256
fa8ef1294eca85750e850210b50854ebe619e335f63308b9d1e2880a6d8e25e4
```

Build identifier:

```text
TRACEWEAVE-BUILD-20260919-fa8ef1294eca
```

## 2. Primary session recovery

Eleven sessions are reconstructed from preserved original Claude Code JSONL backup material and checked against pre-format source metadata.

Three later sessions use recovered near-primary material because the final original RAW bytes did not survive the workstation format. Those sessions are explicitly evidence class B.

## 3. Structural sanitization

Public JSONL is not sanitized with regex over serialized JSON.

The process is:

```text
JSON line
→ parse object
→ recursively sanitize string values
→ serialize object
→ validate JSON
```

This preserves JSON structure while allowing deterministic redaction.

## 4. Validation

Every public transcript must parse one JSON object per line.

A public build cannot pass while invalid JSON lines remain.

## 5. Derived evidence

Incident cards, prompt-ID mappings and Markdown views are derived from validated public JSONL.

Derived evidence never replaces its primary pointer.

## 6. Git provenance

Git evidence is read independently from the private historical repository in read-only mode.

The 077a14e2 case demonstrates:

- a STOP artifact in Git;
- transcript presence in a historical commit;
- later transcript update;
- later path migration;
- matching observed Git blob SHA across the update-to-migration boundary.

See [provenance/077a14e2.md](provenance/077a14e2.md).

## 7. Frozen release

The large corpus release will add:

- the sanitized transcript set;
- all 36 incident cards;
- prompt/event maps;
- redaction manifests;
- SHA256SUMS;
- corpus-freeze metadata;
- verification code;
- explicit recovery notes.

Until that release is attached, these public case files are methodological indexes into the frozen publication candidate, not substitutes for the complete corpus.
