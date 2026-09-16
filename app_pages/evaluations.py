"""Tela de avaliações, notas e exercícios."""

from datetime import date

import streamlit as st

from src.domain.evaluation_rules import EVALUATION_TYPES
from src.ui.components.page_header import render_flow_actions, render_page_header
from src.ui.context import load_current_period_subjects, load_page_context
from src.ui.feedback import set_success_flash, show_action_error
from src.ui.sidebar import render_account_sidebar


services, user, _subjects = load_page_context()
render_account_sidebar(services, user)
render_page_header("ACOMPANHAR", "Avaliações", "Registre provas, trabalhos e exercícios para acompanhar suas notas.")
render_flow_actions("Avaliações")

period_id = user.get("current_academic_period_id")
subjects = load_current_period_subjects(services, user, retry_key="retry_evaluations_subjects")
if period_id is None:
    st.info("Defina um período acadêmico atual antes de registrar avaliações.")
    st.stop()
if not subjects:
    st.info("Cadastre uma disciplina antes de registrar avaliações.")
    if st.button("Gerenciar disciplinas", icon=":material/menu_book:"):
        st.switch_page("app_pages/subjects.py")
    st.stop()

subjects_by_id = {subject["_id"]: subject for subject in subjects}
try:
    evaluations = services.evaluations.list_for_period(user["_id"], period_id, subjects)
except Exception as error:
    show_action_error("carregar suas avaliações", error)
    st.stop()

graded = [
    item for item in evaluations
    if item.get("score") is not None and item.get("max_score")
]
average = sum(item["score"] / item["max_score"] for item in graded) / len(graded) * 10 if graded else 0
metric_cols = st.columns(3)
metric_cols[0].metric("Avaliações", len(evaluations), border=True)
metric_cols[1].metric("Registradas", len(graded), border=True)
metric_cols[2].metric("Média proporcional", f"{average:.1f}/10" if graded else "—", border=True)

if evaluations:
    st.subheader("Seu histórico")
    for item in evaluations:
        with st.container(border=True):
            heading, detail = st.columns([2, 1])
            heading.markdown(f"### {item['title']}")
            heading.caption(f"{item['type']} · {item['subject_name']}")
            if item.get("score") is None or not item.get("max_score"):
                detail.metric("Nota", "Pendente")
                st.caption(f"{item['evaluation_date']} · nota ainda não registrada")
            else:
                percentage = item["score"] / item["max_score"] * 100
                detail.metric("Nota", f"{item['score']:g}/{item['max_score']:g}")
                st.progress(min(percentage / 100, 1.0), text=f"{item['evaluation_date']} · {percentage:.0f}%")
    if len(graded) > 1:
        st.subheader("Evolução das notas")
        chart_data = {
            item["evaluation_date"]: round(item["score"] / item["max_score"] * 10, 2)
            for item in graded
        }
        st.line_chart(chart_data, height=260)
else:
    st.info("Você ainda não registrou avaliações. Adicione a primeira para acompanhar sua evolução.")

with st.expander("Adicionar avaliação", expanded=not evaluations):
    with st.form("new_evaluation"):
        subject_id = st.selectbox("Disciplina", list(subjects_by_id), format_func=lambda value: subjects_by_id[value]["name"])
        title = st.text_input("Nome", placeholder="Ex.: Prova de consultas SQL")
        evaluation_type = st.selectbox("Tipo", EVALUATION_TYPES)
        form_cols = st.columns(3)
        evaluation_date = form_cols[0].date_input("Data", value=date.today(), format="DD/MM/YYYY")
        score = form_cols[1].number_input("Nota obtida", min_value=0.0, value=0.0, step=0.5)
        max_score = form_cols[2].number_input("Nota máxima", min_value=0.5, value=10.0, step=0.5)
        submitted = st.form_submit_button("Salvar avaliação", type="primary", width="stretch")
    if submitted:
        try:
            services.evaluations.create(
                user_id=user["_id"], academic_period_id=period_id, subject_id=subject_id,
                title=title, evaluation_type=evaluation_type, evaluation_date=evaluation_date,
                score=score, max_score=max_score,
            )
        except ValueError as error:
            st.error(str(error))
        except Exception as error:
            show_action_error("salvar a avaliação", error)
        else:
            set_success_flash("Avaliação registrada.")
            st.rerun()
