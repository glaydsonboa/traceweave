# Gemini in Claude Code

Google publishes an OpenAI-compatible Gemini endpoint.

Claude Code speaks Anthropic Messages, so a transparent approach is:

```text
Claude Code
    |
    | Anthropic Messages
    v
local compatibility bridge
    |
    | OpenAI Chat Completions
    v
Gemini API
```

Do not label this as "Gemini pretending to be Opus." It is protocol translation.

## Install the local bridge

```bash
cd examples/model-interop
python -m venv .venv
```

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Set your key and current Gemini model:

Windows:

```powershell
$env:GEMINI_API_KEY="..."
$env:UPSTREAM_API_KEY=$env:GEMINI_API_KEY
$env:UPSTREAM_MODEL="PUT_CURRENT_GEMINI_MODEL_HERE"
python .\anthropic_openai_bridge.py
```

macOS / Linux:

```bash
export GEMINI_API_KEY="..."
export UPSTREAM_API_KEY="$GEMINI_API_KEY"
export UPSTREAM_MODEL="PUT_CURRENT_GEMINI_MODEL_HERE"
python ./anthropic_openai_bridge.py
```

The bridge listens only on:

`http://127.0.0.1:4010`

It does not authenticate local clients. Treat it as a trusted-local reference and do not expose it on a network interface.

## Point Claude Code at the bridge

Windows:

```powershell
$env:ANTHROPIC_BASE_URL="http://127.0.0.1:4010"
$env:ANTHROPIC_AUTH_TOKEN="local-bridge"
$env:GEMINI_MODEL="PUT_CURRENT_GEMINI_MODEL_HERE"

$env:ANTHROPIC_MODEL=$env:GEMINI_MODEL
$env:ANTHROPIC_DEFAULT_OPUS_MODEL=$env:GEMINI_MODEL
$env:ANTHROPIC_DEFAULT_SONNET_MODEL=$env:GEMINI_MODEL
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL=$env:GEMINI_MODEL

claude
```

macOS / Linux:

```bash
export ANTHROPIC_BASE_URL="http://127.0.0.1:4010"
export ANTHROPIC_AUTH_TOKEN="local-bridge"
export GEMINI_MODEL="PUT_CURRENT_GEMINI_MODEL_HERE"

export ANTHROPIC_MODEL="$GEMINI_MODEL"
export ANTHROPIC_DEFAULT_OPUS_MODEL="$GEMINI_MODEL"
export ANTHROPIC_DEFAULT_SONNET_MODEL="$GEMINI_MODEL"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="$GEMINI_MODEL"

claude
```

## What the example bridge translates

Supported:

- system text;
- user/assistant text;
- Anthropic tool definitions → OpenAI function tools;
- `tool_use` → OpenAI `tool_calls`;
- `tool_result` → OpenAI `tool` messages;
- OpenAI tool calls → Anthropic `tool_use`;
- normal non-stream responses;
- Anthropic-compatible SSE output, buffered from one upstream completion;
- token usage where the provider returns it.

Intentionally explicit limitations:

- streaming is buffered, not token-by-token from Gemini;
- image/document content blocks are rejected instead of silently dropped;
- provider-specific beta fields are not emulated;
- prompt caching semantics are not fabricated;
- computer-use/browser beta contracts are outside this minimal example.

This is a reference bridge, not a claim of full Claude API parity.

## Smoke test

```bash
python smoke_anthropic.py \
  --base-url http://127.0.0.1:4010 \
  --api-key local-bridge \
  --model "$GEMINI_MODEL"
```

Only start unattended agent loops after the tool-pairing test passes.

## Sources

- https://ai.google.dev/gemini-api/docs/openai
- https://ai.google.dev/gemini-api/docs/models
