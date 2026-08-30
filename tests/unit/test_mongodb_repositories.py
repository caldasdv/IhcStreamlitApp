from datetime import date
from types import SimpleNamespace

import pytest

from src.domain.exceptions import EntityNotFoundError
from src.repositories.mongodb.repositories import (
    MongoAcademicPeriodRepository,
    MongoClassMeetingRepository,
    MongoStudySessionRepository,
    MongoSubjectRepository,
)


class FakeCollection:
    def __init__(self, *, matched_count: int = 1, deleted_count: int = 1) -> None:
        self.matched_count = matched_count
        self.deleted_count = deleted_count
        self.last_query = None

    def find(self, query, projection=None):
        self.last_query = query
        return self

    def sort(self, *ordering):
        return []

    def update_one(self, query, update):
        self.last_query = query
        self.last_update = update
        return SimpleNamespace(matched_count=self.matched_count)

    def delete_one(self, query):
        self.last_query = query
        return SimpleNamespace(deleted_count=self.deleted_count)


def repository_with(collection: FakeCollection) -> MongoStudySessionRepository:
    database = SimpleNamespace(study_sessions=collection)
    return MongoStudySessionRepository(database)


@pytest.mark.parametrize("operation", ["update", "mark_completed"])
def test_update_operations_reject_missing_session(operation: str) -> None:
    repository = repository_with(FakeCollection(matched_count=0))

    with pytest.raises(EntityNotFoundError):
        if operation == "update":
            repository.update("session-id", "user-id", {"topic": "Revisão"})
        else:
            repository.mark_completed("session-id", "user-id")


def test_delete_rejects_missing_session() -> None:
    repository = repository_with(FakeCollection(deleted_count=0))

    with pytest.raises(EntityNotFoundError):
        repository.delete("session-id", "user-id")


def test_list_by_user_applies_user_and_date_range() -> None:
    collection = FakeCollection()
    repository = repository_with(collection)

    repository.list_by_user(
        "user-id", start_date=date(2026, 8, 24), end_date=date(2026, 8, 30)
    )

    assert collection.last_query == {
        "user_id": "user-id",
        "study_date": {"$gte": "2026-08-24", "$lte": "2026-08-30"},
    }


def test_archive_period_rejects_missing_or_foreign_period() -> None:
    collection = FakeCollection(matched_count=0)
    repository = MongoAcademicPeriodRepository(
        SimpleNamespace(academic_periods=collection)
    )

    with pytest.raises(EntityNotFoundError):
        repository.archive("user-id", "period-id")


def test_subject_list_is_scoped_by_user_and_period() -> None:
    collection = FakeCollection()
    repository = MongoSubjectRepository(SimpleNamespace(subjects=collection))

    repository.list_by_period("user-id", "period-id")

    assert collection.last_query == {
        "user_id": "user-id",
        "academic_period_id": "period-id",
    }


def test_legacy_subject_list_is_explicitly_scoped() -> None:
    collection = FakeCollection()
    repository = MongoSubjectRepository(SimpleNamespace(subjects=collection))

    repository.list_without_period("user-id")

    assert collection.last_query == {
        "user_id": "user-id",
        "academic_period_id": {"$exists": False},
    }


def test_delete_class_meeting_rejects_missing_or_foreign_document() -> None:
    collection = FakeCollection(deleted_count=0)
    repository = MongoClassMeetingRepository(
        SimpleNamespace(class_meetings=collection)
    )

    with pytest.raises(EntityNotFoundError):
        repository.delete("user-id", "period-id", "meeting-id")

    assert collection.last_query == {
        "_id": "meeting-id",
        "user_id": "user-id",
        "academic_period_id": "period-id",
    }


def test_class_meeting_list_is_scoped_by_user_and_period() -> None:
    collection = FakeCollection()
    repository = MongoClassMeetingRepository(
        SimpleNamespace(class_meetings=collection)
    )

    repository.list_by_period("user-id", "period-id")

    assert collection.last_query == {
        "user_id": "user-id",
        "academic_period_id": "period-id",
    }


def test_assign_legacy_subject_uses_atomic_ownership_and_legacy_filter() -> None:
    collection = FakeCollection()
    repository = MongoSubjectRepository(SimpleNamespace(subjects=collection))

    repository.assign_legacy_to_period(
        "user-id", "subject-id", "period-id", "ihc"
    )

    assert collection.last_query == {
        "_id": "subject-id",
        "user_id": "user-id",
        "academic_period_id": {"$exists": False},
    }
    assert collection.last_update["$set"]["academic_period_id"] == "period-id"
    assert collection.last_update["$set"]["name_normalized"] == "ihc"


def test_assign_legacy_subject_rejects_race_or_foreign_document() -> None:
    collection = FakeCollection(matched_count=0)
    repository = MongoSubjectRepository(SimpleNamespace(subjects=collection))

    with pytest.raises(EntityNotFoundError):
        repository.assign_legacy_to_period(
            "user-id", "subject-id", "period-id", "ihc"
        )
