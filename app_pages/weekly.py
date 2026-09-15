"""Visão semanal com ações rápidas."""

from datetime import date, timedelta

import streamlit as st

from src.domain.session_rules import effective_status
from src.ui.components.session_card import render_session_card
from src.ui.context import load_page_context, load_page_sessions
from src.ui.components.page_header import render_page_header
from src.ui.feedback import show_action_error
from src.ui.feedback import set_success_flash
from src.ui.sidebar import render_account_sidebar


services, user, subjects = load_page_context()
render_account_sidebar(services, user)

render_page_header("PLANEJAMENTO", "Visão semanal", "Revise sua carga de estudos e conclua sessões rapidamente.")

week_start = date.today() - timedelta(days=date.today().weekday())
week_end = week_start + timedelta(days=6)
sessions = load_page_sessions(
    services,
    user,
    subjects,
    start_date=week_start,
    end_date=week_end,
    retry_key="retry_weekly_sessions",
)
weekdays = [
    "segunda-feira",
    "terça-feira",
    "quarta-feira",
    "quinta-feira",
    "sexta-feira",
    "sábado",
    "domingo",
]

planned_minutes = sum(session["duration"] for session in sessions)
pending_sessions = [
    session for session in sessions if effective_status(session) != "Concluída"
]
st.caption(f"{week_start:%d/%m} a {week_end:%d/%m/%Y}")
summary_columns = st.columns(3)
summary_columns[0].metric("Sessões", len(sessions))
summary_columns[1].metric("Tempo planejado", f"{planned_minutes} min")
summary_columns[2].metric("Pendentes", len(pending_sessions))

if not sessions:
    st.info("Sua semana ainda está vazia. Crie uma sessão para começar a organizar seus estudos.")
    if st.button("Criar nova sessão", type="primary", icon=":material/add_circle:"):
        st.switch_page("app_pages/new_session.py")

day_tabs = st.tabs(
    [
        f"{weekday[:3].title()} {week_start + timedelta(days=day_offset):%d/%m}"
        for day_offset, weekday in enumerate(weekdays)
    ]
)
for day_offset, (weekday, day_tab) in enumerate(zip(weekdays, day_tabs)):
    current_day = week_start + timedelta(days=day_offset)
    day_sessions = [session for session in sessions if session["study_date"] == current_day.isoformat()]
    with day_tab:
        st.subheader(f"{weekday}, {current_day:%d/%m/%Y}")
        if not day_sessions:
            st.caption("Nenhuma sessão planejada.")
            continue
        for session in day_sessions:
            action = render_session_card(session, key=f"weekly_session_{session['_id']}")
            if action == "complete":
                try:
                    services.sessions.complete(session["_id"], user["_id"])
                except Exception as error:
                    show_action_error("concluir a sessão", error)
                else:
                    set_success_flash("Sessão concluída.")
                    st.rerun()
