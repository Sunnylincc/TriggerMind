"""Absolute-time trigger implementation."""

from __future__ import annotations

from datetime import datetime

from triggermind.models import TriggerRecord
from triggermind.timeparse import parse_absolute_time
from triggermind.triggers.base import TriggerFactory


class AbsoluteTimeTriggerFactory(TriggerFactory):
    """Create next-occurrence HH:MM triggers."""

    def create(self, value: str, message: str, now: datetime) -> TriggerRecord:
        due_at = parse_absolute_time(value, now=now)
        return TriggerRecord(kind="absolute", due_at=due_at, message=message)
