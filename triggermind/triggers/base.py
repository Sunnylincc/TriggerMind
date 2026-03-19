"""Base trigger abstractions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from triggermind.models import TriggerRecord


class TriggerFactory(ABC):
    """Factory that creates trigger records from user input."""

    @abstractmethod
    def create(self, value: str, message: str, now: datetime) -> TriggerRecord:
        """Create a trigger record."""
