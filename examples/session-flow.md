# Traceweave — Minimal Session Flow

This example shows one complete Traceweave session without requiring a Traceweave application.

## Scenario

A developer asks an AI coding agent to add validation for a required API URL.

Repository: `example/traceweave-demo`  
Branch: `feature/config-validation`  
Starting commit: `2f1a83c`

## 1. Session start

Create a stable session identifier:

`session-20260821-demo`

Record the requester, prompt generator, executor, repository, branch and base commit.

## 2. Provenance

The causal chain is:

`Example User → ChatGPT → Codex CLI → code change`

Meaning:

1. the human requested the change;
2. ChatGPT formulated the technical instruction;
3. Codex CLI executed the change;
4. files, tests and Git provide evidence.

No authorship is inferred beyond that chain.

## 3. Execution

The executor changes:

- `src/config.js`
- `tests/config.test.js`

Result:

> Missing required API URL is rejected during configuration loading.

## 4. Test

Command:

`npm test -- config.test.js`

Observed result:

`4 tests passed`

Traceweave records the command and observed result.

## 5. Commit

The verified change is committed:

`7c91b4e fix: validate required API URL`

Git state:

- branch: `feature/config-validation`
- base: `2f1a83c`
- head: `7c91b4e`
- working tree: `clean`

## 6. Graph synchronization

The structural graph is verified against:

`7c91b4e`

Recorded state:

- engine: `graphify`
- status: `synced`
- source commit: `7c91b4e`

Invariant for this checkpoint:

`git.head_commit == graph_sync.source_commit`

## 7. Checkpoint

The session writes:

[`checkpoint.json`](checkpoint.json)

The checkpoint now contains enough information to answer:

- what work was requested;
- who participated;
- what files changed;
- what test ran;
- whether it passed;
- which commit contains the result;
- whether the code graph represents the same revision.

## 8. Reconstruction

A later human or agent can reconstruct the technical state without reading the original chat transcript.

Minimal reconstruction path:

`checkpoint → Git commit → changed files → test command → graph revision`

That is the core Traceweave behavior.

## 9. Minimal implementation contract

A future Traceweave CLI only needs to automate what this example already demonstrates manually:

1. capture session metadata;
2. capture provenance;
3. read Git state;
4. collect test evidence;
5. verify graph state;
6. write the checkpoint.

No larger platform is required for the protocol to be useful.
