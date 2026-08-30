from __future__ import annotations

from datetime import date, time, timedelta
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.domain.session_rules import (
    effective_status,
)
from src.services.container import get_application_services


PROJECT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_DIR / ".env")


def session_card(row: dict) -> None:
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


st.set_page_config(page_title="Plano", page_icon="◷", layout="wide")

st.markdown(
    """
    <style>
    /* Aparência inspirada em ferramentas de notas, sem alterar os componentes. */
    .stApp { background: #ffffff; color: #37352f; }
    [data-testid="stSidebar"] { background: #f7f6f3; border-right: 1px solid #e9e9e7; }
    [data-testid="stSidebar"] section { padding-top: 1.5rem; }
    .block-container { max-width: 960px; padding-top: 3.5rem; padding-bottom: 5rem; }
    h1, h2, h3 { color: #37352f; font-weight: 650; letter-spacing: -0.02em; }
    h1 { font-size: 2.35rem; margin-bottom: .35rem; }
    h2 { font-size: 1.45rem; }
    h3 { font-size: 1.08rem; }
    [data-testid="stCaptionContainer"] p { color: #9b9a97; letter-spacing: .04em; }
    [data-testid="stVerticalBlockBorderWrapper"] { border-color: #e9e9e7; border-radius: 5px; box-shadow: none; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #787774; }
    .stButton button, .stFormSubmitButton button { border-radius: 4px; box-shadow: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

try:
    services = get_application_services()
    user = services.users.get_active_user()
    subjects = services.subjects.list_for_user(user["_id"])
except Exception as error:
    st.error("Não foi possível conectar ao MongoDB Atlas.")
    st.caption(f"Detalhe técnico: {type(error).__name__}")
    st.stop()

with st.sidebar:
    st.markdown("## Plano")
    st.caption("Seu espaço de estudos")
    page = st.selectbox("Navegação", ["Visão geral", "Nova sessão", "Progresso", "Disciplinas"], label_visibility="collapsed")
    st.divider()
    st.caption("Usuário de teste")
    st.write(user["name"])
    st.caption(user["email"])
    st.divider()
    st.caption("MongoDB Atlas · plano_estudos")
    st.divider()
    st.caption("Meta semanal")
    goal_hours = st.number_input("Horas", min_value=1.0, max_value=80.0, value=user.get("weekly_goal_minutes", 300) / 60, step=0.5, label_visibility="collapsed")
    if st.button("Salvar meta", use_container_width=True):
        services.users.update_weekly_goal(user["_id"], goal_hours)
        st.success("Meta atualizada.")
        st.rerun()

if page == "Visão geral":
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
    st.progress(min(completed_minutes / goal_minutes, 1.0) if goal_minutes else 0.0, text=f"{completed_minutes / goal_minutes * 100:.0f}% da meta semanal" if goal_minutes else "Sem meta")
    st.divider()
    selected_date = st.date_input("Ver dia", value=date.today(), format="DD/MM/YYYY")
    day_sessions = [s for s in all_sessions if s["study_date"] == str(selected_date)]
    weekdays = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
    st.subheader(f"{weekdays[selected_date.weekday()]}, {selected_date.day:02d}/{selected_date.month:02d}")
    if not day_sessions:
        st.info("Nenhuma sessão planejada para este dia.")
    for row in day_sessions:
        session_card(row)
    if day_sessions:
        st.subheader("Atualizar sessão")
        session_labels = {
            f"{item['study_time']} — {item['topic']}": item["_id"]
            for item in day_sessions
        }
        chosen_label = st.selectbox("Escolha uma sessão", list(session_labels))
        chosen_id = session_labels[chosen_label]
        chosen = next(item for item in day_sessions if item["_id"] == chosen_id)
        action_col1, action_col2 = st.columns([1, 1])
        if effective_status(chosen) != "Concluída" and action_col1.button("Marcar como concluída", use_container_width=True):
            services.sessions.complete(chosen["_id"], user["_id"])
            st.rerun()
        if action_col2.button("Excluir sessão", use_container_width=True):
            services.sessions.delete(chosen["_id"], user["_id"])
            st.rerun()

elif page == "Nova sessão":
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
        submitted = st.form_submit_button("Adicionar sessão", type="primary", use_container_width=True)
    if submitted:
        try:
            subject_id = next(s["_id"] for s in subjects if s["name"] == subject_name)
            services.sessions.create(user_id=user["_id"], subject_id=subject_id, topic=topic, goal=goal, study_date=study_date, study_time=study_time, duration=duration, priority=priority)
        except ValueError as error:
            st.error(str(error))
        else:
            st.success("Sessão adicionada ao seu plano.")

elif page == "Progresso":
    st.caption("ACOMPANHAMENTO")
    st.title("Seu progresso")
    st.write("Acompanhe o que foi planejado e concluído em cada disciplina.")
    progress_sessions = services.sessions.list_for_user(user["_id"], subjects)
    if not progress_sessions:
        st.info("Adicione uma sessão para começar a acompanhar seu progresso.")
    for subject in subjects:
        rows = [s for s in progress_sessions if s["subject_id"] == subject["_id"]]
        planned = sum(s["duration"] for s in rows)
        done = sum(s["duration"] for s in rows if effective_status(s) == "Concluída")
        with st.container(border=True):
            st.write(f"**{subject['name']}**")
            st.progress(done / planned if planned else 0, text=f"{done} de {planned} minutos concluídos")
            st.caption(f"{len(rows)} sessões · {len([s for s in rows if effective_status(s) == 'Atrasada'])} atrasadas")

else:
    st.caption("ORGANIZAÇÃO")
    st.title("Disciplinas")
    st.write("Use poucas disciplinas e dê uma cor para reconhecer cada uma rapidamente.")
    for subject in subjects:
        st.markdown(f"`{subject['color']}`  **{subject['name']}**")
    st.divider()
    with st.form("new_subject"):
        subject_name = st.text_input("Nome da nova disciplina")
        color = st.color_picker("Cor", "#5E6AD2")
        if st.form_submit_button("Adicionar disciplina", type="primary"):
            try:
                services.subjects.create(user["_id"], subject_name, color)
                st.success("Disciplina adicionada.")
                st.rerun()
            except ValueError as error:
                st.error(str(error))
