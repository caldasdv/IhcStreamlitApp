from datetime import date, time

import pytest

from src.domain.session_rules import (
    SessionValidationError,
    effective_status,
    minutes_at,
    sessions_conflict,
    validate_new_session,
)


def test_pending_past_session_is_overdue() -> None:
    row = {"status": "Pendente", "study_date": "2026-08-29"}

    assert effective_status(row, today=date(2026, 8, 30)) == "Atrasada"


def test_completed_past_session_remains_completed() -> None:
    row = {"status": "Concluída", "study_date": "2026-08-29"}

    assert effective_status(row, today=date(2026, 8, 30)) == "Concluída"


@pytest.mark.parametrize("value", ["", "25:00", "12:60", "12"])
def test_invalid_time_is_rejected(value: str) -> None:
    with pytest.raises(SessionValidationError):
        minutes_at(value)


def test_session_at_boundary_does_not_conflict() -> None:
    existing = [{"study_time": "14:00", "duration": 60}]

    assert not sessions_conflict(time(15, 0), 30, existing)


def test_overlapping_session_conflicts() -> None:
    existing = [{"study_time": "14:00", "duration": 60}]

    assert sessions_conflict(time(14, 30), 30, existing)


def test_new_session_requires_topic_and_future_or_today_date() -> None:
    with pytest.raises(SessionValidationError):
        validate_new_session(topic=" ", study_date=date(2026, 8, 30), duration=30, today=date(2026, 8, 30))

    with pytest.raises(SessionValidationError):
        validate_new_session(topic="Revisão", study_date=date(2026, 8, 29), duration=30, today=date(2026, 8, 30))
