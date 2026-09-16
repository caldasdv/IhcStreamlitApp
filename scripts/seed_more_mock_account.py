"""Adiciona uma segunda camada de dados demonstrativos sem duplicar a primeira carga."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.database.connection import get_database


EMAIL = "david.pereira3@estudante.ifb.edu.br"
MOCK_KEY = "david-pereira-extra-demo-v1"


def seed() -> dict[str, int]:
    database = get_database()
    user = database.users.find_one({"email": EMAIL}, {"_id": 1})
    if not user:
        raise RuntimeError(f"A conta {EMAIL} não foi encontrada no banco.")

    user_id = user["_id"]
    period = database.academic_periods.find_one(
        {"user_id": user_id, "status": "ACTIVE"}, sort=[("start_date", -1)]
    )
    if not period:
        raise RuntimeError("A conta não possui um período acadêmico ativo.")

    subjects = list(
        database.subjects.find(
            {"user_id": user_id, "academic_period_id": period["_id"]},
            {"_id": 1, "name": 1},
        ).sort("name", 1)
    )
    if not subjects:
        raise RuntimeError("A conta não possui disciplinas no período atual.")

    existing = database.study_sessions.count_documents(
        {"user_id": user_id, "mock_key": MOCK_KEY}
    )
    if existing:
        return {"sessions_created": 0, "already_seeded": existing}

    topics_by_subject = {}
    for subject in subjects:
        topics_by_subject[subject["_id"]] = list(
            database.topics.find(
                {
                    "user_id": user_id,
                    "academic_period_id": period["_id"],
                    "subject_id": subject["_id"],
                },
                {"_id": 1, "title": 1},
            ).sort("title", 1)
        )

    today = date.today()
    documents = []
    for offset in range(-90, 31):
        study_date = today + timedelta(days=offset)
        subject = subjects[(study_date.toordinal() // 3) % len(subjects)]
        subject_topics = topics_by_subject.get(subject["_id"], [])
        topic = subject_topics[study_date.toordinal() % len(subject_topics)] if subject_topics else None
        completed = offset < 0 and study_date.toordinal() % 3 != 0
        duration = (25, 40, 50, 75)[study_date.toordinal() % 4]
        documents.append(
            {
                "user_id": user_id,
                "academic_period_id": period["_id"],
                "subject_id": subject["_id"],
                "topic_id": topic["_id"] if topic else None,
                "topic": topic["title"] if topic else "Revisão geral",
                "study_date": study_date.isoformat(),
                "study_time": "12:30" if study_date.weekday() < 5 else "10:30",
                "duration": duration,
                "priority": "Alta" if duration >= 60 else "Baixa",
                "status": "Concluída" if completed else "Pendente",
                "goal": "Revisar o conteúdo e registrar uma ideia principal.",
                "mock_key": MOCK_KEY,
            }
        )

    database.study_sessions.insert_many(documents)
    return {"sessions_created": len(documents), "already_seeded": 0}


if __name__ == "__main__":
    print(seed())
