"""Human-friendly time parsing helpers."""

from __future__ import annotations

import re
from datetime import datetime, timedelta

DURATION_PATTERN = re.compile(r"^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$")


def parse_duration(value: str) -> timedelta:
    """Parse a human duration string like 25m, 2h, or 1h30m."""
    raw = value.strip().lower().replace(" ", "")
    match = DURATION_PATTERN.match(raw)
    if not match:
        raise ValueError(f"Invalid duration format: {value!r}")

    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)

    if hours == minutes == seconds == 0:
        raise ValueError("Duration must be greater than 0")

    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


def parse_absolute_time(value: str, now: datetime) -> datetime:
    """Parse HH:MM as next occurrence in local time."""
    text = value.strip()
    try:
        hour_text, minute_text = text.split(":", maxsplit=1)
        hour = int(hour_text)
        minute = int(minute_text)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"Invalid time format: {value!r}. Use HH:MM.") from exc

    if hour not in range(24) or minute not in range(60):
        raise ValueError(f"Invalid time value: {value!r}. Use 00:00-23:59.")

    candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if candidate <= now:
        candidate += timedelta(days=1)
    return candidate
