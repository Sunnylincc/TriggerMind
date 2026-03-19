#!/usr/bin/env bash
set -euo pipefail

if command -v uv >/dev/null 2>&1; then
  echo "[TriggerMind] Installing with uv..."
  uv tool install triggermind --upgrade || uv tool upgrade triggermind
elif command -v pipx >/dev/null 2>&1; then
  echo "[TriggerMind] Installing with pipx..."
  pipx install triggermind --force
elif command -v python3 >/dev/null 2>&1; then
  echo "[TriggerMind] Installing with pip..."
  python3 -m pip install --user -U triggermind
else
  echo "[TriggerMind] Python 3 is required. Please install Python 3.10+ first."
  exit 1
fi

echo "[TriggerMind] Installed. Run: triggermind"
