# Traceweave — Model Interop Recipes

> **Use the harness you like, the model you choose, and preserve the handoff as evidence.**

These recipes show how to run non-Anthropic models behind **Claude Code's terminal harness** while keeping the provider/model identity explicit.

This is an **optional interoperability layer**. It does not change Traceweave's core boundary: Traceweave remains a continuity and provenance protocol, not a model router.

## The distinction that matters

```text
Claude Code = coding harness / agent loop / terminal UX

DeepSeek
Kimi
Gemini     = model providers

Anthropic Messages API
OpenAI Chat Completions = wire protocols

Traceweave = evidence / provenance / continuity
```

A compatible endpoint can make Claude Code talk to another provider without making that provider "Claude". The harness and the model are separate facts.

Traceweave should record both:

```json
{
  "harness": "claude-code",
  "requested_model_alias": "claude-opus-5",
  "effective_provider": "deepseek",
  "effective_model": "deepseek-v4-pro",
  "protocol": "anthropic-messages"
}
```

Never treat a model alias as proof of model identity.

## Supported patterns

### Pattern A — direct Anthropic-compatible provider

Use this when the provider exposes an Anthropic-compatible Messages API.

```text
Claude Code
    |
    | Anthropic Messages
    v
Provider endpoint
    |
    v
Model
```

Current examples:

- DeepSeek — first-party Anthropic compatibility and a first-party Claude Code guide.
- Kimi — Moonshot/Kimi publishes Anthropic-compatible API support; verify the endpoint and model for your region/account before use.

See:

- [DeepSeek in Claude Code](CLAUDE_CODE_DEEPSEEK.md)
- [Kimi in Claude Code](CLAUDE_CODE_KIMI.md)

### Pattern B — transparent local compatibility bridge

Use this when the provider exposes OpenAI compatibility but not the Anthropic protocol expected by Claude Code.

```text
Claude Code
    |
    | Anthropic Messages
    v
Local compatibility bridge
    |
    | OpenAI-compatible Chat Completions
    v
Provider
```

The included Gemini bridge is intentionally small and inspectable. It translates the protocol; it does not pretend that Gemini is an Anthropic model.

See [Gemini in Claude Code](CLAUDE_CODE_GEMINI.md).

## Why this belongs in Traceweave

The important public idea is not "run every model everywhere."

It is:

> **A multi-model engineering session should remain reconstructable even when the planner, reviewer, prompt author, harness and executor are different systems.**

Traceweave can preserve:

```text
human intent
    ↓
planning model
    ↓
prompt reviewer
    ↓
prompt synthesizer
    ↓
coding harness
    ↓
effective model/provider
    ↓
tests
    ↓
Git
    ↓
checkpoint
```

If a stage did not exist, record `null`. If a model/provider was not observed, record `unknown`.

## Security rules

1. Never commit API keys.
2. Prefer environment variables or OS secret stores.
3. Treat the included bridge as trusted-local-only: it does not authenticate clients and must remain bound to `127.0.0.1`.
4. Do not expose a generic unauthenticated `execute_shell(command)` endpoint.
5. Record provider/model identity separately from harness identity.
6. Run a tool-use smoke test before unattended loops.
7. If a compatibility layer drops a field, fail visibly instead of silently discarding it.

## Verification before real work

For every provider:

1. prove authentication;
2. prove model identity from the provider response where available;
3. prove a normal text turn;
4. prove one tool call;
5. prove a second tool call in the same conversation;
6. prove tool-result pairing;
7. prove streaming or explicitly document that the adapter buffers;
8. only then use Plan Mode or long-running loops.

See `examples/model-interop/smoke_anthropic.py`.

## Prompt workflow

The interoperability layer solves transport. It does not solve prompt quality.

For the planning → review → execution workflow, see:

- [Multi-model prompt pipeline](PROMPT_PIPELINE.md)

## Upstream references

Verify current provider documentation before production use:

- DeepSeek Claude Code integration:
  https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code/
- DeepSeek Anthropic API compatibility:
  https://api-docs.deepseek.com/guides/anthropic_api/
- Moonshot/Kimi:
  https://platform.moonshot.ai/
- Google Gemini OpenAI compatibility:
  https://ai.google.dev/gemini-api/docs/openai
- Google Gemini model catalog:
  https://ai.google.dev/gemini-api/docs/models
- Anthropic prompting best practices:
  https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables
