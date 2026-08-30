"""Visão semanal com ações rápidas."""

from datetime import date, timedelta

import streamlit as st

from src.domain.session_rules import effective_status
from src.ui.context import load_page_context
from src.ui.sidebar import render_account_sidebar


services, user, subjects = load_page_context()
render_account_sidebar(services, user)

st.caption("PLANEJAMENTO")
st.title("Visão semanal")
st.write("Revise sua carga de estudos e conclua sessões rapidamente.")

sessions = services.sessions.list_for_user(user["_id"], subjects)
week_start = date.today() - timedelta(days=date.today().weekday())
weekdays = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]

for day_offset, weekday in enumerate(weekdays):
    current_day = week_start + timedelta(days=day_offset)
    day_sessions = [session for session in sessions if session["study_date"] == current_day.isoformat()]
    with st.container(border=True):
        st.subheader(f"{weekday}, {current_day.day:02d}/{current_day.month:02d}")
        if not day_sessions:
            st.caption("Nenhuma sessão planejada.")
            continue
        for session in day_sessions:
            subject = session.get("subject_name", "Sem disciplina")
            status = effective_status(session)
            row_col, action_col = st.columns([5, 1])
            row_col.write(f"**{session['study_time']} · {session['topic']}**")
            row_col.caption(f"{subject} · {session['duration']} min · {status}")
            if status != "Concluída" and action_col.button("Concluir", key=f"complete_{session['_id']}", width="stretch"):
                services.sessions.complete(session["_id"], user["_id"])
                st.rerun()
