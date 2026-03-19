"""Local desktop notification and terminal intervention output."""

from __future__ import annotations

import platform
import shutil
import subprocess


def send_notification(title: str, message: str) -> None:
    """Send a best-effort desktop notification with terminal fallback."""
    system = platform.system().lower()

    try:
        if system == "darwin":
            subprocess.run(
                [
                    "osascript",
                    "-e",
                    f'display notification "{message}" with title "{title}"',
                ],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        elif system == "linux" and shutil.which("notify-send"):
            subprocess.run(
                ["notify-send", title, message],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
    finally:
        print(f"\033[93m⚡ TriggerMind Intervention:\033[0m {message}")
