"""Typer CLI for TriggerMind."""

from __future__ import annotations

import sys
from datetime import datetime

import typer

from triggermind.doctor import run_doctor
from triggermind.paths import state_file
from triggermind.scheduler.daemon import ensure_daemon
from triggermind.storage.json_store import JSONTriggerStore
from triggermind.triggers.absolute import AbsoluteTimeTriggerFactory
from triggermind.triggers.timer import TimerTriggerFactory

app = typer.Typer(
    help="TriggerMind: a local-first, conditional AI agent that wakes up only when your trigger is met.",
    no_args_is_help=False,
    rich_markup_mode="rich",
)


def _green(text: str) -> str:
    return f"\033[92m{text}\033[0m"


def _cyan(text: str) -> str:
    return f"\033[96m{text}\033[0m"


def _yellow(text: str) -> str:
    return f"\033[93m{text}\033[0m"


def _schedule_timer(duration: str, message: str) -> str:
    now = datetime.now().astimezone()
    factory = TimerTriggerFactory()
    store = JSONTriggerStore(state_file())
    record = factory.create(duration, message, now)
    store.add(record)
    started = ensure_daemon()
    print(f"{_green('✓ Scheduled')} trigger {record.id} for {record.due_at:%Y-%m-%d %H:%M}.")
    if started:
        print(_cyan("Background scheduler started."))
    return record.id


def _schedule_absolute(when: str, message: str) -> str:
    now = datetime.now().astimezone()
    factory = AbsoluteTimeTriggerFactory()
    store = JSONTriggerStore(state_file())
    record = factory.create(when, message, now)
    store.add(record)
    started = ensure_daemon()
    print(f"{_green('✓ Scheduled')} trigger {record.id} for {record.due_at:%Y-%m-%d %H:%M}.")
    if started:
        print(_cyan("Background scheduler started."))
    return record.id


def interactive_guide() -> None:
    """Run a beginner-friendly interactive setup flow."""
    print(_cyan("Welcome to TriggerMind 👋"))
    print("I can set a reminder and stay quiet until it is time to intervene.")
    print("\nChoose what you want to create:")
    print("  1) Timer reminder (example: 25m)")
    print("  2) Specific time reminder (example: 15:00)")
    print("  3) Show my triggers")
    print("  4) Doctor check")

    choice = input("Enter 1, 2, 3, or 4: ").strip()

    if choice == "1":
        duration = input("How long from now? (examples: 25m, 2h, 1h30m): ").strip()
        message = input("What should I remind you to do? ").strip() or "Time to refocus."
        try:
            _schedule_timer(duration, message)
        except ValueError as exc:
            print(_yellow(f"Could not create timer: {exc}"))
    elif choice == "2":
        when = input("What time? (24h format HH:MM, example 15:00): ").strip()
        message = input("What should I remind you to do? ").strip() or "Check back in with your priority task."
        try:
            _schedule_absolute(when, message)
        except ValueError as exc:
            print(_yellow(f"Could not create reminder: {exc}"))
    elif choice == "3":
        list_triggers()
    elif choice == "4":
        doctor()
    else:
        print(_yellow("Invalid selection. Run `triggermind guide` to try again."))


@app.command("guide")
def guide() -> None:
    """Launch an interactive, no-code setup guide."""
    interactive_guide()


@app.command("start")
def start_timer(
    duration: str = typer.Argument(..., help="Duration like 25m, 2h, or 1h30m."),
    message: str = typer.Option("Time to refocus.", "--message", "-m", help="Intervention message."),
) -> None:
    """Start a timer trigger."""
    try:
        _schedule_timer(duration, message)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc


@app.command("at")
def start_absolute(
    when: str = typer.Argument(..., help="Absolute local time in HH:MM (24-hour clock)."),
    message: str = typer.Option("Check back in with your priority task.", "--message", "-m"),
) -> None:
    """Start an absolute-time trigger."""
    try:
        _schedule_absolute(when, message)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc


@app.command("list")
def list_triggers(all_records: bool = typer.Option(False, "--all", help="Include fired/cancelled triggers.")) -> None:
    """List triggers currently in local state."""
    store = JSONTriggerStore(state_file())
    records = store.load()

    if not all_records:
        records = [record for record in records if record.status == "scheduled"]

    if not records:
        print("No triggers found.")
        return

    print("ID         TYPE      DUE               STATUS     MESSAGE")
    print("-" * 72)
    for record in sorted(records, key=lambda rec: rec.due_at):
        print(
            f"{record.id:<10} {record.kind:<9} {record.due_at.strftime('%Y-%m-%d %H:%M'):<17} {record.status:<10} {record.message}"
        )


@app.command()
def cancel(trigger_id: str = typer.Argument(..., help="Trigger ID to cancel.")) -> None:
    """Cancel a pending trigger by ID."""
    store = JSONTriggerStore(state_file())
    if store.cancel(trigger_id):
        print(f"{_green('✓ Cancelled')} trigger {trigger_id}.")
    else:
        raise typer.BadParameter(f"Could not cancel trigger {trigger_id!r}. Is it scheduled?")


@app.command()
def doctor() -> None:
    """Run local environment diagnostics."""
    checks = run_doctor()
    print("CHECK             RESULT  DETAIL")
    print("-" * 72)
    for name, ok, detail in checks:
        emoji = "✅" if ok else "❌"
        print(f"{name:<17} {emoji:<6} {detail}")


@app.command()
def update() -> None:
    """Show update instructions for the current install method."""
    print("To update TriggerMind, run one of these:")
    print("  pip install -U triggermind")
    print("  uv tool upgrade triggermind")


def run() -> None:
    """Console script entrypoint with beginner-friendly default behavior."""
    if len(sys.argv) == 1:
        interactive_guide()
        return
    app()


if __name__ == "__main__":
    run()
