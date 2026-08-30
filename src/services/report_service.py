"""Transformações analíticas puras para o dashboard."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any, Iterable

from src.domain.session_rules import effective_status


def build_subject_summary(
    sessions: Iterable[dict[str, Any]], subjects: Iterable[dict[str, Any]], today: date | None = None
) -> list[dict[str, Any]]:
    """Resume minutos planejados, concluídos e pendentes por disciplina."""
    sessions_by_subject: dict[Any, list[dict[str, Any]]] = {}
    for session in sessions:
        sessions_by_subject.setdefault(session["subject_id"], []).append(session)

    summary = []
    for subject in subjects:
        rows = sessions_by_subject.get(subject["_id"], [])
        statuses = [effective_status(row, today=today) for row in rows]
        summary.append(
            {
                "disciplina": subject["name"],
                "planejados": sum(int(row["duration"]) for row in rows),
                "concluídos": sum(
                    int(row["duration"])
                    for row, status in zip(rows, statuses)
                    if status == "Concluída"
                ),
                "pendentes": sum(status == "Pendente" for status in statuses),
                "atrasadas": sum(status == "Atrasada" for status in statuses),
            }
        )
    return summary


def build_week_summary(
    sessions: Iterable[dict[str, Any]], week_start: date, today: date | None = None
) -> list[dict[str, Any]]:
    """Resume sessões por dia para uma semana iniciada na segunda-feira."""
    sessions_by_date: dict[str, list[dict[str, Any]]] = {}
    for session in sessions:
        sessions_by_date.setdefault(session["study_date"], []).append(session)

    weekdays = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
    summary = []
    for offset, weekday in enumerate(weekdays):
        current_day = week_start + timedelta(days=offset)
        rows = sessions_by_date.get(current_day.isoformat(), [])
        statuses = [effective_status(row, today=today) for row in rows]
        summary.append(
            {
                "dia": f"{weekday} {current_day.day:02d}/{current_day.month:02d}",
                "data": current_day.isoformat(),
                "planejados": sum(int(row["duration"]) for row in rows),
                "concluídos": sum(
                    int(row["duration"])
                    for row, status in zip(rows, statuses)
                    if status == "Concluída"
                ),
                "pendentes": sum(status == "Pendente" for status in statuses),
                "atrasadas": sum(status == "Atrasada" for status in statuses),
            }
        )
    return summary
