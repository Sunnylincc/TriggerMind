from datetime import datetime, timedelta, timezone

from triggermind.models import TriggerRecord
from triggermind.scheduler import daemon


def _record() -> TriggerRecord:
    now = datetime.now(timezone.utc)
    return TriggerRecord(kind="timer", due_at=now, message="Call an Uber")


def test_apply_due_action_dismiss() -> None:
    record = _record()
    daemon.apply_due_action(record, "dismiss")
    assert record.status == "fired"


def test_apply_due_action_open_triggermind(monkeypatch) -> None:
    record = _record()
    called = {"opened": False}

    def fake_open() -> None:
        called["opened"] = True

    monkeypatch.setattr(daemon, "_open_ui", fake_open)
    daemon.apply_due_action(record, "open_triggermind")

    assert record.status == "fired"
    assert called["opened"] is True


def test_apply_due_action_snooze_5m() -> None:
    record = _record()
    previous_due = record.due_at

    daemon.apply_due_action(record, "snooze_5m")

    assert record.status == "scheduled"
    assert record.due_at > previous_due
    assert record.due_at <= datetime.now().astimezone() + timedelta(minutes=5, seconds=5)
