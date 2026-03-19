$ErrorActionPreference = "Stop"

if (Get-Command uv -ErrorAction SilentlyContinue) {
    Write-Host "[TriggerMind] Installing with uv..."
    try {
        uv tool install triggermind --upgrade
    } catch {
        uv tool upgrade triggermind
    }
} elseif (Get-Command pipx -ErrorAction SilentlyContinue) {
    Write-Host "[TriggerMind] Installing with pipx..."
    pipx install triggermind --force
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    Write-Host "[TriggerMind] Installing with pip..."
    py -m pip install --user -U triggermind
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "[TriggerMind] Installing with pip..."
    python -m pip install --user -U triggermind
} else {
    Write-Host "[TriggerMind] Python 3.10+ is required."
    exit 1
}

Write-Host "[TriggerMind] Installed. Run: triggermind"
