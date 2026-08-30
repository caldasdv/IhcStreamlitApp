"""Card visual de uma sessão de estudo."""

from __future__ import annotations

import streamlit as st

from src.domain.session_rules import effective_status


def render_session_card(row: dict) -> None:
    with st.container(border=True):
        info_col, status_col = st.columns([5, 1])
        info_col.caption(f"{row['study_time']} · {row['duration']} minutos")
        info_col.write(f"**{row['subject_name']}**")
        info_col.subheader(row["topic"])
        if row["goal"]:
            info_col.write(row["goal"])
        status = effective_status(row)
        if status == "Concluída":
            status_col.success("Concluída")
        elif status == "Atrasada":
            status_col.error("Atrasada")
        else:
            status_col.warning("Pendente")
