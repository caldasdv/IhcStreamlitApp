"""Dados demonstrativos usados apenas quando o banco ainda está vazio."""

from __future__ import annotations

from datetime import date, timedelta


def seed_database(database) -> None:
    if database.users.find_one({}):
        return
    user_id = database.users.insert_one(
        {
            "name": "Marina Oliveira",
            "email": "marina.teste@exemplo.com",
            "weekly_goal_minutes": 300,
        }
    ).inserted_id
    subjects = [
        {"user_id": user_id, "name": "Interação Humano-Computador", "color": "#5E6AD2"},
        {"user_id": user_id, "name": "Banco de Dados", "color": "#2E8B72"},
        {"user_id": user_id, "name": "Programação Web", "color": "#C47F17"},
    ]
    subject_ids = [database.subjects.insert_one(subject).inserted_id for subject in subjects]
    today = date.today()
    database.study_sessions.insert_many(
        [
            {
                "user_id": user_id,
                "subject_id": subject_ids[0],
                "topic": "Heurísticas de Nielsen",
                "study_date": today.isoformat(),
                "study_time": "14:00",
                "duration": 60,
                "priority": "Alta",
                "status": "Pendente",
                "goal": "Revisar as 10 heurísticas e fazer anotações.",
            },
            {
                "user_id": user_id,
                "subject_id": subject_ids[1],
                "topic": "Relacionamentos e chaves",
                "study_date": (today + timedelta(days=1)).isoformat(),
                "study_time": "16:30",
                "duration": 45,
                "priority": "Média",
                "status": "Pendente",
                "goal": "Resolver cinco exercícios do material.",
            },
            {
                "user_id": user_id,
                "subject_id": subject_ids[2],
                "topic": "Revisão de formulários",
                "study_date": (today - timedelta(days=1)).isoformat(),
                "study_time": "19:00",
                "duration": 50,
                "priority": "Baixa",
                "status": "Concluída",
                "goal": "Praticar validação de campos.",
            },
        ]
    )
