# Traceweave Engineering Method

## Evidence-governed AI-assisted software engineering

Traceweave treats AI-assisted development as a sequence of technical claims that should become progressively stronger as evidence accumulates.

The method is designed to prevent a common failure pattern:

```text
symptom
→ plausible explanation
→ immediate code change
→ report says "fixed"
→ later session discovers the cause was different
```

Traceweave instead uses:

```text
intent
→ current state
→ bounded hypothesis
→ adversarial test
→ cause proved?
→ minimal correction
→ regression/runtime evidence
→ Git state
→ readback
→ checkpoint
```

## 1. Intent

Start from the requested technical outcome.

Record what must change and, equally important, what must not be changed.

Do not silently convert an ambiguous request into a broader architecture task.

## 2. Current state

Inspect the actual state before editing.

Useful sources may include:

- Git revision and working tree;
- source files;
- tests;
- runtime traces;
- structural indexes;
- prior checkpoints;
- recent reports.

A graph or index can navigate the codebase, but the underlying source/runtime remains the confirmation surface.

## 3. Hypothesis

State the smallest causal hypothesis that explains the observed symptom.

A hypothesis is not yet a fact.

Example:

> “The duplicate latency fields may be measuring the same time interval.”

Not:

> “The latency system is broken because both fields are identical.”

## 4. Adversarial test

Try to make the hypothesis fail.

A useful test isolates the suspected cause from neighboring effects.

If the test cannot distinguish two causes, it must not be used to choose between them.

## 5. Cause proof

Only promote the hypothesis when the evidence supports the causal link.

Possible states:

- confirmed;
- derived;
- inferred;
- unknown.

If the cause remains unknown, keep it unknown.

## 6. Minimal correction

Change the smallest surface that repairs the proved cause.

Avoid unrelated cleanup while the causal fix is being validated.

This keeps attribution and regression analysis legible.

## 7. Regression and runtime

Static correctness is not the same as operational acceptance.

Use the strongest available evidence:

- syntax/type checks;
- unit tests;
- targeted regression guards;
- integration tests;
- runtime observation;
- human acceptance when the behavior is user-visible.

## 8. Git state

Once the change is coherent:

- identify the resulting revision;
- record dirty/clean state;
- associate tests with the correct revision;
- avoid claiming delivery merely because a commit exists.

## 9. Readback

When work is expected to exist outside the local workspace, verify the target.

Examples:

- remote commit exists;
- published artifact digest matches;
- deployed version is observable;
- external record can be fetched.

Readback converts “I sent it” into inspectable evidence.

## 10. Checkpoint

Write a compact state that allows reconstruction without rereading an entire conversation.

A checkpoint should answer:

- what was requested;
- what hypothesis was tested;
- what cause was established;
- what changed;
- what evidence ran;
- what revision contains the result;
- what is still unknown or pending.

## 11. Reconciliation

A report should change operational state.

When new evidence arrives:

```text
previous state
→ new evidence
→ resulting state
→ remaining gate
```

Do not leave a solved item open merely because an old backlog was not edited.

Do not close an item merely because a report used the word “resolved.”

## 12. Concurrency

When multiple humans or agents work concurrently:

- identify ownership of the current surface;
- avoid overwriting unrelated work;
- preserve uncommitted evidence;
- record which executor changed which artifact;
- reconcile after each independent workstream closes.

## 13. Why this method matters

The method turns AI assistance from a sequence of persuasive narratives into an inspectable engineering process.

Its central discipline is not “trust the agent.”

It is:

> **Make the agent leave enough evidence that another agent or human does not need to trust it.**
