# Traceweave — Public Session Flow Example

This example demonstrates the public Traceweave method without requiring a production Traceweave system.

All names, identifiers and repository details are fictitious.

## Scenario

A developer requests validation for a required service URL.

Repository:

`example/traceweave-demo`

Branch:

`feature/config-validation`

Starting commit:

`2f1a83c`

## 1. Request

Observed request:

> Add validation so startup fails clearly when the required service URL is missing.

Traceweave records the bounded objective.

It does not infer additional architectural goals.

## 2. Session identity

Example:

```json
{
  "session_id": "session-20260823-demo",
  "repository": "example/traceweave-demo",
  "branch": "feature/config-validation",
  "base_commit": "2f1a83c"
}
```

## 3. Provenance

Example roles:

```text
request authority
→ instruction generator
→ executor
→ verifier
```

For this fictitious session:

```json
{
  "requested_by": {"type": "human", "name": "Example Maintainer"},
  "intellectual_author": {"type": "human", "name": "Example Maintainer"},
  "prompt_generator": {"type": "ai", "name": "Example Assistant"},
  "executor": {"type": "ai_cli", "name": "Example Coding CLI"},
  "verifier": {"type": "process", "name": "test-suite"}
}
```

These are distinct roles.

No role is inferred from the name of another role.

## 4. Current-state inspection

Before editing, the executor observes:

- branch: `feature/config-validation`;
- HEAD: `2f1a83c`;
- working tree: clean;
- existing validation tests: 3 passing;
- no test currently covers a missing service URL.

This is a checkpointable observation, not yet a diagnosis.

## 5. Hypothesis

Hypothesis:

> Startup accepts an empty service URL because the configuration loader checks only whether the key exists, not whether its normalized value is non-empty.

This is still an inference.

## 6. Adversarial test

Before changing production code, add or run a focused test that would fail only if the suspected condition exists.

Observed result:

```text
test_missing_service_url
expected: startup error
observed: startup succeeds
result: failed
```

The failure supports the hypothesis.

## 7. Minimal correction

Changed files:

- `src/config.py`
- `tests/test_config.py`

The correction validates the normalized value at the configuration boundary.

No unrelated refactor is included.

## 8. Regression

Command:

```bash
python -m pytest tests/test_config.py
```

Observed result:

```text
4 passed
```

Traceweave records the command and observed result.

It does not invent results for tests that were not executed.

## 9. Git state

The verified change is committed:

```text
7c91b4e fix: validate required service URL
```

Observed state:

```json
{
  "branch": "feature/config-validation",
  "base_commit": "2f1a83c",
  "head_commit": "7c91b4e",
  "working_tree": "clean"
}
```

This proves repository state.

It does not yet prove external delivery.

## 10. Optional structural state

Assume the project uses a fictitious structural index.

After rebuilding it:

```json
{
  "engine": "example-structural-tool",
  "status": "synced",
  "source_commit": "7c91b4e"
}
```

If the index instead still referenced `2f1a83c`, the correct state would be `stale`.

Traceweave does not require this step when structural tooling is not applicable.

## 11. Checkpoint

The session can now create a checkpoint containing:

- session identity;
- provenance;
- bounded work summary;
- changed files;
- test result;
- Git state;
- optional structural state;
- status.

A reasonable status is:

```json
{
  "status": "complete"
}
```

Here `complete` means:

> complete for the checkpoint boundary that required the focused change, tests and local Git state.

It does **not** mean the feature has been deployed.

## 12. Delivery proof

If the requirement also says “publish the change to the remote repository,” then a local commit is insufficient.

A later observation might record:

```json
{
  "delivery_proof_id": "delivery-demo-001",
  "type": "remote_commit_readback",
  "revision": "7c91b4e",
  "result": "confirmed"
}
```

Only then can the evidence trail claim that the expected remote delivery was observed.

The public Reference Demonstration v0.1 does not implement a production delivery-proof engine; this section demonstrates the protocol distinction.

## 13. Reconstruction

A later reviewer should be able to follow:

```text
checkpoint
→ request
→ provenance
→ changed files
→ test evidence
→ Git revision
→ optional structural state
→ optional delivery proof
```

The reviewer does not need to trust the original conversation.

The evidence trail is the continuity mechanism.

## 14. What this example intentionally does not reveal

This public example does not include:

- private infrastructure;
- private project identifiers;
- proprietary orchestration;
- proprietary validation mechanisms;
- production integration details;
- unpublished heuristics.

Its purpose is to teach the protocol, not reconstruct a private implementation.
