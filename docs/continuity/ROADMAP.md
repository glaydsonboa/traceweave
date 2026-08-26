# Roadmap — Continuity-First Small Tools

## Principle

Build the smallest independently demonstrable solutions first. Do not make progress depend on proving multi-agent orchestration.

## Phase 1 — Continuity Guard

Deliver `traceweave stop`, `traceweave resume`, current Git drift detection, open/completed items, checkpoint verification, tests, and a neutral demo repository.

**Exit criterion:** a clean two-session demo reproduces the last verified state and detects a changed HEAD.

## Phase 2 — Resume Capsule

Deliver projection from a Traceweave checkpoint, YAML/JSON artifact, completed/open/decision/do-not-reopen/unknown states, verification, and portable handoff text.

**Exit criterion:** a capsule generated from a checkpoint remains factually stable after repository drift and reports that drift separately.

## Phase 3 — Causal Commit Guard

Deliver cause start, pre-existing change snapshot, include/exclude, status classification, safe stage plan, and no automatic staging in v0.1.

**Exit criterion:** a fixture with mixed causal/runtime/pre-existing files produces the exact safe stage set.

## Phase 4 — Stale Artifact Guard

Deliver a manifest convention, Git HEAD comparison, `synced`/`stale`/`unknown`/`not_applicable` states, exit codes, and a CI-friendly command.

**Exit criterion:** an artifact moves deterministically through `synced → stale → synced` across source commit/rebuild.

## Phase 5 — Header Contract Linter

Deliver config schema, required/ordered fields, duplicate detection, path existence checks, enum validation, and short/full header policies.

**Exit criterion:** fixtures deterministically report missing, duplicate, invalid, and stale-reference header errors.

## Integration rule

Each tool should be independently useful before integration. Shared concepts may later converge under the `traceweave` CLI and checkpoint schema, but no phase should require a daemon, database, cloud service, model API, or orchestration layer.
