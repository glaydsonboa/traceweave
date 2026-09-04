# DeepSeek in Claude Code

DeepSeek can be used behind Claude Code when its endpoint exposes an Anthropic-compatible Messages API.

## Prerequisites

- Node.js 18+
- Claude Code installed
- DeepSeek API key
- current DeepSeek Anthropic-compatible endpoint and model name

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

## Windows PowerShell

Set the current provider values from DeepSeek's documentation:

```powershell
$env:DEEPSEEK_API_KEY="..."

$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN=$env:DEEPSEEK_API_KEY

$env:DEEPSEEK_MODEL="deepseek-v4-pro"

$env:ANTHROPIC_MODEL=$env:DEEPSEEK_MODEL
$env:ANTHROPIC_DEFAULT_OPUS_MODEL=$env:DEEPSEEK_MODEL
$env:ANTHROPIC_DEFAULT_SONNET_MODEL=$env:DEEPSEEK_MODEL
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL=$env:DEEPSEEK_MODEL

claude
```

A ready-to-edit launcher is in:

`examples/model-interop/deepseek.ps1`

## macOS / Linux

```bash
export DEEPSEEK_API_KEY="..."

export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
export ANTHROPIC_AUTH_TOKEN="$DEEPSEEK_API_KEY"

export DEEPSEEK_MODEL="${DEEPSEEK_MODEL:-deepseek-v4-pro}"

export ANTHROPIC_MODEL="$DEEPSEEK_MODEL"
export ANTHROPIC_DEFAULT_OPUS_MODEL="$DEEPSEEK_MODEL"
export ANTHROPIC_DEFAULT_SONNET_MODEL="$DEEPSEEK_MODEL"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="$DEEPSEEK_MODEL"

claude
```

## What is actually happening

A Claude-style harness can talk to a non-Anthropic model through an Anthropic-compatible protocol.

A visible Claude model label is **not** proof that an Anthropic model ran.

Record both the harness and effective provider:

```json
{
  "harness": "claude-code",
  "provider": "deepseek",
  "model": "deepseek-v4-pro",
  "protocol": "anthropic-messages"
}
```

## Plan-mode workflow

For architecture or review work:

```text
1. start with a minimal context file;
2. restore only the verified prior checkpoint / transcript summary;
3. enter Plan Mode;
4. ask the model to investigate before proposing edits;
5. review the plan outside the execution context;
6. execute only after scope and acceptance criteria are frozen.
```

## Smoke test

Before unattended loops:

```bash
python examples/model-interop/smoke_anthropic.py \
  --base-url https://api.deepseek.com/anthropic \
  --api-key "$DEEPSEEK_API_KEY" \
  --model "$DEEPSEEK_MODEL"
```

The smoke test checks two sequential tool calls and rejects duplicate tool-use IDs.

## Sources

- https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code/
- https://api-docs.deepseek.com/guides/anthropic_api/
