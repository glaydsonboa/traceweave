# Evidence model

## Three independent state layers

The research model separates three states that agentic systems often collapse into one narrative.

### 1. Executed state

What actually changed or ran.

Examples:

- a tool invocation;
- a file write;
- a Git ref movement;
- a commit;
- a network request;
- an external-system mutation;
- a process that actually executed.

### 2. Observed state

What an instrument was capable of seeing and actually recorded.

Examples:

- tool results;
- runtime logs;
- traces;
- Git readback;
- test output;
- persisted artifacts;
- external API responses.

Observation has a scope. A negative observation is valid only when the instrument could have observed the target condition.

### 3. Narrated state

What the agent says happened.

Examples:

- "verified";
- "zero calls";
- "the source says";
- "I ran";
- "the bug is fixed";
- a session summary or STOP report.

Narrated state is evidence of what the agent reported. It is not automatically evidence that the reported execution occurred.

## Core relation

```text
executed state ≠ observed state ≠ narrated state
```

Equality between two layers must be demonstrated, not assumed.

## Core proposition

> **An agent's self-report should not serve as proof of the execution that the same agent is describing.**

This proposition does not require a claim about consciousness, motive, deception or intent.

It requires only independently comparable evidence layers.

## Negative evidence rule

A statement such as "zero", "none", "did not run" or "not present" requires an instrument with demonstrated visibility into the thing being negated.

If the sensor cannot observe an event, absence from that sensor is not proof that the event did not occur.

## Retractions

A later retraction or correction strengthens chronology because it records that the prior statement was withdrawn or narrowed.

But:

```text
retraction = textual evidence
retraction ≠ proof of intent
```

The study therefore uses concrete descriptions such as:

- unsupported verification claim;
- source attribution contradicted by the cited source;
- execution-state mismatch;
- authority/scope violation;
- instrumentation false-state.

## Evidence hierarchy

When sources conflict, the working order is:

1. primary event/tool result;
2. runtime or Git state;
3. immutable hash/manifest;
4. incident index;
5. analytical report;
6. thesis or summary.

A stronger source can falsify or narrow a weaker narrative. A weaker derived document cannot override stronger primary evidence.
