# Runs DeepSeek V4 Pro inside the Claude Code harness and writes stream-json to stdout.
# Usage: pwsh -File tools/run-deepseek-job.ps1 "<prompt>"
# Read-only tools. Runs in the current directory. The key is read from the Worion Vault (ID 52) into this
# process's environment only; it is never written to a file or printed, and is removed on exit.
param([Parameter(Mandatory, Position = 0)] [string]$Prompt)
$ErrorActionPreference = "Stop"
$canonical = if ($env:WORION_CANONICAL) { $env:WORION_CANONICAL } else { "C:\Users\user\worion-desktop\.worktrees\canonical" }
$loader = @"
const { getModelVaultConfig } = require('$($canonical.Replace('\', '/'))/scripts/model-vault.js');
getModelVaultConfig('deepseek').then((c) => {
  if (c.vaultId !== 52 || c.provider !== 'deepseek' || !c.apiKey) process.exit(2);
  process.stdout.write(String(c.apiKey));
}).catch(() => process.exit(3));
"@
$here = (Get-Location).Path
Push-Location $canonical
try { $key = (& node -e $loader 2>$null | Out-String).Trim() } finally { Pop-Location }
if (-not $key) { [Console]::Error.WriteLine("run-deepseek-job: DeepSeek key unavailable from Vault 52"); exit 3 }
$vars = "ANTHROPIC_MODEL", "ANTHROPIC_DEFAULT_OPUS_MODEL", "ANTHROPIC_DEFAULT_SONNET_MODEL",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL", "CLAUDE_CODE_SUBAGENT_MODEL"
try {
    $env:ANTHROPIC_BASE_URL = "https://api.deepseek.com/anthropic"
    $env:ANTHROPIC_AUTH_TOKEN = $key
    Remove-Variable key
    # Pro only: deepseek-v4-flash is retired (Worion DECISOES_VIVAS 2026-08-17).
    foreach ($v in $vars) { Set-Item "Env:\$v" "deepseek-v4-pro[1m]" }
    Set-Location $here
    & claude -p $Prompt --output-format stream-json --verbose --setting-sources project `
        --allowedTools Read `
        --disallowedTools "Bash PowerShell Write Edit NotebookEdit Skill Agent WebFetch WebSearch"
    exit $LASTEXITCODE
} finally {
    foreach ($v in @("ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN") + $vars) {
        Remove-Item "Env:\$v" -ErrorAction SilentlyContinue
    }
}
