"""Visualização compacta do ritmo semanal de estudos."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date, timedelta
from html import escape
from typing import Any

from src.domain.session_rules import effective_status
import streamlit as st


def render_study_rhythm(
    sessions: Iterable[dict[str, Any]], week_start: date, *, title: str = "Ritmo da semana"
) -> None:
    """Mostra consistência e volume por dia sem substituir a agenda detalhada."""
    rows = list(sessions)
    cards: list[str] = []
    weekdays = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
    for offset, label in enumerate(weekdays):
        current_day = week_start + timedelta(days=offset)
        day_rows = [row for row in rows if row["study_date"] == current_day.isoformat()]
        completed = sum(
            int(row["duration"])
            for row in day_rows
            if effective_status(row, today=date.today()) == "Concluída"
        )
        planned = sum(int(row["duration"]) for row in day_rows)
        percentage = min(completed / planned * 100, 100) if planned else 0
        state = "done" if completed else "planned" if planned else "empty"
        cards.append(
            f'<article class="plan-rhythm-day plan-rhythm-{state}">'
            f'<span>{label}</span><strong>{current_day.day:02d}</strong>'
            f'<i><b style="height:{percentage:.0f}%"></b></i>'
            f'<small>{completed if completed else planned} min</small></article>'
        )
    st.html(
        f'<section class="plan-rhythm"><div class="plan-rhythm-heading">'
        f'<strong>{escape(title)}</strong><span>concluído / planejado</span></div>'
        f'<div class="plan-rhythm-grid">{"".join(cards)}</div></section>'
    )
