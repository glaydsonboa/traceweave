param(
  [string]$Project = ".",
  [string]$Model = $(if ($env:DEEPSEEK_MODEL) { $env:DEEPSEEK_MODEL } else { "deepseek-v4-pro" })
)

if (-not $env:DEEPSEEK_API_KEY) {
  throw "Set DEEPSEEK_API_KEY first."
}

$env:ANTHROPIC_BASE_URL = "https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN = $env:DEEPSEEK_API_KEY

$env:ANTHROPIC_MODEL = $Model
$env:ANTHROPIC_DEFAULT_OPUS_MODEL = $Model
$env:ANTHROPIC_DEFAULT_SONNET_MODEL = $Model
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL = $Model

Set-Location $Project
claude
