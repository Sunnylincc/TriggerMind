# TriggerMind

**A local-first, trigger-based AI agent CLI for bounded autonomy.**

TriggerMind is not an always-on copilot. It stays dormant by default and only intervenes when a user-defined condition is met.

The MVP ships with practical timer triggers so TriggerMind can be useful every day:

- `triggermind start 25m --message "Go back to writing"`
- `triggermind at 15:00 --message "Review the grant draft"`

---

## Why conditional AI agents matter

Most agent tooling today is either always listening, always polling, or always expensive. TriggerMind takes a different approach:

- **Dormant by default** → lower noise and distraction
- **Explicit activation conditions** → stronger user control
- **Local-first operation** → no cloud dependency for core behavior
- **Bounded autonomy** → predictable intervention only when you request it

This lowers token waste, reduces intrusive behavior, and gives humans clear control over when an AI-like intervention layer should wake up.

---

## Features (MVP)

- Human-friendly duration parsing (`25m`, `2h`, `1h30m`)
- Absolute-time triggers (`HH:MM` local time)
- Local JSON state persistence
- Lightweight background scheduler daemon
- Desktop notifications (macOS/Linux) + rich terminal fallback
- Friendly command output, robust help text, and doctor diagnostics
- Clean extension points for future trigger families

---

## Installation

### pip

```bash
pip install triggermind
```

### uv

```bash
uv tool install triggermind
```

### From source

```bash
git clone https://github.com/example/triggermind.git
cd triggermind
uv sync
uv run triggermind --help
```

---

## Usage

### Start a relative timer trigger

```bash
triggermind start 25m --message "Go back to writing"
```

### Start an absolute-time trigger

```bash
triggermind at 15:00 --message "Review the grant draft"
```

If the time already passed today, TriggerMind schedules it for tomorrow.

### List scheduled triggers

```bash
triggermind list
triggermind list --all
```

### Cancel a trigger

```bash
triggermind cancel <id>
```

### Run local diagnostics

```bash
triggermind doctor
```

---

## Architecture overview

```text
CLI (Typer)
  ├─ triggers/      # trigger parsing + factory abstractions
  ├─ storage/       # local persistence (JSON)
  ├─ scheduler/     # background polling daemon
  └─ notifications/ # OS notifications + terminal intervention
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.

---

## Example intervention flow

1. You run: `triggermind start 45m --message "Back to deep work"`
2. TriggerMind stores the trigger locally.
3. Scheduler daemon runs quietly in background.
4. At due time, TriggerMind sends a local notification and prints intervention text.

---

## Roadmap

### Near-term milestones

1. **SQLite backend + reliability improvements** (file locking, crash-safe writes, retry semantics)
2. **Plugin-style trigger registry** (calendar/focus/behavior trigger packages)
3. **Optional LLM intervention templates** (still local-first and human-in-the-loop)

### Future trigger stubs

- Calendar trigger
- Focus drift trigger
- Behavioral pattern trigger
- Biometric threshold trigger

---

## Open-source metadata suggestions

- **Short repo description:**
  `Local-first CLI for bounded-autonomy AI agents that wake only on user-defined triggers.`
- **GitHub topics/tags:**
  - `ai-agents`
  - `developer-tools`
  - `productivity`

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
