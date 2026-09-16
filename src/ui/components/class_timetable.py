"""Visualização da grade semanal de aulas."""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from html import escape
from typing import Any

import streamlit as st


def render_class_timetable(
    meetings: Iterable[dict[str, Any]], weekdays: Sequence[str]
) -> None:
    """Renderiza uma visão semanal visual sem transformar aulas em eventos de calendário."""
    meetings = list(meetings)
    meetings_by_day = {
        weekday: [meeting for meeting in meetings if meeting["weekday"] == weekday]
        for weekday in range(len(weekdays))
    }
    day_markup: list[str] = []
    for weekday, weekday_name in enumerate(weekdays):
        meeting_markup: list[str] = []
        for meeting in meetings_by_day[weekday]:
            color = meeting.get("subject_color", "#176B5D")
            safe_color = color if isinstance(color, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", color) else "#176B5D"
            location = (
                f'<span class="plan-meeting-location">{escape(str(meeting["location"]))}</span>'
                if meeting.get("location")
                else ""
            )
            meeting_markup.append(
                f'<article class="plan-meeting" style="--meeting-color:{safe_color}">'
                f'<strong>{escape(str(meeting["start_time"]))}–{escape(str(meeting["end_time"]))}</strong>'
                f'<span>{escape(str(meeting["subject_name"]))}</span>{location}</article>'
            )
        if not meeting_markup:
            meeting_markup.append('<p class="plan-timetable-empty">Livre</p>')
        day_markup.append(
            f'<section class="plan-timetable-day" aria-label="{escape(weekday_name)}">'
            f'<h3>{escape(weekday_name[:3])}</h3>{"".join(meeting_markup)}</section>'
        )
    st.markdown(
        '<div class="plan-timetable-scroll"><div class="plan-timetable" role="list">'
        + "".join(day_markup)
        + "</div></div>",
        unsafe_allow_html=True,
    )
