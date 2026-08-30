"""Tela de criação de sessão."""

from datetime import date, time

import streamlit as st

from src.ui.context import load_page_context
from src.ui.sidebar import render_account_sidebar


services, user, subjects = load_page_context()
render_account_sidebar(services, user)

st.caption("PLANEJAMENTO")
st.title("Nova sessão")
st.write("Defina uma sessão pequena e objetiva para facilitar o início do estudo.")
with st.form("new_session"):
    subject_names = [s["name"] for s in subjects]
    subject_name = st.selectbox("Disciplina", subject_names)
    topic = st.text_input("O que você vai estudar?", placeholder="Ex.: Heurísticas de Nielsen")
    goal = st.text_area("Objetivo da sessão", placeholder="Ex.: revisar as heurísticas e anotar exemplos")
    col1, col2, col3 = st.columns(3)
    study_date = col1.date_input("Data", value=date.today(), format="DD/MM/YYYY")
    study_time = col2.time_input("Horário", value=time(14, 0), step=900)
    duration = col3.selectbox("Duração", [25, 45, 60, 90, 120], index=2, format_func=lambda x: f"{x} minutos")
    priority = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"], index=1)
    submitted = st.form_submit_button("Adicionar sessão", type="primary", width="stretch")
if submitted:
    try:
        subject_id = next(s["_id"] for s in subjects if s["name"] == subject_name)
        services.sessions.create(
            user_id=user["_id"], subject_id=subject_id, topic=topic, goal=goal,
            study_date=study_date, study_time=study_time, duration=duration, priority=priority,
        )
    except (ValueError, StopIteration) as error:
        st.error(str(error) if isinstance(error, ValueError) else "Selecione uma disciplina válida.")
    else:
        st.success("Sessão adicionada ao seu plano.")
