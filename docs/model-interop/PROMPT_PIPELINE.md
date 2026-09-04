# Multi-model prompt pipeline

> **Use models for different jobs, but keep one execution contract.**

The purpose of a multi-model workflow is not to make prompts longer. It is to remove ambiguity before expensive execution begins.

## 1. The pipeline

```text
human intent
    ↓
verified context capsule
    ↓
planning model
    ↓
independent prompt reviewers
    ↓
prompt synthesizer
    ↓
fresh execution context
    ↓
coding model / harness
    ↓
tests + Git + checkpoint
```

A practical division of labor can be:

```text
cheap/high-context model  → repeated exploration and Plan Mode
review models             → contradictions, missing evidence, missing tests
prompt synthesizer        → one locked execution contract
strong coding model       → bounded implementation
Traceweave                → provenance and evidence across all handoffs
```

The provider names are interchangeable. The architecture is the important part.

## 2. Start with a context capsule, not a transcript dump

A useful session bootstrap contains only:

```text
A. repository / branch / source cutoff
B. rules that must not change
C. verified state from the prior session
D. open questions
E. current task
F. forbidden scope
```

Do not make conversational memory the only source of truth.

If a fact matters, point to an artifact, commit, test, trace or file.

## 3. Use Plan Mode to discover, not to code

A planning prompt should say explicitly:

```text
READ ONLY.
Do not implement.
Do not edit.
Do not commit.

Investigate the real path first.
Separate fact, interpretation and hypothesis.
Produce a plan with acceptance criteria.
Ask only when intent cannot be recovered from evidence.
```

The planning model should answer:

```text
where is the first divergence?
what proves it?
what is still unknown?
what is the smallest causal patch?
what test would fail before and pass after?
what must not be mixed into this patch?
```

## 4. Review the prompt, not the code, before execution

Give the planned execution contract to independent reviewers.

Do **not** ask each reviewer to rewrite the whole prompt.

Use this:

```text
Review this execution prompt.

Return only:
1. contradictions;
2. missing context that changes implementation;
3. missing evidence requirements;
4. missing negative/edge tests;
5. scope leaks;
6. acceptance criteria that are not binary;
7. assumptions presented as facts.

Do not redesign the task unless one of those defects requires it.
```

This creates deltas instead of five competing prompts.

## 5. Synthesize once

The final prompt author receives:

- original intent;
- verified context;
- plan;
- reviewer deltas;
- explicit human decisions.

The final result should be one execution contract.

## 6. Recommended execution-prompt structure

```xml
<role>
You are the implementation executor for one bounded cause.
</role>

<source_cutoff>
Repository:
Branch:
HEAD:
Relevant artifacts:
</source_cutoff>

<context>
Only verified facts needed for this patch.
</context>

<closed_facts>
Facts already resolved. Do not reopen without contradictory evidence.
</closed_facts>

<task>
Exactly one cause to implement.
</task>

<constraints>
What must be preserved.
What is forbidden.
Files/systems that are out of scope.
</constraints>

<evidence_required>
Structural proof:
Behavioral proof:
Runtime proof:
Effect proof:
</evidence_required>

<tests>
Positive:
Negative:
Regression:
Mutation/contradiction test if useful:
</tests>

<acceptance>
PASS iff:
FAIL iff:
</acceptance>

<delivery>
Required files/commits/report fields.
</delivery>
```

XML is not magic. Its value is separating instruction classes so the model does not confuse context with commands.

## 7. Put long context before the actual task

For very large contexts, place long documents/context first and the query/instructions after them when the model's guidance recommends this.

A practical order:

```text
long evidence
→ compact state summary
→ task
→ constraints
→ acceptance
```

## 8. Examples beat adjectives

Instead of:

```text
be extremely careful and complete
```

give one or more examples of the failure you want prevented.

For ambiguous formats, a few diverse examples are usually more useful than emphatic adjectives.

## 9. Improve prompts by adding boundaries, not hype

Weak:

```text
Do a complete and perfect refactor. Think deeply.
```

Stronger:

```text
Only change the producer/consumer mismatch described below.
Do not touch routing, UI or persistence.
Before editing, prove which field is produced and which field is consumed.
The patch is accepted only if the old failure is reproduced and the new test passes.
```

## 10. Separate four proof classes

For technical work, require the prompt to distinguish:

```text
STRUCTURAL
What the code can do.

BEHAVIORAL
What the test/harness demonstrated.

RUNTIME
What the real running path executed.

EFFECT
What changed at the final consumer/output.
```

A green unit test is not automatically runtime proof.

## 11. Freeze human decisions before execution

If Plan Mode asks:

```text
A or B?
```

record the decision in the final prompt.

Do not force the execution model to infer it again.

## 12. Fresh execution context

A clean execution context is often useful after long planning:

```text
minimal rules
+ verified previous-session capsule
+ final execution prompt
```

This removes obsolete debate from the coding context while preserving the decisions that survived review.

## 13. Preserve provenance instead of private reasoning

Traceweave should preserve:

```text
who requested
who planned
who reviewed
who authored the final prompt
who executed
what tests ran
what commit represents the result
```

It should not require private chain-of-thought from any model.

Store concise rationale, decisions and evidence instead.

## 14. Example provenance recipe

```json
{
  "requested_by": {
    "type": "human",
    "name": "Example User"
  },
  "prompt_generation": [
    {
      "stage": "draft",
      "system": "chatgpt",
      "model": "unknown"
    },
    {
      "stage": "review",
      "system": "gemini",
      "model": "unknown"
    },
    {
      "stage": "plan",
      "harness": "claude-code",
      "provider": "deepseek",
      "model": "deepseek-v4-pro"
    }
  ],
  "executor": {
    "harness": "claude-code",
    "provider": "anthropic",
    "model": "claude-opus"
  }
}
```

This is a recipe extension, not a Protocol 0.1 requirement.

## 15. The shortest useful rule

> **Plan broadly. Decide explicitly. Execute narrowly. Verify from evidence.**
