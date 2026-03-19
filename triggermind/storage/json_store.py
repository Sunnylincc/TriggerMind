"""JSON-backed local storage for trigger records."""

from __future__ import annotations

import json
from pathlib import Path

from triggermind.models import TriggerRecord


class JSONTriggerStore:
    """Simple JSON trigger store."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> list[TriggerRecord]:
        """Load all trigger records from disk."""
        if not self.path.exists():
            return []
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return [TriggerRecord.from_dict(item) for item in payload]

    def save(self, records: list[TriggerRecord]) -> None:
        """Persist all records to disk."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = [record.to_dict() for record in records]
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def add(self, record: TriggerRecord) -> TriggerRecord:
        """Add a record and persist."""
        records = self.load()
        records.append(record)
        self.save(records)
        return record

    def cancel(self, trigger_id: str) -> bool:
        """Cancel a scheduled trigger by id."""
        records = self.load()
        changed = False
        for record in records:
            if record.id == trigger_id and record.status == "scheduled":
                record.status = "cancelled"
                changed = True
        if changed:
            self.save(records)
        return changed
