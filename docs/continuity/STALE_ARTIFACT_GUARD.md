# Stale Artifact Guard

## Purpose

Stale Artifact Guard detects a derived artifact that claims to represent a source revision different from the current repository state.

Examples include code graphs, search indexes, generated catalogs, schema snapshots, API inventories, build manifests, and documentation indexes.

## Core contract

A derived artifact should declare the source state it represents:

```json
{
  "artifact_type": "code_graph",
  "built_at": "2026-08-26T20:00:00Z",
  "source_commit": "abc123",
  "source_fingerprint": null
}
```

The guard compares that declaration with current source state.

## Proposed CLI

```bash
traceweave stale check graphify-out/manifest.json
traceweave stale status
```

## States

- `synced` — declared source revision equals expected source revision;
- `stale` — revisions differ;
- `unknown` — revision cannot be established;
- `not_applicable` — artifact is not revision-based.

The result should be deterministic and CI-friendly. File timestamps alone are not sufficient evidence that an artifact represents the current source revision.
