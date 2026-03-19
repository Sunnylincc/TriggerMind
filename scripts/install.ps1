$ErrorActionPreference = "Stop"
$DefaultArchiveUrl = "https://github.com/Sunnylincc/TriggerMind/archive/refs/heads/main.zip"

if ($env:TRIGGERMIND_ARCHIVE_URL) {
    $PkgSpec = $env:TRIGGERMIND_ARCHIVE_URL
} elseif (Test-Path "pyproject.toml") {
    $PkgSpec = "."
} else {
    $PkgSpec = $DefaultArchiveUrl
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
