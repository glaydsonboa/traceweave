# Multi-model architecture without losing provenance

Traceweave's core protocol is provider-neutral. This document defines an optional recipe for users who plan with one model, review with another, and execute through a coding harness backed by a third provider.

## 1. Separate five identities

Do not collapse these into one word such as "agent":

| Identity | Example |
|---|---|
| Human authority | person who approved the work |
| Prompt author | ChatGPT, Gemini, human |
| Planner/reviewer | DeepSeek, Kimi, Claude, Gemini |
| Harness | Claude Code, Codex, Kimi Code |
| Effective model/provider | DeepSeek V4 Pro, Kimi, Gemini |

A terminal may display Claude Code while the effective model is DeepSeek. That is not a contradiction. It is a harness/model split.

## 2. Recommended Traceweave recipe fields

This is a recipe extension, not part of Protocol 0.1:

```json
{
  "ai_workflow": {
    "human_authority": "user",
    "prompt_author": {
      "system": "chatgpt",
      "model": "unknown"
    },
    "planning": [
      {
        "harness": "claude-code",
        "provider": "deepseek",
        "model": "deepseek-v4-pro",
        "mode": "plan"
      }
    ],
    "reviews": [
      {"system": "gemini", "model": "unknown"},
      {"system": "kimi", "model": "unknown"}
    ],
    "execution": {
      "harness": "claude-code",
      "provider": "anthropic",
      "model": "claude-opus"
    }
  }
}
```

Use `unknown`, not inference, when the actual model is not observed.

## 3. Transport boundary

```text
                    ┌──────────────────────┐
                    │     human intent     │
                    └──────────┬───────────┘
                               │
                 ┌─────────────▼─────────────┐
                 │ prompt planning / review │
                 └─────────────┬─────────────┘
                               │
                    execution contract
                               │
             ┌─────────────────▼─────────────────┐
             │            Claude Code            │
             │ harness / tools / terminal loop  │
             └─────────────────┬─────────────────┘
                               │ Anthropic Messages
                ┌──────────────┴───────────────┐
                │                              │
         direct compatible                local bridge
                │                              │
         DeepSeek / Kimi                 OpenAI protocol
                                               │
                                            Gemini
```

## 4. Requested model vs effective model

Compatibility layers often accept a Claude-style model name because the harness expects one.

That label is routing input, not identity.

Record:

```json
{
  "requested_model_alias": "claude-opus",
  "effective_provider": "deepseek",
  "effective_model": "deepseek-v4-pro"
}
```

If the provider maps one visible model name to another effective model, preserve both names.

## 5. Plan/review/execute is a state boundary

A robust workflow treats planning and execution as different technical states.

```text
PLAN
- read
- inspect
- compare
- produce plan
- no mutation

REVIEW
- challenge scope
- find contradictions
- find missing evidence
- find missing tests
- no mutation

EXECUTE
- fresh context where possible
- bounded scope
- explicit acceptance criteria
- tests
- Git evidence
```

The output of one stage is an artifact consumed by the next stage.

Traceweave should preserve the artifact's provenance, not the private chain of thought that produced it.

## 6. Compatibility must be testable

A provider bridge is not "working" because a text answer appeared.

Minimum proof:

```text
authentication
→ text response
→ tool_use #1
→ tool_result #1
→ tool_use #2
→ tool_result #2
→ final response
```

This catches protocol defects that only appear after the first tool turn.

## 7. Public boundary

Traceweave should not need to become the router.

A clean public boundary is:

```text
provider/harness decides how work runs
Traceweave records what actually ran
```

That preserves the project's continuity-first positioning while still documenting multi-model engineering workflows.
