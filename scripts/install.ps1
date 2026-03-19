$ErrorActionPreference = "Stop"

if (Test-Path "pyproject.toml") {
    $PkgSpec = "."
} elseif ($env:TRIGGERMIND_ARCHIVE_URL) {
    $PkgSpec = $env:TRIGGERMIND_ARCHIVE_URL
} else {
    Write-Host "[TriggerMind] Not in repo root and TRIGGERMIND_ARCHIVE_URL is not set."
    Write-Host "[TriggerMind] Option A: cd into source folder and run: py -m pip install --user -U ."
    Write-Host "[TriggerMind] Option B: set TRIGGERMIND_ARCHIVE_URL to your GitHub ZIP URL and rerun."
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
