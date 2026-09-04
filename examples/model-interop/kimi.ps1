param(
  [string]$Project = ".",
  [string]$BaseUrl = $(if ($env:KIMI_ANTHROPIC_BASE_URL) { $env:KIMI_ANTHROPIC_BASE_URL } else { "PUT_CURRENT_ENDPOINT_HERE" }),
  [string]$Model = $(if ($env:KIMI_MODEL) { $env:KIMI_MODEL } else { "PUT_CURRENT_MODEL_HERE" })
)

if (-not $env:KIMI_API_KEY) {
  throw "Set KIMI_API_KEY first."
}

$env:ANTHROPIC_BASE_URL = $BaseUrl
$env:ANTHROPIC_AUTH_TOKEN = $env:KIMI_API_KEY

$env:ANTHROPIC_MODEL = $Model
$env:ANTHROPIC_DEFAULT_OPUS_MODEL = $Model
$env:ANTHROPIC_DEFAULT_SONNET_MODEL = $Model
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL = $Model

Set-Location $Project
claude
