"""Tela de progresso e dashboard analítico."""

from datetime import date, timedelta

import streamlit as st

from src.domain.session_rules import effective_status
from src.services.report_service import build_subject_summary, build_week_summary
from src.ui.context import load_page_context
from src.ui.sidebar import render_account_sidebar


services, user, subjects = load_page_context()
render_account_sidebar(services, user)

st.caption("ACOMPANHAMENTO")
st.title("Seu progresso")
st.write("Entenda sua carga de estudos e o que já foi concluído.")
progress_sessions = services.sessions.list_for_user(user["_id"], subjects)
week_start = st.date_input(
    "Início da semana",
    value=date.today() - timedelta(days=date.today().weekday()),
    format="DD/MM/YYYY",
    key="progress_week_start",
)
week_start -= timedelta(days=week_start.weekday())
week_summary = build_week_summary(progress_sessions, week_start)
subject_summary = build_subject_summary(progress_sessions, subjects)
planned_minutes = sum(row["planejados"] for row in week_summary)
completed_minutes = sum(row["concluídos"] for row in week_summary)
pending_count = sum(row["pendentes"] for row in week_summary)
overdue_count = sum(row["atrasadas"] for row in week_summary)

if not progress_sessions:
    st.info("Adicione uma sessão para começar a acompanhar seu progresso.")
else:
    metric_cols = st.columns(4)
    metric_cols[0].metric("Planejados", f"{planned_minutes} min", border=True)
    metric_cols[1].metric("Concluídos", f"{completed_minutes} min", border=True)
    metric_cols[2].metric("Pendências", pending_count, border=True)
    metric_cols[3].metric("Atrasadas", overdue_count, border=True)

    chart_col, table_col = st.columns(2)
    with chart_col:
        with st.container(border=True):
            st.subheader("Carga por disciplina")
            st.caption("Minutos planejados e concluídos na semana selecionada.")
            st.bar_chart(subject_summary, x="disciplina", y=["planejados", "concluídos"], horizontal=True)
    with table_col:
        with st.container(border=True):
            st.subheader("Ritmo ao longo da semana")
            st.caption("Compare a carga planejada com o que foi concluído em cada dia.")
            st.line_chart(week_summary, x="dia", y=["planejados", "concluídos"])

    st.subheader("Detalhamento por disciplina")
    for row in subject_summary:
        planned = row["planejados"]
        done = row["concluídos"]
        with st.container(border=True):
            st.write(f"**{row['disciplina']}**")
            st.progress(done / planned if planned else 0, text=f"{done} de {planned} minutos concluídos")
            st.caption(f"{row['pendentes']} pendentes · {row['atrasadas']} atrasadas")
