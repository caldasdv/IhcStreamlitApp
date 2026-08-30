"""Regras puras do domínio de sessões de estudo."""

from __future__ import annotations

from datetime import date, time
from typing import Mapping


class SessionValidationError(ValueError):
    """Indica que os dados básicos de uma sessão são inválidos."""


class SessionConflictError(SessionValidationError):
    """Indica sobreposição com outra sessão pendente."""


def effective_status(row: Mapping[str, object], today: date | None = None) -> str:
    """Retorna o status exibido, considerando sessões pendentes atrasadas."""
    current_date = today or date.today()
    status = str(row["status"])
    study_date = str(row["study_date"])
    if status == "Pendente" and study_date < current_date.isoformat():
        return "Atrasada"
    return status


def minutes_at(value: str) -> int:
    """Converte um horário HH:MM em minutos desde meia-noite."""
    if len(value) != 5 or value[2] != ":":
        raise SessionValidationError("Horário deve estar no formato HH:MM.")
    try:
        parsed = time.fromisoformat(value)
    except ValueError as error:
        raise SessionValidationError("Horário deve estar no formato HH:MM.") from error
    return parsed.hour * 60 + parsed.minute


def validate_new_session(
    *,
    topic: str,
    study_date: date,
    duration: int,
    today: date | None = None,
) -> None:
    """Valida os invariantes de uma nova sessão planejada."""
    current_date = today or date.today()
    if not topic.strip():
        raise SessionValidationError("Informe o assunto da sessão.")
    if study_date < current_date:
        raise SessionValidationError("Escolha hoje ou uma data futura para planejar uma sessão.")
    if duration <= 0:
        raise SessionValidationError("A duração deve ser maior que zero.")


def sessions_conflict(
    study_time: time,
    duration: int,
    existing_sessions: list[Mapping[str, object]],
) -> bool:
    """Verifica sobreposição com sessões pendentes do mesmo dia."""
    start = study_time.hour * 60 + study_time.minute
    end = start + duration
    for item in existing_sessions:
        existing_start = minutes_at(str(item["study_time"]))
        existing_duration = int(item["duration"])
        if start < existing_start + existing_duration and existing_start < end:
            return True
    return False
