# Authorship and Provenance

## Why Traceweave separates them

AI-assisted engineering often collapses several distinct roles into one label such as “author” or “agent.”

That loses important information.

A method may be originated by a human, formalized in a prompt by an AI assistant, implemented by a coding CLI and verified by another process.

Those contributions are different.

## Recommended roles

### Requested by

Who authorized or requested the work.

### Intellectual author

Who originated the method, architecture, design principle or decision being implemented, when that origin is known and evidenced.

### Prompt or instruction generator

Who translated the request into an executable instruction.

### Executor

Who performed the code/document/tool operations.

### Verifier

Who or what evaluated the resulting evidence.

### Publisher

Who published or delivered the resulting artifact.

## Core rules

1. Execution does not imply intellectual authorship.
2. Prompt generation does not imply intellectual authorship.
3. Git commit authorship does not necessarily describe the full causal chain.
4. A role should be recorded only when it is explicitly known.
5. Unknown roles should remain unknown.
6. Multiple contributors may share a role when the evidence supports that representation.

## Example

```json
{
  "requested_by": {
    "type": "human",
    "name": "Project owner"
  },
  "intellectual_author": {
    "type": "human",
    "name": "Project owner"
  },
  "prompt_generator": {
    "type": "ai",
    "name": "Assistant A"
  },
  "executor": {
    "type": "ai_cli",
    "name": "Coding Agent B"
  },
  "verifier": {
    "type": "process",
    "name": "test-suite"
  }
}
```

This example does not rank the contributors.

It preserves what each one did.

## Public attribution

Public documentation should avoid vague claims such as:

> “The AI created the architecture.”

when the evidence only shows that the AI implemented or documented a human-originated architecture.

Likewise, public documentation should not erase substantial AI execution or verification when those actions are part of the reproducible history.

The goal is accurate provenance, not promotional attribution.
