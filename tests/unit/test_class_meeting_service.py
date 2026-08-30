from datetime import time

import pytest

from src.services.class_meeting_service import ClassMeetingService


class FakeClassMeetingRepository:
    def __init__(self) -> None:
        self.meetings = []
        self.created = []
        self.deleted = []

    def list_by_period(self, user_id, academic_period_id):
        return [
            meeting.copy()
            for meeting in self.meetings
            if meeting["user_id"] == user_id
            and meeting["academic_period_id"] == academic_period_id
        ]

    def list_by_weekday(self, user_id, academic_period_id, weekday):
        return [
            meeting
            for meeting in self.list_by_period(user_id, academic_period_id)
            if meeting["weekday"] == weekday
        ]

    def create(self, data):
        self.created.append(data)
        return "meeting-id"

    def delete(self, user_id, academic_period_id, meeting_id):
        self.deleted.append((user_id, academic_period_id, meeting_id))


class FakeSubjectRepository:
    def belongs_to_user_period(self, user_id, subject_id, academic_period_id):
        return (user_id, subject_id, academic_period_id) == (
            "user-id",
            "subject-id",
            "period-id",
        )


class FakeAcademicPeriodRepository:
    def is_active_owned_by(self, user_id, academic_period_id):
        return (user_id, academic_period_id) == ("user-id", "period-id")


def build_service(repository=None):
    return ClassMeetingService(
        repository or FakeClassMeetingRepository(),
        FakeSubjectRepository(),
        FakeAcademicPeriodRepository(),
    )


def test_create_class_meeting_persists_normalized_data() -> None:
    repository = FakeClassMeetingRepository()

    result = build_service(repository).create(
        user_id="user-id",
        academic_period_id="period-id",
        subject_id="subject-id",
        weekday=0,
        start_time=time(8, 0),
        end_time=time(9, 30),
        location="  Bloco B   sala 204 ",
    )

    assert result == "meeting-id"
    assert repository.created == [
        {
            "user_id": "user-id",
            "academic_period_id": "period-id",
            "subject_id": "subject-id",
            "weekday": 0,
            "start_time": "08:00",
            "end_time": "09:30",
            "location": "Bloco B sala 204",
        }
    ]


def test_create_rejects_foreign_subject_or_period() -> None:
    service = build_service()

    with pytest.raises(ValueError, match="período acadêmico ativo"):
        service.create(
            user_id="user-id",
            academic_period_id="foreign-period",
            subject_id="subject-id",
            weekday=0,
            start_time=time(8),
            end_time=time(9),
            location="",
        )

    with pytest.raises(ValueError, match="disciplina válida"):
        service.create(
            user_id="user-id",
            academic_period_id="period-id",
            subject_id="foreign-subject",
            weekday=0,
            start_time=time(8),
            end_time=time(9),
            location="",
        )


def test_create_rejects_schedule_conflict() -> None:
    repository = FakeClassMeetingRepository()
    repository.meetings.append(
        {
            "_id": "existing",
            "user_id": "user-id",
            "academic_period_id": "period-id",
            "subject_id": "subject-id",
            "weekday": 0,
            "start_time": "08:00",
            "end_time": "09:00",
        }
    )

    with pytest.raises(ValueError, match="conflita"):
        build_service(repository).create(
            user_id="user-id",
            academic_period_id="period-id",
            subject_id="subject-id",
            weekday=0,
            start_time=time(8, 30),
            end_time=time(9, 30),
            location="",
        )

    assert repository.created == []


def test_list_enriches_meeting_without_losing_missing_subject() -> None:
    repository = FakeClassMeetingRepository()
    repository.meetings.extend(
        [
            {
                "_id": "known",
                "user_id": "user-id",
                "academic_period_id": "period-id",
                "subject_id": "subject-id",
                "weekday": 0,
            },
            {
                "_id": "missing",
                "user_id": "user-id",
                "academic_period_id": "period-id",
                "subject_id": "missing-subject",
                "weekday": 1,
            },
        ]
    )

    meetings = build_service(repository).list_for_period(
        "user-id",
        "period-id",
        [{"_id": "subject-id", "name": "IHC", "color": "#5E6AD2"}],
    )

    assert meetings[0]["subject_name"] == "IHC"
    assert meetings[1]["subject_name"] == "Disciplina indisponível"


def test_delete_forwards_complete_ownership_scope() -> None:
    repository = FakeClassMeetingRepository()

    build_service(repository).delete("user-id", "period-id", "meeting-id")

    assert repository.deleted == [("user-id", "period-id", "meeting-id")]
