"""Health checks for local TriggerMind environment."""

from __future__ import annotations

import platform
from pathlib import Path

from triggermind.paths import data_dir, pid_file, state_file
from triggermind.scheduler.daemon import daemon_running


def run_doctor() -> list[tuple[str, bool, str]]:
    """Run local diagnostics and return check tuples."""
    data = data_dir()
    checks: list[tuple[str, bool, str]] = [
        ("Platform", True, platform.platform()),
        ("Data directory", data.exists(), str(data)),
        ("State file", state_file().exists(), str(state_file())),
        ("Daemon PID file", pid_file().exists(), str(pid_file())),
        ("Daemon running", daemon_running(), "background scheduler process"),
        ("Cloud required", True, "No"),
        ("Telemetry enabled", True, "No"),
    ]
    return checks
