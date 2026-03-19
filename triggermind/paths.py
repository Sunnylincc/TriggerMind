"""Filesystem paths used by TriggerMind."""

from __future__ import annotations

import os
from pathlib import Path


def data_dir() -> Path:
    """Return the local data directory, creating it when needed."""
    base = os.environ.get("TRIGGERMIND_DATA_DIR")
    directory = Path(base).expanduser() if base else Path.home() / ".local" / "share" / "triggermind"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def state_file() -> Path:
    """Path to trigger state file."""
    return data_dir() / "triggers.json"


def pid_file() -> Path:
    """Path to scheduler daemon PID file."""
    return data_dir() / "daemon.pid"


def daemon_log_file() -> Path:
    """Path to daemon output log file."""
    return data_dir() / "daemon.log"
