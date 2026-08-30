from datetime import date, time

import pytest

from src.services.session_service import SessionService
from src.services.subject_service import SubjectService


class FakeSessionRepository:
    def __init__(self, pending=None):
        self.pending = pending or []
        self.created = []
        self.updated = []
        self.completed = []
        self.deleted = []

    def list_by_user(self, user_id):
        return []

    def list_pending_by_date(self, user_id, study_date):
        return self.pending

    def create(self, data):
        self.created.append(data)
        return "session-id"

    def mark_completed(self, session_id, user_id):
        self.completed.append((session_id, user_id))

    def update(self, session_id, user_id, data):
        self.updated.append((session_id, user_id, data))

    def delete(self, session_id, user_id):
        self.deleted.append((session_id, user_id))


def test_session_service_creates_normalized_session():
    repository = FakeSessionRepository()
    service = SessionService(repository)

    result = service.create(
        user_id="user-id",
        subject_id="subject-id",
        topic="  Heurísticas  ",
        goal="  Revisar  ",
        study_date=date(2026, 8, 30),
        study_time=time(14, 0),
        duration=60,
        priority="Alta",
    )

    assert result == "session-id"
    assert repository.created[0]["topic"] == "Heurísticas"
    assert repository.created[0]["goal"] == "Revisar"
    assert repository.created[0]["status"] == "Pendente"


def test_session_service_rejects_conflicting_session():
    repository = FakeSessionRepository([{"study_time": "14:00", "duration": 60}])
    service = SessionService(repository)

    with pytest.raises(ValueError, match="conflita"):
        service.create(
            user_id="user-id",
            subject_id="subject-id",
            topic="Revisão",
            goal="",
            study_date=date(2026, 8, 30),
            study_time=time(14, 30),
            duration=30,
            priority="Média",
        )

    assert repository.created == []


def test_session_service_updates_own_session_without_self_conflict():
    repository = FakeSessionRepository([{"_id": "session-id", "study_time": "14:00", "duration": 60}])
    service = SessionService(repository)

    service.update(
        session_id="session-id",
        user_id="user-id",
        subject_id="subject-id",
        topic="Revisão",
        goal="",
        study_date=date(2026, 8, 30),
        study_time=time(14, 30),
        duration=30,
        priority="Média",
    )

    assert repository.updated[0][0:2] == ("session-id", "user-id")
    assert repository.updated[0][2]["topic"] == "Revisão"


def test_subject_service_rejects_blank_name():
    class FakeSubjectRepository:
        def create(self, user_id, name, color):
            raise AssertionError("não deveria persistir")

    with pytest.raises(ValueError, match="nome"):
        SubjectService(FakeSubjectRepository()).create("user-id", "  ", "#5E6AD2")
