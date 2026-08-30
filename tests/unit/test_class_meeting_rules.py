from datetime import time

import pytest

from src.domain.class_meeting_rules import (
    class_meetings_conflict,
    validate_class_meeting,
)


def test_class_meeting_requires_end_after_start() -> None:
    with pytest.raises(ValueError, match="posterior"):
        validate_class_meeting(0, time(10, 0), time(9, 0))


def test_class_meeting_rejects_invalid_weekday() -> None:
    with pytest.raises(ValueError, match="dia da semana"):
        validate_class_meeting(7, time(8, 0), time(9, 0))


def test_class_meeting_detects_overlap() -> None:
    assert class_meetings_conflict(
        time(8, 30),
        time(9, 30),
        [{"start_time": "08:00", "end_time": "09:00"}],
    )


def test_class_meeting_allows_adjacent_ranges() -> None:
    assert not class_meetings_conflict(
        time(9, 0),
        time(10, 0),
        [{"start_time": "08:00", "end_time": "09:00"}],
    )
