"""Core models for triggers and storage records."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

TriggerKind = Literal["timer", "absolute"]
TriggerStatus = Literal["scheduled", "fired", "cancelled"]


@dataclass(slots=True)
class TriggerRecord:
    """Represents a scheduled trigger."""

    kind: TriggerKind
    due_at: datetime
    message: str
    id: str = field(default_factory=lambda: uuid4().hex[:10])
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: TriggerStatus = "scheduled"

    def to_dict(self) -> dict[str, str]:
        """Serialize to a JSON-compatible dict."""
        return {
            "id": self.id,
            "kind": self.kind,
            "message": self.message,
            "due_at": self.due_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "TriggerRecord":
        """Deserialize from JSON dict."""
        return cls(
            id=data["id"],
            kind=data["kind"],
            message=data["message"],
            due_at=datetime.fromisoformat(data["due_at"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            status=data["status"],
        )
