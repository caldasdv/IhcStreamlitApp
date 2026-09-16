"""Resumo visual de progresso por disciplina."""

from __future__ import annotations

from collections.abc import Iterable
from html import escape
from typing import Any

import streamlit as st


def render_subject_progress_summary(summary: Iterable[dict[str, Any]]) -> None:
    """Renderiza barras de progresso com texto equivalente e estado explícito."""
    rows = list(summary)
    if not rows:
        st.info("Ainda não há disciplinas para acompanhar nesta visão.")
        return

    cards: list[str] = []
    for row in rows:
        planned = int(row["planejados"])
        completed = int(row["concluídos"])
        percentage = min(completed / planned * 100, 100) if planned else 0
        cards.append(
            '<article class="plan-progress-card">'
            f'<div class="plan-progress-card-heading"><strong>{escape(str(row["disciplina"]))}</strong>'
            f'<span>{percentage:.0f}%</span></div>'
            f'<div class="plan-progress-track" role="progressbar" aria-valuenow="{percentage:.0f}" '
            'aria-valuemin="0" aria-valuemax="100" '
            f'aria-label="Progresso em {escape(str(row["disciplina"]))}">'
            f'<span style="width:{percentage:.0f}%"></span></div>'
            f'<div class="plan-progress-card-meta">{completed} de {planned} minutos concluídos</div>'
            f'<div class="plan-progress-card-status">{int(row["pendentes"])} pendentes · '
            f'{int(row["atrasadas"])} atrasadas</div>'
            '</article>'
        )
    st.markdown(
        '<div class="plan-progress-grid">' + "".join(cards) + "</div>",
        unsafe_allow_html=True,
    )
