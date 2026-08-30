from __future__ import annotations

import os
from datetime import date, time, timedelta
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi


APP_DIR = Path(__file__).parent
load_dotenv(APP_DIR / ".env")


@st.cache_resource
def get_database():
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise RuntimeError("MONGODB_URI não foi encontrada no arquivo .env.")
    client = MongoClient(uri, server_api=ServerApi("1"), serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    return client["plano_estudos"]


def seed_database(db) -> None:
    if db.users.find_one({}):
        return
    user_id = db.users.insert_one({"name": "Marina Oliveira", "email": "marina.teste@exemplo.com", "weekly_goal_minutes": 300}).inserted_id
    subjects = [
        {"user_id": user_id, "name": "Interação Humano-Computador", "color": "#5E6AD2"},
        {"user_id": user_id, "name": "Banco de Dados", "color": "#2E8B72"},
        {"user_id": user_id, "name": "Programação Web", "color": "#C47F17"},
    ]
    subject_ids = [db.subjects.insert_one(subject).inserted_id for subject in subjects]
    today = date.today()
    db.study_sessions.insert_many([
        {"user_id": user_id, "subject_id": subject_ids[0], "topic": "Heurísticas de Nielsen", "study_date": today.isoformat(), "study_time": "14:00", "duration": 60, "priority": "Alta", "status": "Pendente", "goal": "Revisar as 10 heurísticas e fazer anotações."},
        {"user_id": user_id, "subject_id": subject_ids[1], "topic": "Relacionamentos e chaves", "study_date": (today + timedelta(days=1)).isoformat(), "study_time": "16:30", "duration": 45, "priority": "Média", "status": "Pendente", "goal": "Resolver cinco exercícios do material."},
        {"user_id": user_id, "subject_id": subject_ids[2], "topic": "Revisão de formulários", "study_date": (today - timedelta(days=1)).isoformat(), "study_time": "19:00", "duration": 50, "priority": "Baixa", "status": "Concluída", "goal": "Praticar validação de campos."},
    ])


def effective_status(row: dict) -> str:
    if row["status"] == "Pendente" and row["study_date"] < date.today().isoformat():
        return "Atrasada"
    return row["status"]


def minutes_at(value: str) -> int:
    hours, minutes = (int(part) for part in value.split(":"))
    return hours * 60 + minutes


def has_conflict(db, user_id, study_date: date, study_time: time, duration: int) -> bool:
    start = study_time.hour * 60 + study_time.minute
    end = start + duration
    existing = db.study_sessions.find({"user_id": user_id, "study_date": study_date.isoformat(), "status": "Pendente"}, {"study_time": 1, "duration": 1})
    return any(
        start < minutes_at(item["study_time"]) + item["duration"]
        and minutes_at(item["study_time"]) < end
        for item in existing
    )


def load_sessions(db, user_id) -> list[dict]:
    subjects_by_id = {subject["_id"]: subject for subject in db.subjects.find({"user_id": user_id})}
    sessions = list(db.study_sessions.find({"user_id": user_id}).sort([("study_date", 1), ("study_time", 1)]))
    for session in sessions:
        subject = subjects_by_id.get(session["subject_id"], {"name": "Sem disciplina", "color": "#787774"})
        session["subject_name"] = subject["name"]
        session["subject_color"] = subject["color"]
    return sessions


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
    db = get_database()
    seed_database(db)
except Exception as error:
    st.error("Não foi possível conectar ao MongoDB Atlas.")
    st.code(str(error))
    st.stop()

user = db.users.find_one({})
subjects = list(db.subjects.find({"user_id": user["_id"]}).sort("name", 1))

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
        db.users.update_one({"_id": user["_id"]}, {"$set": {"weekly_goal_minutes": round(goal_hours * 60)}})
        st.success("Meta atualizada.")
        st.rerun()

if page == "Visão geral":
    st.caption("SEMANA DE ESTUDOS")
    st.title(f"Olá, {user['name'].split()[0]}")
    st.write("Aqui está o que você planejou para os próximos dias.")
    all_sessions = load_sessions(db, user["_id"])
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
            db.study_sessions.update_one({"_id": chosen["_id"]}, {"$set": {"status": "Concluída"}})
            st.rerun()
        if action_col2.button("Excluir sessão", use_container_width=True):
            db.study_sessions.delete_one({"_id": chosen["_id"]})
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
        if not topic.strip():
            st.error("Informe o assunto da sessão.")
        elif study_date < date.today():
            st.error("Escolha hoje ou uma data futura para planejar uma sessão.")
        elif has_conflict(db, user["_id"], study_date, study_time, duration):
            st.error("Esse horário conflita com outra sessão pendente.")
        else:
            subject_id = next(s["_id"] for s in subjects if s["name"] == subject_name)
            db.study_sessions.insert_one({"user_id": user["_id"], "subject_id": subject_id, "topic": topic.strip(), "study_date": study_date.isoformat(), "study_time": study_time.strftime("%H:%M"), "duration": duration, "priority": priority, "status": "Pendente", "goal": goal.strip()})
            st.success("Sessão adicionada ao seu plano.")

elif page == "Progresso":
    st.caption("ACOMPANHAMENTO")
    st.title("Seu progresso")
    st.write("Acompanhe o que foi planejado e concluído em cada disciplina.")
    progress_sessions = load_sessions(db, user["_id"])
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
            if subject_name.strip():
                db.subjects.insert_one({"user_id": user["_id"], "name": subject_name.strip(), "color": color})
                st.success("Disciplina adicionada.")
                st.rerun()
            st.error("Informe o nome da disciplina.")
