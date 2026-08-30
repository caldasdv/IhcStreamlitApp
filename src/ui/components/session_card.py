"""Card visual de uma sessão de estudo."""

from __future__ import annotations

import re
from html import escape

import streamlit as st

from src.domain.session_rules import effective_status
from src.ui.components.status_badge import render_status


def render_session_card(row: dict) -> None:
    with st.container(border=True):
        info_col, status_col = st.columns([5, 1])
        info_col.caption(f"{row['study_time']} · {row['duration']} minutos")
        subject_color = row.get("subject_color", "#787774")
        if isinstance(subject_color, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", subject_color):
            safe_subject_name = escape(str(row["subject_name"]))
            info_col.markdown(
                f'<span class="subject-dot" style="background:{subject_color}" '
                f'aria-label="Cor da disciplina {subject_color}"></span> **{safe_subject_name}**',
                unsafe_allow_html=True,
            )
        else:
            info_col.write(f"**{row['subject_name']}**")
        info_col.subheader(row["topic"])
        if row["goal"]:
            info_col.write(row["goal"])
        status = effective_status(row)
        with status_col:
            render_status(status)
