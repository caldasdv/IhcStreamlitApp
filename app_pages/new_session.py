"""Tela de criação de sessão."""

from datetime import date, time

import streamlit as st

from src.ui.context import load_current_period_subjects, load_page_context
from src.ui.components.page_header import render_page_header
from src.ui.feedback import set_success_flash, show_action_error
from src.ui.sidebar import render_account_sidebar


services, user, subjects = load_page_context()
render_account_sidebar(services, user)

current_period_id = user.get("current_academic_period_id")
current_subjects = load_current_period_subjects(
    services, user, retry_key="retry_new_session_subjects"
)

if current_period_id is None:
    st.info("Defina um período acadêmico atual antes de criar uma sessão.")
    st.stop()
if not current_subjects:
    st.info("Cadastre uma disciplina no período atual antes de criar uma sessão.")
    st.stop()

render_page_header("PLANEJAMENTO", "Nova sessão", "Defina uma sessão pequena e objetiva para facilitar o início do estudo.")
with st.form("new_session"):
    subjects_by_id = {subject["_id"]: subject for subject in current_subjects}
    subject_id = st.selectbox(
        "Disciplina",
        list(subjects_by_id),
        format_func=lambda value: subjects_by_id[value]["name"],
    )
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
        services.sessions.create(
            user_id=user["_id"], subject_id=subject_id, topic=topic, goal=goal,
            academic_period_id=current_period_id,
            study_date=study_date, study_time=study_time, duration=duration, priority=priority,
        )
    except ValueError as error:
        st.error(str(error))
    except Exception as error:
        show_action_error("adicionar a sessão", error)
    else:
        set_success_flash("Sessão adicionada ao seu plano.")
        st.switch_page("app_pages/overview.py")
