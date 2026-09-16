"""Cria uma carga demonstrativa extensa para uma conta existente."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.database.connection import get_database


EMAIL = "david.pereira3@estudante.ifb.edu.br"
MOCK_KEY = "david-pereira-rich-demo-v1"


def _period(database, user_id):
    current = database.academic_periods.find_one(
        {"user_id": user_id, "status": "ACTIVE"}, sort=[("start_date", -1)]
    )
    if current:
        return current
    today = date.today()
    period_id = database.academic_periods.insert_one(
        {
            "user_id": user_id,
            "name": "Semestre em movimento",
            "name_normalized": "semestre em movimento",
            "start_date": (today - timedelta(days=90)).isoformat(),
            "end_date": (today + timedelta(days=30)).isoformat(),
            "status": "ACTIVE",
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
            "mock_key": MOCK_KEY,
        }
    ).inserted_id
    return database.academic_periods.find_one({"_id": period_id})


def _subject(database, user_id, period_id, name, color):
    found = database.subjects.find_one(
        {"user_id": user_id, "academic_period_id": period_id, "name_normalized": name.lower()}
    )
    if found:
        return found
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


def _topic(database, user_id, period_id, subject_id, title, parent_id=None):
    query = {
        "user_id": user_id,
        "academic_period_id": period_id,
        "subject_id": subject_id,
        "title_normalized": title.lower(),
        "parent_id": parent_id,
    }
    found = database.topics.find_one(query)
    if found:
        return found
    topic_id = database.topics.insert_one(
        {
            **query,
            "title": title,
            "status": "MASTERED" if parent_id and title.endswith("prática") else "IN_PROGRESS",
            "difficulty": "HIGH" if title in {"Integração", "Consultas SQL"} else "MEDIUM",
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
            "mock_key": MOCK_KEY,
        }
    ).inserted_id
    return database.topics.find_one({"_id": topic_id})


def seed() -> dict[str, int]:
    database = get_database()
    user = database.users.find_one({"email": EMAIL}, {"_id": 1})
    if not user:
        raise RuntimeError(f"A conta {EMAIL} não foi encontrada no banco.")

    user_id = user["_id"]
    period = _period(database, user_id)
    period_id = period["_id"]
    database.users.update_one(
        {"_id": user_id},
        {"$set": {"current_academic_period_id": period_id, "weekly_goal_minutes": 600}},
    )

    subject_specs = [
        ("Interação Humano-Computador", "#176B5D"),
        ("Banco de Dados", "#4D7C9B"),
        ("Engenharia de Software", "#C58B22"),
        ("Programação Web", "#8E6BBE"),
    ]
    subjects = [_subject(database, user_id, period_id, *spec) for spec in subject_specs]
    topic_groups = [
        ("Fundamentos", ["Heurísticas", "Acessibilidade", "Avaliação prática"]),
        ("Modelagem", ["Entidades", "Relacionamentos", "Consultas SQL"]),
        ("Processos", ["Scrum", "Backlog", "Testes"]),
        ("Aplicações", ["Interfaces", "Integração", "Responsividade"]),
    ]
    topic_ids = []
    topics_count = 0
    for subject, (root_title, children) in zip(subjects, topic_groups):
        root = _topic(database, user_id, period_id, subject["_id"], root_title)
        topic_ids.append(root["_id"])
        topics_count += 1
        for title in children:
            _topic(database, user_id, period_id, subject["_id"], title, root["_id"])
            topics_count += 1

    existing = database.study_sessions.count_documents(
        {"user_id": user_id, "mock_key": MOCK_KEY}
    )
    sessions_created = 0
    if not existing:
        today = date.today()
        documents = []
        for offset in range(-90, 31):
            study_date = today + timedelta(days=offset)
            if study_date.weekday() >= 5:
                continue
            for slot, study_time in enumerate(("08:00", "18:00")):
                subject_index = (study_date.toordinal() + slot) % len(subjects)
                duration = (30, 45, 60)[(study_date.toordinal() + slot) % 3]
                is_past = offset < 0
                completed = is_past and (study_date.toordinal() + slot) % 4 != 0
                documents.append(
                    {
                        "user_id": user_id,
                        "academic_period_id": period_id,
                        "subject_id": subjects[subject_index]["_id"],
                        "topic_id": topic_ids[subject_index],
                        "topic": topic_groups[subject_index][1][slot % 3],
                        "study_date": study_date.isoformat(),
                        "study_time": study_time,
                        "duration": duration,
                        "priority": "Alta" if duration == 60 else "Média",
                        "status": "Concluída" if completed else "Pendente",
                        "goal": "Avançar uma etapa e registrar o que ficou claro.",
                        "mock_key": MOCK_KEY,
                    }
                )
        if documents:
            database.study_sessions.insert_many(documents)
            sessions_created = len(documents)

    meeting_documents = []
    if not database.class_meetings.count_documents({"user_id": user_id, "mock_key": MOCK_KEY}):
        for weekday, subject_index, start, end, location in [
            (0, 0, "08:00", "10:00", "Sala 204"),
            (1, 1, "14:00", "16:00", "Laboratório 3"),
            (2, 2, "10:00", "12:00", "Sala 108"),
            (3, 3, "16:00", "18:00", "Online"),
            (4, 0, "08:00", "10:00", "Sala 204"),
        ]:
            meeting_documents.append(
                {
                    "user_id": user_id,
                    "academic_period_id": period_id,
                    "subject_id": subjects[subject_index]["_id"],
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

    return {
        "subjects": len(subjects),
        "topics": topics_count,
        "sessions_created": sessions_created,
        "meetings_created": len(meeting_documents),
    }


if __name__ == "__main__":
    print(seed())
