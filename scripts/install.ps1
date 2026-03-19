$ErrorActionPreference = "Stop"

if ($env:TRIGGERMIND_ARCHIVE_URL) {
    $PkgSpec = $env:TRIGGERMIND_ARCHIVE_URL
} elseif (Test-Path "pyproject.toml") {
    $PkgSpec = "."
} else {
    Write-Host "[TriggerMind] TRIGGERMIND_ARCHIVE_URL is not set."
    Write-Host "[TriggerMind] Set it to your ZIP URL, e.g."
    Write-Host "[TriggerMind] $env:TRIGGERMIND_ARCHIVE_URL='https://github.com/<YOUR_ORG>/triggermind/archive/refs/heads/main.zip'"
    exit 1
}

if (Get-Command py -ErrorAction SilentlyContinue) {
    Write-Host "[TriggerMind] Installing with pip (py launcher)..."
    py -m pip install --user -U $PkgSpec
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "[TriggerMind] Installing with pip (python)..."
    python -m pip install --user -U $PkgSpec
} else {
    Write-Host "[TriggerMind] Python 3.10+ is required."
    exit 1
}

Write-Host "[TriggerMind] Installed. Run: triggermind"
