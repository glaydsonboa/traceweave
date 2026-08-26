# Causal Commit Guard

## Purpose

Causal Commit Guard prevents a coherent fix from accidentally committing unrelated changes.

A normal `git status` shows what changed. It does not classify why those files changed or whether they belong to the current change boundary.

## Core idea

Create a bounded cause before mutation, then classify repository changes against that baseline.

```bash
traceweave cause start "fix config validation"
traceweave cause include src/config.py
traceweave cause include tests/test_config.py
traceweave cause exclude data/runtime/state.json
traceweave cause status
traceweave cause stage-plan
traceweave cause close
```

Version 0.1 should distinguish:

- pre-existing changes;
- files changed after cause start;
- explicitly declared causal files;
- explicitly excluded files.

It should not infer semantic causality with a model.

## Safety boundary

`stage-plan` should print the exact safe staging command rather than execute it automatically.

```text
CAUSAL STAGE PLAN

include:
  src/config.py
  tests/test_config.py

exclude:
  data/runtime/state.json

command:
  git add -- src/config.py tests/test_config.py
```

This keeps Git mutation under explicit user control while making the causal boundary inspectable and reproducible.
