"""Visão semanal com ações rápidas."""

from datetime import date, timedelta

import streamlit as st

from src.domain.session_rules import effective_status
from src.ui.context import load_page_context, load_page_sessions
from src.ui.components.page_header import render_page_header
from src.ui.components.study_agenda import render_study_agenda
from src.ui.feedback import show_action_error
from src.ui.feedback import set_success_flash
from src.ui.sidebar import render_account_sidebar


services, user, subjects = load_page_context()
render_account_sidebar(services, user)

render_page_header("PLANEJAMENTO", "Visão semanal", "Revise sua carga de estudos e conclua sessões rapidamente.")

sessions = load_page_sessions(services, user, subjects)
week_start = date.today() - timedelta(days=date.today().weekday())
weekdays = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]

st.subheader("Agenda visual")
st.caption("Selecione uma sessão para consultar seus detalhes. A lista por dia abaixo continua disponível.")
try:
    selected_id = render_study_agenda(sessions, week_start, key="weekly_study_agenda")
except Exception:
    st.warning("A agenda visual está indisponível; use a lista por dia abaixo.")
    selected_id = None
if selected_id:
    selected_session = next((session for session in sessions if str(session["_id"]) == selected_id), None)
    if selected_session:
        st.info(
            f"Selecionada: {selected_session['study_time']} · {selected_session['topic']} "
            f"({selected_session['duration']} min, {effective_status(selected_session)})."
        )

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
                try:
                    services.sessions.complete(session["_id"], user["_id"])
                except Exception as error:
                    show_action_error("concluir a sessão", error)
                else:
                    set_success_flash("Sessão concluída.")
                    st.rerun()
