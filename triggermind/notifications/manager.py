"""Local native reminder prompt and desktop notification helpers."""

from __future__ import annotations

from dataclasses import dataclass
import platform
import shutil
import subprocess
from typing import Literal

ReminderAction = Literal["dismiss", "snooze_5m", "open_triggermind"]


@dataclass(slots=True)
class ReminderPrompt:
    """Rendered reminder content shown to the user."""

    title: str
    message: str


def _send_non_interactive_notification(title: str, message: str) -> None:
    """Send best-effort desktop notification with terminal fallback."""
    system = platform.system().lower()

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


def _show_tk_prompt(prompt: ReminderPrompt) -> ReminderAction:
    """Render a small native prompt with fixed v1 actions."""
    import tkinter as tk

    selected: ReminderAction = "dismiss"

    root = tk.Tk()
    root.title(prompt.title)
    root.attributes("-topmost", True)
    root.resizable(False, False)

    frame = tk.Frame(root, padx=16, pady=12)
    frame.pack(fill="both", expand=True)

    heading = tk.Label(frame, text="TriggerMind Reminder", font=("Segoe UI", 12, "bold"))
    heading.pack(anchor="w")

    message = tk.Label(frame, text=prompt.message, wraplength=380, justify="left", pady=8)
    message.pack(anchor="w")

    buttons = tk.Frame(frame)
    buttons.pack(anchor="e", pady=(8, 0))

    def choose(action: ReminderAction) -> None:
        nonlocal selected
        selected = action
        root.destroy()

    tk.Button(buttons, text="Dismiss", width=14, command=lambda: choose("dismiss")).pack(side="left", padx=4)
    tk.Button(buttons, text="Snooze 5m", width=14, command=lambda: choose("snooze_5m")).pack(side="left", padx=4)
    tk.Button(buttons, text="Open TriggerMind", width=14, command=lambda: choose("open_triggermind")).pack(side="left", padx=4)

    root.protocol("WM_DELETE_WINDOW", lambda: choose("dismiss"))
    root.mainloop()
    return selected


def prompt_reminder_action(title: str, message: str) -> ReminderAction:
    """Show a visible reminder prompt and return the user action."""
    prompt = ReminderPrompt(title=title, message=message)

    try:
        return _show_tk_prompt(prompt)
    except Exception:
        # Headless or GUI-unavailable fallback: notify + dismiss.
        _send_non_interactive_notification(title, message)
        print(f"\033[93m⚡ TriggerMind Intervention:\033[0m {message}")
        return "dismiss"
