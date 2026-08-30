"""Composição das dependências da aplicação."""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

from src.database.connection import get_database
from src.repositories.mongodb.repositories import (
    MongoStudySessionRepository,
    MongoSubjectRepository,
    MongoUserRepository,
)
from src.services.session_service import SessionService
from src.services.subject_service import SubjectService
from src.services.user_service import UserService


@dataclass(frozen=True)
class ApplicationServices:
    users: UserService
    subjects: SubjectService
    sessions: SessionService


@st.cache_resource
def get_application_services() -> ApplicationServices:
    database = get_database()
    subject_repository = MongoSubjectRepository(database)
    return ApplicationServices(
        users=UserService(MongoUserRepository(database)),
        subjects=SubjectService(subject_repository),
        sessions=SessionService(MongoStudySessionRepository(database), subject_repository),
    )
