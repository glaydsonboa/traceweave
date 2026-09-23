# Dual provenance boundary

## Purpose

“Dual provenance” can describe two different mechanisms. Treating them as one
creates a false proof boundary.

Traceweave separates:

```text
independent custody mirror ≠ paired external publication
```

## 1. Independent custody mirror

A custody mirror preserves the same source bytes in a separately controlled
location so that one writer cannot silently remove both copies.

```text
native source
→ stable snapshot
→ source SHA-256 and byte count
→ independently identified replica
→ replica SHA-256 and byte count
→ readback
```

A confirmed custody mirror requires:

- exact source and replica SHA-256 equality;
- exact byte-count equality;
- a native identity for the replica;
- confirmed readback;
- overwrite protection or an equivalent append-only guarantee.

Custody proves preservation of bytes. It does not prove that the recorded
narrative is correct, that an external publication exists, or that two
destinations share one causal update.

## 2. Paired external publication

A publication pair correlates projections of one causal update:

```text
PAIR_KEY
├── GITHUB_ID → native Git identity → content identity → readback
└── NOTION_ID → native Notion identity → content identity → readback
```

The logical IDs are correlation identities. They are not receipts. The pair is
confirmed only after both destinations independently satisfy their
materialization contract.

Publication proves external materialization. It does not prove that the source
also has an independently controlled custody copy.

## 3. Byte identity is not visual similarity

Renderers, terminals and text APIs can normalize or append line endings. These
two payloads can look identical in a UI while being different artifacts:

```text
payload A: "same visible line\n"
payload B: "same visible line\n\r\n"
```

They differ by two bytes and have different SHA-256 values. A byte-identical
claim therefore requires readback of the actual destination artifact, not a
comparison of rendered text.

Traceweave V2 exposes this rule through `compare_bytes`,
`record_custody_mirror`, `custody_mirrored`, schema-level custody records, and
verification errors for hash or byte-count divergence.

## 4. Source code must remain an artifact

When a publication contains Python, JavaScript or another source file, a code
block is a view, not the artifact.

Each confirmed source materialization must preserve:

- the native filename and extension;
- byte length;
- SHA-256;
- a download reference;
- destination-native identity and readback.

Copy-to-clipboard is useful. It is not a substitute for a downloadable file
whose bytes can be verified.

## 5. Header mutation boundary

Header validation has two responsibilities:

1. the prompt or change contract must explicitly require applicable source
   headers to be reconciled when a file is changed;
2. the executor must update the header to describe the post-change state or
   report why the repository policy does not apply.

A structural linter can verify presence, order and allowed values. It cannot
prove that prose about runtime behavior is true. Semantic claims still require
code, tests, runtime evidence or another capable sensor.

## 6. Failure classification

Use separate states:

```text
CUSTODY_CONFIRMED
CUSTODY_PARTIAL
PUBLICATION_CONFIRMED
PUBLICATION_PARTIAL
BYTE_IDENTITY_FAILED
SOURCE_ARTIFACT_NOT_DOWNLOADABLE
```

Never promote one state into another by narrative inference.
