"""Timer trigger implementation."""

from __future__ import annotations

from datetime import datetime

from triggermind.models import TriggerRecord
from triggermind.timeparse import parse_duration
from triggermind.triggers.base import TriggerFactory


class TimerTriggerFactory(TriggerFactory):
    """Create relative-duration timer triggers."""

    def create(self, value: str, message: str, now: datetime) -> TriggerRecord:
        delay = parse_duration(value)
        return TriggerRecord(kind="timer", due_at=now + delay, message=message)
