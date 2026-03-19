"""Background scheduler daemon for TriggerMind."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
import os
import signal
import subprocess
import sys
import time

from triggermind.notifications.manager import ReminderAction, prompt_reminder_action
from triggermind.paths import daemon_log_file, pid_file, state_file
from triggermind.storage.json_store import JSONTriggerStore


POLL_INTERVAL_SECONDS = 1.0


def _is_process_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def daemon_running() -> bool:
    """Return whether scheduler daemon appears to be alive."""
    pid_path = pid_file()
    if not pid_path.exists():
        return False
    try:
        pid = int(pid_path.read_text(encoding="utf-8").strip())
    except ValueError:
        return False
    return _is_process_running(pid)


def ensure_daemon() -> bool:
    """Ensure the daemon is running; return True if started now."""
    if daemon_running():
        return False

    log_path = daemon_log_file()
    with log_path.open("a", encoding="utf-8") as logfile:
        process = subprocess.Popen(  # noqa: S603
            [sys.executable, "-m", "triggermind.scheduler.daemon", "run"],
            stdout=logfile,
            stderr=logfile,
            start_new_session=True,
        )

    pid_file().write_text(str(process.pid), encoding="utf-8")
    return True


def _open_ui() -> None:
    subprocess.Popen(  # noqa: S603
        [sys.executable, "-m", "triggermind.main", "ui"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


def apply_due_action(record, action: ReminderAction) -> None:
    """Update a due record based on prompt action."""
    if action == "snooze_5m":
        record.due_at = datetime.now().astimezone() + timedelta(minutes=5)
        record.status = "scheduled"
        return

    record.status = "fired"
    if action == "open_triggermind":
        _open_ui()


def run_loop() -> None:
    """Main scheduler loop."""
    store = JSONTriggerStore(state_file())

    def _cleanup(*_: object) -> None:
        if pid_file().exists():
            pid_file().unlink(missing_ok=True)
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, _cleanup)
    signal.signal(signal.SIGINT, _cleanup)

    while True:
        now = datetime.now().astimezone()
        records = store.load()
        dirty = False

        for record in records:
            if record.status != "scheduled":
                continue
            if record.due_at <= now:
                action = prompt_reminder_action("TriggerMind", record.message)
                apply_due_action(record, action)
                dirty = True

        if dirty:
            store.save(records)

        time.sleep(POLL_INTERVAL_SECONDS)


def main() -> None:
    """Daemon module entrypoint."""
    parser = argparse.ArgumentParser(description="TriggerMind background scheduler")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("run")

    args = parser.parse_args()
    if args.command == "run":
        run_loop()
        return
    parser.print_help()


if __name__ == "__main__":
    main()
