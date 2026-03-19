"""Minimal native UI for creating and viewing reminders."""

from __future__ import annotations

from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

from triggermind.paths import state_file
from triggermind.scheduler.daemon import ensure_daemon
from triggermind.storage.json_store import JSONTriggerStore
from triggermind.triggers.absolute import AbsoluteTimeTriggerFactory
from triggermind.triggers.timer import TimerTriggerFactory


class TriggerMindUI:
    """Thin tkinter UI over existing TriggerMind scheduling/storage logic."""

    def __init__(self) -> None:
        self.store = JSONTriggerStore(state_file())
        self.timer_factory = TimerTriggerFactory()
        self.absolute_factory = AbsoluteTimeTriggerFactory()

        self.root = tk.Tk()
        self.root.title("TriggerMind")
        self.root.geometry("760x430")

        self._build_layout()
        self.refresh_list()

    def _build_layout(self) -> None:
        container = ttk.Frame(self.root, padding=14)
        container.pack(fill="both", expand=True)

        title = ttk.Label(container, text="TriggerMind", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, sticky="w")

        subtitle = ttk.Label(container, text="Local-first reminders")
        subtitle.grid(row=1, column=0, sticky="w", pady=(0, 8))

        forms = ttk.Frame(container)
        forms.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        forms.columnconfigure(0, weight=1)
        forms.columnconfigure(1, weight=1)

        timer_box = ttk.LabelFrame(forms, text="Create Timer Reminder", padding=10)
        timer_box.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ttk.Label(timer_box, text="Duration (e.g. 10m, 1h30m)").grid(row=0, column=0, sticky="w")
        self.timer_duration = ttk.Entry(timer_box, width=24)
        self.timer_duration.grid(row=1, column=0, sticky="ew", pady=(2, 6))
        ttk.Label(timer_box, text="Reminder text").grid(row=2, column=0, sticky="w")
        self.timer_message = ttk.Entry(timer_box, width=36)
        self.timer_message.grid(row=3, column=0, sticky="ew", pady=(2, 8))
        ttk.Button(timer_box, text="Create Timer", command=self.create_timer).grid(row=4, column=0, sticky="w")

        abs_box = ttk.LabelFrame(forms, text="Create Absolute-Time Reminder", padding=10)
        abs_box.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        ttk.Label(abs_box, text="Time (HH:MM, 24h)").grid(row=0, column=0, sticky="w")
        self.absolute_time = ttk.Entry(abs_box, width=24)
        self.absolute_time.grid(row=1, column=0, sticky="ew", pady=(2, 6))
        ttk.Label(abs_box, text="Reminder text").grid(row=2, column=0, sticky="w")
        self.absolute_message = ttk.Entry(abs_box, width=36)
        self.absolute_message.grid(row=3, column=0, sticky="ew", pady=(2, 8))
        ttk.Button(abs_box, text="Create Reminder", command=self.create_absolute).grid(row=4, column=0, sticky="w")

        list_frame = ttk.LabelFrame(container, text="Scheduled Reminders", padding=10)
        list_frame.grid(row=3, column=0, sticky="nsew")
        container.rowconfigure(3, weight=1)

        cols = ("id", "type", "due", "status", "message")
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("type", text="Type")
        self.tree.heading("due", text="Due")
        self.tree.heading("status", text="Status")
        self.tree.heading("message", text="Message")
        self.tree.column("id", width=110, anchor="w")
        self.tree.column("type", width=85, anchor="w")
        self.tree.column("due", width=160, anchor="w")
        self.tree.column("status", width=90, anchor="w")
        self.tree.column("message", width=280, anchor="w")
        self.tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        actions = ttk.Frame(container)
        actions.grid(row=4, column=0, sticky="e", pady=(8, 0))
        ttk.Button(actions, text="Refresh", command=self.refresh_list).pack(side="left", padx=4)
        ttk.Button(actions, text="Close", command=self.root.destroy).pack(side="left", padx=4)

    def _now(self) -> datetime:
        return datetime.now().astimezone()

    def create_timer(self) -> None:
        duration = self.timer_duration.get().strip()
        message = self.timer_message.get().strip() or "Time to refocus."
        try:
            record = self.timer_factory.create(duration, message, self._now())
            self.store.add(record)
            ensure_daemon()
        except ValueError as exc:
            messagebox.showerror("Invalid timer", str(exc))
            return
        self.timer_duration.delete(0, tk.END)
        self.timer_message.delete(0, tk.END)
        self.refresh_list()

    def create_absolute(self) -> None:
        when = self.absolute_time.get().strip()
        message = self.absolute_message.get().strip() or "Check back in with your priority task."
        try:
            record = self.absolute_factory.create(when, message, self._now())
            self.store.add(record)
            ensure_daemon()
        except ValueError as exc:
            messagebox.showerror("Invalid time", str(exc))
            return
        self.absolute_time.delete(0, tk.END)
        self.absolute_message.delete(0, tk.END)
        self.refresh_list()

    def refresh_list(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)

        records = sorted(self.store.load(), key=lambda rec: rec.due_at)
        for record in records:
            self.tree.insert(
                "",
                "end",
                values=(
                    record.id,
                    record.kind,
                    record.due_at.strftime("%Y-%m-%d %H:%M"),
                    record.status,
                    record.message,
                ),
            )

    def run(self) -> None:
        self.root.mainloop()


def launch_ui() -> None:
    """Open the TriggerMind native UI."""
    app = TriggerMindUI()
    app.run()
