"""Tela de visão geral."""

from datetime import date, timedelta

import streamlit as st

from src.domain.session_rules import effective_status
from src.ui.components.session_card import render_session_card
from src.ui.context import load_page_context
from src.ui.sidebar import render_account_sidebar


services, user, subjects = load_page_context()
render_account_sidebar(services, user)

st.caption("SEMANA DE ESTUDOS")
st.title(f"Olá, {user['name'].split()[0]}")
st.write("Aqui está o que você planejou para os próximos dias.")
all_sessions = services.sessions.list_for_user(user["_id"], subjects)
pending = [s for s in all_sessions if effective_status(s) in ("Pendente", "Atrasada")]
completed = [s for s in all_sessions if effective_status(s) == "Concluída"]
week_start = date.today() - timedelta(days=date.today().weekday())
week_end = week_start + timedelta(days=6)
week_sessions = [s for s in all_sessions if str(week_start) <= s["study_date"] <= str(week_end)]
completed_minutes = sum(s["duration"] for s in week_sessions if effective_status(s) == "Concluída")
goal_minutes = user.get("weekly_goal_minutes", 300)
col1, col2, col3 = st.columns(3)
col1.write("**Pendências**")
col1.title(len(pending))
col2.write("**Progresso da semana**")
col2.title(f"{completed_minutes / 60:.1f} / {goal_minutes / 60:.1f}h")
col3.write("**Sessões concluídas**")
col3.title(len(completed))
st.progress(
    min(completed_minutes / goal_minutes, 1.0) if goal_minutes else 0.0,
    text=f"{completed_minutes / goal_minutes * 100:.0f}% da meta semanal" if goal_minutes else "Sem meta",
)
st.divider()
selected_date = st.date_input("Ver dia", value=date.today(), format="DD/MM/YYYY", key="overview_date")
day_sessions = [s for s in all_sessions if s["study_date"] == str(selected_date)]
weekdays = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
st.subheader(f"{weekdays[selected_date.weekday()]}, {selected_date.day:02d}/{selected_date.month:02d}")
if not day_sessions:
    st.info("Nenhuma sessão planejada para este dia.")
for row in day_sessions:
    render_session_card(row)
if day_sessions:
    st.subheader("Atualizar sessão")
    session_labels = {f"{item['study_time']} — {item['topic']}": item["_id"] for item in day_sessions}
    chosen_label = st.selectbox("Escolha uma sessão", list(session_labels), key="overview_session")
    chosen_id = session_labels[chosen_label]
    chosen = next(item for item in day_sessions if item["_id"] == chosen_id)
    action_col1, action_col2 = st.columns([1, 1])
    if effective_status(chosen) != "Concluída" and action_col1.button("Marcar como concluída", width="stretch"):
        services.sessions.complete(chosen["_id"], user["_id"])
        st.rerun()
    if action_col2.button("Excluir sessão", width="stretch"):
        services.sessions.delete(chosen["_id"], user["_id"])
        st.rerun()
