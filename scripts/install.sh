#!/usr/bin/env bash
set -euo pipefail

DEFAULT_ARCHIVE_URL="https://github.com/Sunnylincc/TriggerMind/archive/refs/heads/main.zip"

if [[ -n "${TRIGGERMIND_ARCHIVE_URL:-}" ]]; then
  PKG_SPEC="${TRIGGERMIND_ARCHIVE_URL}"
elif [[ -f "pyproject.toml" ]]; then
  PKG_SPEC="."
else
  PKG_SPEC="$DEFAULT_ARCHIVE_URL"
fi

if command -v python3 >/dev/null 2>&1; then
  echo "[TriggerMind] Installing with pip..."
  python3 -m pip install --user -U "$PKG_SPEC"
else
  echo "[TriggerMind] Python 3 is required. Please install Python 3.10+ first."
  exit 1
fi

echo "[TriggerMind] Installed. Run: triggermind"
