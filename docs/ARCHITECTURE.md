# TriggerMind Architecture

TriggerMind is designed around one principle: **bounded autonomy**. The agent remains dormant and only acts when explicit trigger conditions are true.

## High-level modules

- `triggermind/main.py`: Typer CLI entrypoint and UX.
- `triggermind/triggers/`: Trigger factories and future trigger stubs.
- `triggermind/storage/`: Local persistence (JSON for MVP).
- `triggermind/scheduler/`: Lightweight background daemon.
- `triggermind/notifications/`: OS notification adapters and terminal intervention output.

## Trigger lifecycle

1. User creates a trigger with `start` or `at`.
2. CLI parses/validates user input.
3. Trigger is serialized to local state (`triggers.json`).
4. Background daemon checks pending triggers every second.
5. When due, trigger status changes to `fired` and notification is emitted.

## Why this architecture scales

- Trigger creation is abstracted behind `TriggerFactory`.
- Storage backend is replaceable (JSON now, SQLite later).
- Scheduler and notification concerns are separated.
- Future trigger types can be added without changing core CLI behavior.

## Cross-platform strategy

- macOS: `osascript`
- Linux: `notify-send` when available
- Fallback: rich terminal intervention output
- Windows support can be added by implementing a notification adapter and service runner.
