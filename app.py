from __future__ import annotations

import os
import sqlite3
from datetime import date, datetime, time, timedelta
from pathlib import Path

import streamlit as st


APP_DIR = Path(__file__).parent
DRIVE_DB = Path("/content/drive/MyDrive/IhcStreamlitApp/estudos.db")
LOCAL_DB = APP_DIR / "estudos.db"
DB_PATH = Path(os.getenv("STUDY_DB_PATH", DRIVE_DB if DRIVE_DB.parent.exists() else LOCAL_DB))


def connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def setup_database() -> None:
    with connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                color TEXT NOT NULL DEFAULT '#5E6AD2'
            );

            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
                topic TEXT NOT NULL,
                study_date TEXT NOT NULL,
                study_time TEXT NOT NULL,
                duration INTEGER NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pendente',
                goal TEXT NOT NULL DEFAULT ''
            );
            """
        )
        user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
        if user:
            return

        user_id = conn.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            ("Marina Oliveira", "marina.teste@exemplo.com"),
        ).lastrowid
        subjects = [
            (user_id, "Interação Humano-Computador", "#5E6AD2"),
            (user_id, "Banco de Dados", "#2E8B72"),
            (user_id, "Programação Web", "#C47F17"),
        ]
        conn.executemany(
            "INSERT INTO subjects (user_id, name, color) VALUES (?, ?, ?)", subjects
        )
        subject_ids = {
            row["name"]: row["id"]
            for row in conn.execute("SELECT id, name FROM subjects WHERE user_id = ?", (user_id,))
        }
        today = date.today()
        sessions = [
            (user_id, subject_ids["Interação Humano-Computador"], "Heurísticas de Nielsen", str(today), "14:00", 60, "Alta", "Revisar as 10 heurísticas e fazer anotações.", "Pendente"),
            (user_id, subject_ids["Banco de Dados"], "Relacionamentos e chaves", str(today + timedelta(days=1)), "16:30", 45, "Média", "Resolver cinco exercícios do material.", "Pendente"),
            (user_id, subject_ids["Programação Web"], "Revisão de formulários", str(today - timedelta(days=1)), "19:00", 50, "Baixa", "Praticar validação de campos.", "Concluída"),
        ]
        conn.executemany(
            """INSERT INTO study_sessions
            (user_id, subject_id, topic, study_date, study_time, duration, priority, goal, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            sessions,
        )


def query(sql: str, params: tuple = ()) -> list[sqlite3.Row]:
    with connection() as conn:
        return conn.execute(sql, params).fetchall()


def execute(sql: str, params: tuple = ()) -> None:
    with connection() as conn:
        conn.execute(sql, params)


def session_card(row: sqlite3.Row) -> None:
    with st.container(border=True):
        info_col, status_col = st.columns([5, 1])
        info_col.caption(f"{row['study_time']} · {row['duration']} minutos")
        info_col.write(f"**{row['subject_name']}**")
        info_col.subheader(row["topic"])
        if row["goal"]:
            info_col.write(row["goal"])
        if row["status"] == "Concluída":
            status_col.success("Concluída")
        else:
            status_col.warning("Pendente")


st.set_page_config(page_title="Plano", page_icon="◷", layout="wide")
setup_database()

user = query("SELECT * FROM users LIMIT 1")[0]
subjects = query("SELECT * FROM subjects WHERE user_id = ? ORDER BY name", (user["id"],))

with st.sidebar:
    st.markdown("### Plano")
    st.caption("Planejador de estudos")
    page = st.radio("Navegação", ["Visão geral", "Nova sessão", "Disciplinas"], label_visibility="collapsed")
    st.divider()
    st.caption("Usuário de teste")
    st.write(user["name"])
    st.caption(user["email"])
    st.divider()
    st.caption(f"Banco: `{DB_PATH.name}`")

if page == "Visão geral":
    st.caption("SEMANA DE ESTUDOS")
    st.title(f"Olá, {user['name'].split()[0]}")
    st.write("Aqui está o que você planejou para os próximos dias.")
    all_sessions = query(
        """SELECT s.*, subjects.name AS subject_name FROM study_sessions s
        JOIN subjects ON subjects.id = s.subject_id WHERE s.user_id = ?
        ORDER BY s.study_date, s.study_time""", (user["id"],)
    )
    pending = [s for s in all_sessions if s["status"] == "Pendente"]
    completed = [s for s in all_sessions if s["status"] == "Concluída"]
    col1, col2, col3 = st.columns(3)
    col1.write("**Sessões pendentes**")
    col1.title(len(pending))
    col2.write("**Horas planejadas**")
    col2.title(f"{sum(s['duration'] for s in pending) / 60:.1f}h")
    col3.write("**Concluídas**")
    col3.title(len(completed))
    st.divider()
    selected_date = st.date_input("Ver dia", value=date.today(), format="DD/MM/YYYY")
    day_sessions = [s for s in all_sessions if s["study_date"] == str(selected_date)]
    st.subheader(selected_date.strftime("%A, %d de %B").capitalize())
    if not day_sessions:
        st.info("Nenhuma sessão planejada para este dia.")
    for row in day_sessions:
        session_card(row)
    if day_sessions:
        st.subheader("Atualizar sessão")
        # Use apenas strings no selectbox. sqlite3.Row não pode ser serializado
        # pelo estado do Streamlit entre os reruns do aplicativo.
        session_labels = {
            f"{item['study_time']} — {item['topic']}": item["id"]
            for item in day_sessions
        }
        chosen_label = st.selectbox("Escolha uma sessão", list(session_labels))
        chosen_id = session_labels[chosen_label]
        chosen = next(item for item in day_sessions if item["id"] == chosen_id)
        action_col1, action_col2 = st.columns([1, 1])
        if chosen["status"] == "Pendente" and action_col1.button("Marcar como concluída", use_container_width=True):
            execute("UPDATE study_sessions SET status = 'Concluída' WHERE id = ?", (chosen["id"],))
            st.rerun()
        if action_col2.button("Excluir sessão", use_container_width=True):
            execute("DELETE FROM study_sessions WHERE id = ?", (chosen["id"],))
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
        priority = st.radio("Prioridade", ["Baixa", "Média", "Alta"], horizontal=True, index=1)
        submitted = st.form_submit_button("Adicionar sessão", type="primary", use_container_width=True)
    if submitted:
        if not topic.strip():
            st.error("Informe o assunto da sessão.")
        else:
            subject_id = next(s["id"] for s in subjects if s["name"] == subject_name)
            execute(
                """INSERT INTO study_sessions
                (user_id, subject_id, topic, study_date, study_time, duration, priority, goal)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (user["id"], subject_id, topic.strip(), str(study_date), study_time.strftime("%H:%M"), duration, priority, goal.strip()),
            )
            st.success("Sessão adicionada ao seu plano.")

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
                execute("INSERT INTO subjects (user_id, name, color) VALUES (?, ?, ?)", (user["id"], subject_name.strip(), color))
                st.success("Disciplina adicionada.")
                st.rerun()
            st.error("Informe o nome da disciplina.")
