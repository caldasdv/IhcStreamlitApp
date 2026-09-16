"""Popula uma conta existente com dados demonstrativos, sem duplicar a carga."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from pathlib import Path
import sys


if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.database.connection import get_database


EMAIL = "nerofxcs@gmail.com"
MOCK_KEY = "david-caldas-demo-v1"


def _find_or_create_period(database, user_id):
    period = database.academic_periods.find_one(
        {"user_id": user_id, "status": "ACTIVE"}, sort=[("start_date", -1)]
    )
    if period:
        return period

    today = date.today()
    period_id = database.academic_periods.insert_one(
        {
            "user_id": user_id,
            "name": "Semestre em movimento",
            "name_normalized": "semestre em movimento",
            "start_date": (today - timedelta(days=45)).isoformat(),
            "end_date": (today + timedelta(days=100)).isoformat(),
            "status": "ACTIVE",
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
            "mock_key": MOCK_KEY,
        }
    ).inserted_id
    return database.academic_periods.find_one({"_id": period_id})


def _find_or_create_subject(database, user_id, period_id, name, color):
    subject = database.subjects.find_one(
        {"user_id": user_id, "academic_period_id": period_id, "name_normalized": name.lower()}
    )
    if subject:
        return subject
    subject_id = database.subjects.insert_one(
        {
            "user_id": user_id,
            "academic_period_id": period_id,
            "name": name,
            "name_normalized": name.lower(),
            "color": color,
            "mock_key": MOCK_KEY,
        }
    ).inserted_id
    return database.subjects.find_one({"_id": subject_id})


def _find_or_create_topic(database, user_id, period_id, subject_id, title, parent_id=None):
    query = {
        "user_id": user_id,
        "academic_period_id": period_id,
        "subject_id": subject_id,
        "title_normalized": title.lower(),
        "parent_id": parent_id,
    }
    topic = database.topics.find_one(query)
    if topic:
        return topic
    topic_id = database.topics.insert_one(
        {
            **query,
            "title": title,
            "status": "IN_PROGRESS",
            "difficulty": "MEDIUM",
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
            "mock_key": MOCK_KEY,
        }
    ).inserted_id
    return database.topics.find_one({"_id": topic_id})


def seed() -> dict[str, int]:
    database = get_database()
    user = database.users.find_one({"email": EMAIL}, {"_id": 1, "identity": 1})
    if not user:
        raise RuntimeError("A conta informada não foi encontrada no banco.")

    user_id = user["_id"]
    period = _find_or_create_period(database, user_id)
    period_id = period["_id"]
    database.users.update_one(
        {"_id": user_id}, {"$set": {"current_academic_period_id": period_id}}
    )

    subject_specs = [
        ("Interação Humano-Computador", "#176B5D"),
        ("Banco de Dados", "#4D7C9B"),
        ("Engenharia de Software", "#C58B22"),
        ("Programação Web", "#8E6BBE"),
    ]
    subjects = [
        _find_or_create_subject(database, user_id, period_id, name, color)
        for name, color in subject_specs
    ]

    topic_specs = [
        [("Heurísticas de Nielsen", ["Avaliação", "Usabilidade"]), ("Acessibilidade", ["WCAG", "Contraste"])],
        [("Modelagem relacional", ["Entidades", "Relacionamentos"]), ("Consultas SQL", ["JOIN", "Agregações"])],
        [("Gestão ágil", ["Scrum", "Backlog"]), ("Qualidade", ["Testes", "Refatoração"])],
        [("Interfaces", ["Formulários", "Responsividade"]), ("APIs", ["HTTP", "Integração"])],
    ]
    topics_by_subject = {}
    for subject, groups in zip(subjects, topic_specs):
        topics_by_subject[subject["_id"]] = []
        for title, children in groups:
            parent = _find_or_create_topic(database, user_id, period_id, subject["_id"], title)
            topics_by_subject[subject["_id"]].append(parent)
            for child_title in children:
                topics_by_subject[subject["_id"]].append(
                    _find_or_create_topic(
                        database, user_id, period_id, subject["_id"], child_title, parent["_id"]
                    )
                )

    existing_mock = database.study_sessions.count_documents({"user_id": user_id, "mock_key": MOCK_KEY})
    sessions_created = 0
    meetings_created = 0
    if not existing_mock:
        today = date.today()
        session_specs = [
            (0, "08:00", 45, 0, "Revisar princípios de usabilidade", "Concluída"),
            (0, "14:00", 60, 1, "Praticar consultas com JOIN", "Pendente"),
            (1, "09:00", 50, 2, "Refinar o backlog do projeto", "Pendente"),
            (1, "16:00", 30, 3, "Ajustar formulário responsivo", "Concluída"),
            (2, "10:00", 60, 0, "Avaliar uma interface com heurísticas", "Pendente"),
            (2, "15:30", 45, 1, "Modelar relacionamentos", "Pendente"),
            (3, "08:30", 40, 2, "Escrever testes de unidade", "Pendente"),
            (3, "18:00", 60, 3, "Estudar integração HTTP", "Pendente"),
            (4, "09:30", 50, 0, "Revisar acessibilidade", "Pendente"),
            (5, "10:00", 90, 1, "Resolver exercícios SQL", "Pendente"),
        ]
        session_documents = []
        for day_offset, study_time, duration, subject_index, topic, status in session_specs:
            subject = subjects[subject_index]
            topic_id = topics_by_subject[subject["_id"]][0]["_id"]
            session_documents.append(
                {
                    "user_id": user_id,
                    "academic_period_id": period_id,
                    "subject_id": subject["_id"],
                    "topic_id": topic_id,
                    "topic": topic,
                    "study_date": (today + timedelta(days=day_offset)).isoformat(),
                    "study_time": study_time,
                    "duration": duration,
                    "priority": "Alta" if duration >= 60 else "Média",
                    "status": status,
                    "goal": "Concluir uma etapa pequena e registrar o que ficou claro.",
                    "mock_key": MOCK_KEY,
                }
            )
        database.study_sessions.insert_many(session_documents)
        sessions_created = len(session_documents)

        meeting_documents = []
        for weekday, subject_index, start, end, location in [
            (0, 0, "08:00", "10:00", "Sala 204"),
            (1, 1, "14:00", "16:00", "Laboratório 3"),
            (2, 2, "10:00", "12:00", "Sala 108"),
            (3, 3, "16:00", "18:00", "Online"),
            (4, 0, "08:00", "10:00", "Sala 204"),
        ]:
            subject = subjects[subject_index]
            meeting_documents.append(
                {
                    "user_id": user_id,
                    "academic_period_id": period_id,
                    "subject_id": subject["_id"],
                    "weekday": weekday,
                    "start_time": start,
                    "end_time": end,
                    "location": location,
                    "mock_key": MOCK_KEY,
                    "created_at": datetime.now(UTC),
                    "updated_at": datetime.now(UTC),
                }
            )
        database.class_meetings.insert_many(meeting_documents)
        meetings_created = len(meeting_documents)

    return {
        "subjects": len(subjects),
        "topics": sum(len(items) for items in topics_by_subject.values()),
        "sessions_created": sessions_created,
        "meetings_created": meetings_created,
    }


if __name__ == "__main__":
    print(seed())
