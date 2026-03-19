from datetime import datetime, timedelta

import pytest

from triggermind.timeparse import parse_absolute_time, parse_duration


def test_parse_duration_examples() -> None:
    assert parse_duration("25m") == timedelta(minutes=25)
    assert parse_duration("2h") == timedelta(hours=2)
    assert parse_duration("1h30m") == timedelta(hours=1, minutes=30)


def test_parse_duration_rejects_invalid() -> None:
    with pytest.raises(ValueError):
        parse_duration("abc")

    with pytest.raises(ValueError):
        parse_duration("0m")


def test_parse_absolute_time_rolls_forward() -> None:
    now = datetime(2026, 1, 1, 16, 0, 0)
    due = parse_absolute_time("15:00", now)
    assert due == datetime(2026, 1, 2, 15, 0, 0)


def test_parse_absolute_time_same_day_future() -> None:
    now = datetime(2026, 1, 1, 14, 0, 0)
    due = parse_absolute_time("15:30", now)
    assert due == datetime(2026, 1, 1, 15, 30, 0)
