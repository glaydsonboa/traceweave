# Starts TraceTrack in THIS window, so the PROMPT_ID of each job shows up here, where you can read it.
# Usage: pwsh -NoExit -File tools/start-tracetrack.ps1 [-Workdir C:\path\to\project] [-Port 7317]
param(
    [string]$Workdir = (Split-Path -Parent $PSScriptRoot),
    [int]$Port = 7317
)
$root = Split-Path -Parent $PSScriptRoot
$python = "C:\Users\Glaydson\Tools\traceweave\.venv\Scripts\python.exe"
$env:PYTHONPATH = $root
$env:PYTHONIOENCODING = "utf-8"
# DeepSeek runs through tools/run-deepseek-job.ps1 (key read from the Worion Vault, never stored).
$env:TRACETRACK_CMD_DEEPSEEK = ConvertTo-Json -Compress @(
    "pwsh", "-NoLogo", "-NoProfile", "-File", (Join-Path $root "tools\run-deepseek-job.ps1"), "{prompt}")
$Host.UI.RawUI.WindowTitle = "TraceTrack :$Port — PROMPT_IDs aparecem aqui"
Write-Host "TraceTrack: os PROMPT_IDs dos jobs aparecem NESTA janela." -ForegroundColor Cyan
& $python -m traceweave.cli tracetrack --port $Port --workdir $Workdir --repo $Workdir
