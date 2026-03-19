"""Future trigger type placeholders for roadmap clarity."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PlannedTrigger:
    """Metadata for upcoming trigger types."""

    name: str
    description: str


PLANNED_TRIGGERS: list[PlannedTrigger] = [
    PlannedTrigger("calendar", "Fire when a calendar event starts or ends."),
    PlannedTrigger("focus", "Fire when focus drift is detected from active context."),
    PlannedTrigger("behavior", "Fire on repeated behavior patterns in local activity logs."),
    PlannedTrigger("biometric", "Fire from local wearable biometrics and thresholds."),
]
