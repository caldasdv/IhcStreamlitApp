"""Tela de visão geral."""

from datetime import date, time, timedelta

import streamlit as st

from src.domain.session_rules import effective_status
from src.ui.components.session_card import render_session_card
from src.ui.context import load_page_context, load_page_sessions
from src.ui.feedback import show_action_error
from src.ui.sidebar import render_account_sidebar


services, user, subjects = load_page_context()
render_account_sidebar(services, user)

st.caption("SEMANA DE ESTUDOS")
st.title(f"Olá, {user['name'].split()[0]}")
st.write("Aqui está o que você planejou para os próximos dias.")
all_sessions = load_page_sessions(services, user, subjects)
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
        try:
            services.sessions.complete(chosen["_id"], user["_id"])
        except Exception as error:
            show_action_error("concluir a sessão", error)
        else:
            st.success("Sessão concluída.")
            st.rerun()
    if action_col2.button("Excluir sessão", width="stretch"):
        st.session_state["confirm_delete_session_id"] = chosen["_id"]
        st.rerun()

    if st.session_state.get("confirm_delete_session_id") == chosen["_id"]:
        with st.container(border=True):
            st.warning(f"Excluir a sessão **{chosen['topic']}**? Essa ação não pode ser desfeita.")
            confirm_col, cancel_col = st.columns(2)
            if confirm_col.button("Confirmar exclusão", type="primary", width="stretch"):
                try:
                    services.sessions.delete(chosen["_id"], user["_id"])
                except Exception as error:
                    show_action_error("excluir a sessão", error)
                else:
                    st.session_state["confirm_delete_session_id"] = None
                    st.success("Sessão excluída.")
                    st.rerun()
            if cancel_col.button("Cancelar", width="stretch"):
                st.session_state["confirm_delete_session_id"] = None
                st.rerun()

    with st.expander("Editar ou reagendar sessão"):
        with st.form("edit_session"):
            subject_names = [s["name"] for s in subjects]
            current_subject = next((s["name"] for s in subjects if s["_id"] == chosen["subject_id"]), subject_names[0])
            edit_subject_name = st.selectbox("Disciplina", subject_names, index=subject_names.index(current_subject))
            edit_topic = st.text_input("Assunto", value=chosen["topic"])
            edit_goal = st.text_area("Objetivo", value=chosen.get("goal", ""))
            edit_col1, edit_col2, edit_col3 = st.columns(3)
            edit_date = edit_col1.date_input("Data", value=date.fromisoformat(chosen["study_date"]), format="DD/MM/YYYY")
            edit_time = edit_col2.time_input("Horário", value=time.fromisoformat(chosen["study_time"]), step=900)
            edit_duration = edit_col3.selectbox("Duração", [25, 45, 60, 90, 120], index=[25, 45, 60, 90, 120].index(chosen["duration"]), format_func=lambda x: f"{x} minutos")
            edit_priority = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"], index=["Baixa", "Média", "Alta"].index(chosen["priority"]))
            edit_submitted = st.form_submit_button("Salvar alterações", type="primary", width="stretch")
        if edit_submitted:
            try:
                edit_subject_id = next(s["_id"] for s in subjects if s["name"] == edit_subject_name)
                services.sessions.update(
                    session_id=chosen["_id"], user_id=user["_id"], subject_id=edit_subject_id,
                    topic=edit_topic, goal=edit_goal, study_date=edit_date, study_time=edit_time,
                    duration=edit_duration, priority=edit_priority,
                )
            except (ValueError, StopIteration) as error:
                st.error(str(error) if isinstance(error, ValueError) else "Selecione uma disciplina válida.")
            except Exception as error:
                show_action_error("salvar as alterações", error)
            else:
                st.success("Sessão atualizada.")
                st.rerun()
