# Model interop examples

These examples support the optional Traceweave model-interoperability recipes.

## Direct launchers

### DeepSeek

PowerShell:

```powershell
$env:DEEPSEEK_API_KEY="..."
$env:DEEPSEEK_MODEL="deepseek-v4-pro"
.\deepseek.ps1 C:\path\to\repo
```

Bash:

```bash
export DEEPSEEK_API_KEY="..."
export DEEPSEEK_MODEL="deepseek-v4-pro"
./deepseek.sh /path/to/repo
```

### Kimi

PowerShell:

```powershell
$env:KIMI_API_KEY="..."
$env:KIMI_ANTHROPIC_BASE_URL="PUT_CURRENT_ENDPOINT_HERE"
$env:KIMI_MODEL="PUT_CURRENT_MODEL_HERE"
.\kimi.ps1 C:\path\to\repo
```

Bash:

```bash
export KIMI_API_KEY="..."
export KIMI_ANTHROPIC_BASE_URL="PUT_CURRENT_ENDPOINT_HERE"
export KIMI_MODEL="PUT_CURRENT_MODEL_HERE"
./kimi.sh /path/to/repo
```

Verify your Moonshot/Kimi region endpoint before use.

## Gemini compatibility bridge

```bash
python -m venv .venv
pip install -r requirements.txt
```

Set:

```text
GEMINI_API_KEY
UPSTREAM_MODEL
```

Then:

```bash
python anthropic_openai_bridge.py
```

Health check:

```bash
curl http://127.0.0.1:4010/health
```

Point Claude Code at:

```text
ANTHROPIC_BASE_URL=http://127.0.0.1:4010
```

## Smoke test

```bash
python smoke_anthropic.py \
  --base-url http://127.0.0.1:4010 \
  --api-key local-bridge \
  --model "$UPSTREAM_MODEL"
```

The smoke test does not execute a shell command. It simulates a `pwd` tool result to verify protocol pairing.

## Boundary

These are reference examples.

They intentionally do not:

- store API keys;
- expose a remote shell;
- claim full Anthropic API parity for the local bridge;
- change Traceweave Protocol 0.1.
