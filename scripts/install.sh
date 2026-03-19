#!/usr/bin/env bash
set -euo pipefail

if [[ -n "${TRIGGERMIND_ARCHIVE_URL:-}" ]]; then
  PKG_SPEC="${TRIGGERMIND_ARCHIVE_URL}"
elif [[ -f "pyproject.toml" ]]; then
  PKG_SPEC="."
else
  echo "[TriggerMind] TRIGGERMIND_ARCHIVE_URL is not set."
  echo "[TriggerMind] Set it to your ZIP URL, e.g."
  echo "[TriggerMind] export TRIGGERMIND_ARCHIVE_URL=https://github.com/<YOUR_ORG>/triggermind/archive/refs/heads/main.zip"
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
