#!/usr/bin/env bash
set -euo pipefail

if [[ -f "pyproject.toml" ]]; then
  PKG_SPEC="."
elif [[ -n "${TRIGGERMIND_GIT_URL:-}" ]]; then
  PKG_SPEC="git+${TRIGGERMIND_GIT_URL}"
else
  echo "[TriggerMind] Not in repo root and TRIGGERMIND_GIT_URL is not set."
  echo "[TriggerMind] Clone the repo first, then run: python3 -m pip install --user -U ."
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  echo "[TriggerMind] Installing with pip..."
  python3 -m pip install --user -U "$PKG_SPEC"
else
  echo "[TriggerMind] Python 3 is required. Please install Python 3.10+ first."
  exit 1
fi

echo "[TriggerMind] Installed. Run: triggermind"
