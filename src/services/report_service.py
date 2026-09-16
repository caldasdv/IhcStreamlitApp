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


def build_topic_summary(
    sessions: Iterable[dict[str, Any]], topics: Iterable[dict[str, Any]], today: date | None = None
) -> list[dict[str, Any]]:
    """Calcula o progresso real de cada conteúdo a partir das sessões vinculadas."""
    sessions_by_topic: dict[Any, list[dict[str, Any]]] = {}
    for session in sessions:
        if session.get("topic_id") is not None:
            sessions_by_topic.setdefault(session["topic_id"], []).append(session)

    summary = []
    for topic in topics:
        rows = sessions_by_topic.get(topic["_id"], [])
        planned = sum(int(row["duration"]) for row in rows)
        completed = sum(
            int(row["duration"])
            for row in rows
            if effective_status(row, today=today) == "Concluída"
        )
        summary.append(
            {
                "topic_id": topic["_id"],
                "title": topic["title"],
                "planned_minutes": planned,
                "completed_minutes": completed,
                "session_count": len(rows),
                "progress": completed / planned if planned else 0.0,
            }
        )
    return summary


def build_evaluation_summary(
    evaluations: Iterable[dict[str, Any]], subjects: Iterable[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Resume média proporcional e aproveitamento por disciplina."""
    evaluations_by_subject: dict[Any, list[dict[str, Any]]] = {}
    for evaluation in evaluations:
        if evaluation.get("score") is None or not evaluation.get("max_score"):
            continue
        evaluations_by_subject.setdefault(evaluation["subject_id"], []).append(evaluation)

    summary = []
    for subject in subjects:
        rows = evaluations_by_subject.get(subject["_id"], [])
        if not rows:
            continue
        average = sum(row["score"] / row["max_score"] for row in rows) / len(rows)
        summary.append(
            {
                "disciplina": subject["name"],
                "avaliacoes": len(rows),
                "media": average * 10,
                "aproveitamento": average,
            }
        )
    return summary


def build_adaptive_goal_plan(
    subjects: Iterable[dict[str, Any]],
    topics_by_subject: dict[Any, list[dict[str, Any]]],
    evaluations: Iterable[dict[str, Any]],
    sessions: Iterable[dict[str, Any]],
    total_minutes: int,
    strategy: str = "Equilibrada",
) -> list[dict[str, Any]]:
    """Distribui a meta entre disciplinas usando sinais explicáveis do próprio usuário."""
    strategies = {
        "Equilibrada": (0.4, 0.3, 0.3),
        "Priorizar notas": (0.6, 0.2, 0.2),
        "Priorizar dificuldade": (0.2, 0.6, 0.2),
        "Priorizar pendências": (0.2, 0.2, 0.6),
    }
    note_weight, difficulty_weight, pending_weight = strategies.get(strategy, strategies["Equilibrada"])
    subject_list = list(subjects)
    if not subject_list or total_minutes <= 0:
        return []
    evaluations_by_subject: dict[Any, list[dict[str, Any]]] = {}
    for evaluation in evaluations:
        if evaluation.get("score") is not None and evaluation.get("max_score"):
            evaluations_by_subject.setdefault(evaluation["subject_id"], []).append(evaluation)
    pending_by_subject: dict[Any, int] = {}
    for session in sessions:
        if session.get("status") != "Concluída":
            pending_by_subject[session["subject_id"]] = pending_by_subject.get(session["subject_id"], 0) + int(session["duration"])
    max_pending = max(pending_by_subject.values(), default=1)
    raw_rows = []
    for subject in subject_list:
        subject_id = subject["_id"]
        subject_evaluations = evaluations_by_subject.get(subject_id, [])
        note_factor = (
            1 - sum(row["score"] / row["max_score"] for row in subject_evaluations) / len(subject_evaluations)
            if subject_evaluations else 0.5
        )
        topic_difficulties = topics_by_subject.get(subject_id, [])
        difficulty_values = {"LOW": 0.25, "MEDIUM": 0.6, "HIGH": 1.0}
        difficulty_factor = (
            sum(difficulty_values.get(topic.get("difficulty"), 0.5) for topic in topic_difficulties) / len(topic_difficulties)
            if topic_difficulties else 0.25
        )
        pending_factor = pending_by_subject.get(subject_id, 0) / max_pending
        score = note_factor * note_weight + difficulty_factor * difficulty_weight + pending_factor * pending_weight
        raw_rows.append((subject, score, note_factor, difficulty_factor, pending_factor))
    total_score = sum(row[1] for row in raw_rows) or 1
    allocations = [int(total_minutes * row[1] / total_score) for row in raw_rows]
    remainder = total_minutes - sum(allocations)
    order = sorted(range(len(raw_rows)), key=lambda index: raw_rows[index][1], reverse=True)
    for index in order[:remainder]:
        allocations[index] += 1
    result = []
    for allocation, (subject, score, note_factor, difficulty_factor, pending_factor) in zip(allocations, raw_rows):
        signals = [
            (note_factor, "notas abaixo do esperado"),
            (difficulty_factor, "conteúdos difíceis"),
            (pending_factor, "mais tempo pendente"),
        ]
        reason = max(signals, key=lambda signal: signal[0])[1]
        result.append({"disciplina": subject["name"], "minutos": allocation, "score": score, "motivo": reason})
    return result
