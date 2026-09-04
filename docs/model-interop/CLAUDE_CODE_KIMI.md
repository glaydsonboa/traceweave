# Kimi in Claude Code

Kimi/Moonshot can be used behind Claude Code when your account exposes an Anthropic-compatible Messages endpoint.

Because Moonshot operates different products and regions, keep the base URL and model configurable instead of baking one endpoint into Traceweave.

## Prerequisites

- Claude Code installed
- Moonshot/Kimi API key
- Anthropic-compatible base URL for your account
- model name available to that endpoint

## Windows PowerShell

```powershell
$env:KIMI_API_KEY="..."
$env:KIMI_ANTHROPIC_BASE_URL="PUT_CURRENT_ENDPOINT_HERE"
$env:KIMI_MODEL="PUT_CURRENT_MODEL_HERE"

$env:ANTHROPIC_BASE_URL=$env:KIMI_ANTHROPIC_BASE_URL
$env:ANTHROPIC_AUTH_TOKEN=$env:KIMI_API_KEY

$env:ANTHROPIC_MODEL=$env:KIMI_MODEL
$env:ANTHROPIC_DEFAULT_OPUS_MODEL=$env:KIMI_MODEL
$env:ANTHROPIC_DEFAULT_SONNET_MODEL=$env:KIMI_MODEL
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL=$env:KIMI_MODEL

claude
```

A launcher is included in:

`examples/model-interop/kimi.ps1`

## macOS / Linux

```bash
export KIMI_API_KEY="..."
export KIMI_ANTHROPIC_BASE_URL="PUT_CURRENT_ENDPOINT_HERE"
export KIMI_MODEL="PUT_CURRENT_MODEL_HERE"

export ANTHROPIC_BASE_URL="$KIMI_ANTHROPIC_BASE_URL"
export ANTHROPIC_AUTH_TOKEN="$KIMI_API_KEY"

export ANTHROPIC_MODEL="$KIMI_MODEL"
export ANTHROPIC_DEFAULT_OPUS_MODEL="$KIMI_MODEL"
export ANTHROPIC_DEFAULT_SONNET_MODEL="$KIMI_MODEL"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="$KIMI_MODEL"

claude
```

## Tool-call compatibility test

Run:

```bash
python examples/model-interop/smoke_anthropic.py \
  --base-url "$KIMI_ANTHROPIC_BASE_URL" \
  --api-key "$KIMI_API_KEY" \
  --model "$KIMI_MODEL"
```

The test intentionally asks for the same tool twice in separate turns.

If the smoke test fails:

- do not run unattended `/loop`;
- verify the provider's current Claude Code or Anthropic-compatibility guide;
- verify the region/base URL;
- verify the model;
- test again before real work.

## Traceweave evidence

Record:

```json
{
  "harness": "claude-code",
  "provider": "moonshot",
  "model": "observed-model-name",
  "protocol": "anthropic-messages",
  "tool_pairing_smoke": "passed"
}
```

## Sources

- https://platform.moonshot.ai/
- https://github.com/MoonshotAI
