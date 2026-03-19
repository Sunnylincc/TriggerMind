# TriggerMind

**A local-first, trigger-based AI agent CLI for bounded autonomy.**

TriggerMind stays dormant by default and only intervenes when a user-defined condition is met.

## One-line install (copy/paste)

> `triggermind` is not published on PyPI yet. Use direct source ZIP install.

### macOS + Linux

```bash
python3 -m pip install --user -U "https://github.com/Sunnylincc/TriggerMind/archive/refs/heads/main.zip"
```

### Windows PowerShell

```powershell
py -m pip install --user -U "https://github.com/Sunnylincc/TriggerMind/archive/refs/heads/main.zip"
```

If `py` is unavailable on Windows, use:

```powershell
python -m pip install --user -U "https://github.com/Sunnylincc/TriggerMind/archive/refs/heads/main.zip"
```

### Optional: install from local source folder

```bash
python3 -m pip install --user -U .
```

After install, run:

```bash
triggermind
```

No coding needed: TriggerMind launches an interactive guide and asks what reminder you want.

---

## Quick examples

```bash
triggermind start 25m --message "Go back to writing"
triggermind at 15:00 --message "Review the grant draft"
triggermind list
triggermind cancel <id>
triggermind doctor
triggermind update
triggermind ui
```

---


## Native UI + reminder dialog (v1)

TriggerMind now includes a thin native UI layer while keeping the CLI as the core workflow.

- Launch UI: `triggermind ui`
- Create timer reminders and absolute-time reminders
- View currently scheduled reminders

When a reminder fires, TriggerMind shows a visible native prompt with exactly these actions:

- **Dismiss**: marks the reminder as fired
- **Snooze 5m**: reschedules the same reminder for 5 minutes later
- **Open TriggerMind**: marks fired and opens the TriggerMind UI

Reminder messages are treated as plain reminder text in v1 (not automation instructions).

---

## Why conditional AI agents matter

Most agent tooling is always-on and noisy. TriggerMind is different:

- **Dormant by default**
- **Activated only by explicit conditions**
- **Local-first** (no cloud required)
- **Human-controlled bounded autonomy**

This reduces unnecessary token usage, risk, and intrusion.

---

## Features (MVP)

- Human-friendly time parsing (`25m`, `2h`, `1h30m`)
- Absolute-time triggers (`HH:MM` local time)
- Friendly interactive setup mode (`triggermind` with no args)
- Local JSON state persistence
- Lightweight background scheduler daemon
- Minimal native UI (`triggermind ui`) to create and view reminders
- Visible native reminder dialog with actions: Dismiss, Snooze 5m, Open TriggerMind
- Desktop notifications fallback for headless/non-GUI environments
- Clean extension points for future trigger types

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

## Roadmap

1. SQLite backend + crash-safe scheduling
2. Plugin trigger registry for calendar/focus/behavior signals
3. Optional local LLM intervention templates

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
