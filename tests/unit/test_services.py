from datetime import date, time

import pytest

from src.services.session_service import SessionService
from src.services.subject_service import SubjectService
from src.services.user_service import UserService


class FakeSessionRepository:
    def __init__(self, pending=None):
        self.pending = pending or []
        self.created = []
        self.updated = []
        self.completed = []
        self.deleted = []

    def list_by_user(self, user_id, start_date=None, end_date=None):
        self.list_range = (user_id, start_date, end_date)
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


class FakeUserRepository:
    def __init__(self):
        self.users = {}

    def find_or_create_by_identity(self, identity):
        key = (identity["provider"], identity["subject"])
        return self.users.setdefault(
            key,
            {
                "_id": key,
                "identity": {"provider": identity["provider"], "subject": identity["subject"]},
                "name": identity["name"],
                "email": identity["email"],
                "weekly_goal_minutes": 300,
            },
        )

    def update_weekly_goal(self, user_id, minutes):
        self.goal = (user_id, minutes)

    def update_current_academic_period(self, user_id, period_id):
        self.current_period = (user_id, period_id)


class FakeSubjectRepository:
    def __init__(self, valid_subject_ids=None):
        self.valid_subject_ids = set(valid_subject_ids or ["subject-id"])
        self.normalized_names = set()
        self.created = []

    def belongs_to_user(self, user_id, subject_id):
        return subject_id in self.valid_subject_ids

    def list_by_user(self, user_id):
        return [
            {"_id": index, "name": name}
            for index, name in enumerate(getattr(self, "legacy_names", []))
        ]

    def exists_by_normalized_name(self, user_id, normalized_name):
        return normalized_name in self.normalized_names

    def create(self, user_id, name, normalized_name, color):
        self.created.append((user_id, name, normalized_name, color))
        self.normalized_names.add(normalized_name)
        return "subject-id"


def test_session_service_creates_normalized_session():
    repository = FakeSessionRepository()
    service = SessionService(repository, FakeSubjectRepository())

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
    service = SessionService(repository, FakeSubjectRepository())

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
    service = SessionService(repository, FakeSubjectRepository())

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
    with pytest.raises(ValueError, match="nome"):
        SubjectService(FakeSubjectRepository()).create("user-id", "  ", "#5E6AD2")


def test_subject_service_rejects_equivalent_duplicate_name():
    repository = FakeSubjectRepository()
    repository.normalized_names.add("interação humano-computador")

    with pytest.raises(ValueError, match="já possui"):
        SubjectService(repository).create(
            "user-id", "  INTERAÇÃO   HUMANO-COMPUTADOR ", "#5E6AD2"
        )


def test_subject_service_rejects_duplicate_legacy_name():
    repository = FakeSubjectRepository()
    repository.legacy_names = ["Interação Humano-Computador"]

    with pytest.raises(ValueError, match="já possui"):
        SubjectService(repository).create(
            "user-id", " interação  humano-computador ", "#5E6AD2"
        )


def test_subject_service_rejects_invalid_color():
    with pytest.raises(ValueError, match="cor válida"):
        SubjectService(FakeSubjectRepository()).create("user-id", "IHC", "red")


def test_session_service_rejects_subject_from_another_user():
    repository = FakeSessionRepository()
    service = SessionService(repository, FakeSubjectRepository(valid_subject_ids=[]))

    with pytest.raises(ValueError, match="disciplina válida"):
        service.create(
            user_id="user-id",
            subject_id="another-user-subject",
            topic="Revisão",
            goal="",
            study_date=date(2026, 8, 30),
            study_time=time(14, 0),
            duration=30,
            priority="Média",
        )

    assert repository.created == []


def test_session_service_forwards_requested_date_range():
    repository = FakeSessionRepository()
    service = SessionService(repository, FakeSubjectRepository())

    service.list_for_user(
        "user-id", [], start_date=date(2026, 8, 24), end_date=date(2026, 8, 30)
    )

    assert repository.list_range == (
        "user-id",
        date(2026, 8, 24),
        date(2026, 8, 30),
    )


def test_user_service_resolves_user_by_provider_subject():
    repository = FakeUserRepository()
    service = UserService(repository)
    identity = {
        "provider": "google",
        "subject": "google-subject",
        "name": "Ana",
        "email": "ana@example.com",
    }

    first = service.get_or_create_authenticated_user(identity)
    second = service.get_or_create_authenticated_user(identity)

    assert first == second
    assert first["identity"] == {"provider": "google", "subject": "google-subject"}


@pytest.mark.parametrize("hours", [0, 80.5])
def test_user_service_rejects_weekly_goal_outside_allowed_range(hours):
    service = UserService(FakeUserRepository())

    with pytest.raises(ValueError, match="entre 1 e 80"):
        service.update_weekly_goal("user-id", hours)


def test_user_service_updates_current_academic_period():
    repository = FakeUserRepository()

    UserService(repository).update_current_academic_period("user-id", "period-id")

    assert repository.current_period == ("user-id", "period-id")
