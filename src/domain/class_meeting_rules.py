"""Regras puras para horários recorrentes de aula."""

from __future__ import annotations

from datetime import time
from typing import Mapping


def minutes_at(value: time | str) -> int:
    """Converte horário em minutos desde meia-noite."""
    try:
        parsed = value if isinstance(value, time) else time.fromisoformat(value)
    except ValueError as error:
        raise ValueError("Informe um horário válido.") from error
    return parsed.hour * 60 + parsed.minute


def validate_class_meeting(weekday: int, start_time: time, end_time: time) -> None:
    """Valida dia e intervalo de uma aula semanal."""
    if weekday not in range(7):
        raise ValueError("Selecione um dia da semana válido.")
    if minutes_at(start_time) >= minutes_at(end_time):
        raise ValueError("O horário final deve ser posterior ao horário inicial.")


def class_meetings_conflict(
    start_time: time,
    end_time: time,
    existing_meetings: list[Mapping[str, object]],
) -> bool:
    """Indica sobreposição no mesmo dia; horários adjacentes são permitidos."""
    start = minutes_at(start_time)
    end = minutes_at(end_time)
    for meeting in existing_meetings:
        existing_start = minutes_at(str(meeting["start_time"]))
        existing_end = minutes_at(str(meeting["end_time"]))
        if start < existing_end and existing_start < end:
            return True
    return False
