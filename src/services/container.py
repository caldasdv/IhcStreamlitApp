"""Composição das dependências da aplicação."""

from __future__ import annotations

from dataclasses import dataclass

from src.database.connection import get_database
from src.repositories.mongodb.repositories import (
    MongoAcademicPeriodRepository,
    MongoClassMeetingRepository,
    MongoStudySessionRepository,
    MongoSubjectRepository,
    MongoUserRepository,
)
from src.services.academic_period_service import AcademicPeriodService
from src.services.class_meeting_service import ClassMeetingService
from src.services.session_service import SessionService
from src.services.subject_service import SubjectService
from src.services.user_service import UserService


@dataclass(frozen=True)
class ApplicationServices:
    users: UserService
    academic_periods: AcademicPeriodService
    subjects: SubjectService
    class_meetings: ClassMeetingService
    sessions: SessionService


def get_application_services() -> ApplicationServices:
    """Compõe services atuais; somente a conexão de banco permanece em cache."""
    database = get_database()
    subject_repository = MongoSubjectRepository(database)
    academic_period_repository = MongoAcademicPeriodRepository(database)
    user_repository = MongoUserRepository(database)
    return ApplicationServices(
        users=UserService(user_repository),
        academic_periods=AcademicPeriodService(
            academic_period_repository, user_repository
        ),
        subjects=SubjectService(subject_repository, academic_period_repository),
        class_meetings=ClassMeetingService(
            MongoClassMeetingRepository(database),
            subject_repository,
            academic_period_repository,
        ),
        sessions=SessionService(MongoStudySessionRepository(database), subject_repository),
    )
