"""Tela de visão geral."""

from datetime import date, time, timedelta

import streamlit as st

from src.domain.session_rules import effective_status
from src.ui.components.session_card import render_session_card
from src.ui.components.page_header import render_page_header
from src.ui.context import load_page_context, load_page_sessions
from src.ui.feedback import show_action_error
from src.ui.feedback import set_success_flash
from src.ui.sidebar import render_account_sidebar


services, user, subjects = load_page_context()
render_account_sidebar(services, user)

render_page_header(
    "SEMANA DE ESTUDOS",
    f"Olá, {user['name'].split()[0]}",
    "Aqui está o que você planejou para os próximos dias.",
)
week_start = date.today() - timedelta(days=date.today().weekday())
week_end = week_start + timedelta(days=6)
selected_date = st.date_input("Ver dia", value=date.today(), format="DD/MM/YYYY", key="overview_date")
week_sessions = load_page_sessions(
    services,
    user,
    subjects,
    start_date=week_start,
    end_date=week_end,
    retry_key="retry_overview_week",
)
pending = [s for s in week_sessions if effective_status(s) in ("Pendente", "Atrasada")]
completed = [s for s in week_sessions if effective_status(s) == "Concluída"]
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
if week_start <= selected_date <= week_end:
    day_sessions = [s for s in week_sessions if s["study_date"] == selected_date.isoformat()]
else:
    day_sessions = load_page_sessions(
        services,
        user,
        subjects,
        start_date=selected_date,
        end_date=selected_date,
        retry_key="retry_overview_day",
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
st.subheader(f"{weekdays[selected_date.weekday()]}, {selected_date.day:02d}/{selected_date.month:02d}")
if not day_sessions:
    st.info("Nenhuma sessão planejada para este dia.")
for row in day_sessions:
    render_session_card(row)
if day_sessions:
    st.subheader("Atualizar sessão")
    sessions_by_id = {item["_id"]: item for item in day_sessions}
    chosen_id = st.selectbox(
        "Escolha uma sessão",
        list(sessions_by_id),
        format_func=lambda value: (
            f"{sessions_by_id[value]['study_time']} — {sessions_by_id[value]['topic']}"
        ),
        key="overview_session",
    )
    chosen = next(item for item in day_sessions if item["_id"] == chosen_id)
    action_col1, action_col2 = st.columns([1, 1])
    if effective_status(chosen) != "Concluída" and action_col1.button("Marcar como concluída", width="stretch"):
        try:
            services.sessions.complete(chosen["_id"], user["_id"])
        except Exception as error:
            show_action_error("concluir a sessão", error)
        else:
            set_success_flash("Sessão concluída.")
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
                    set_success_flash("Sessão excluída.")
                    st.rerun()
            if cancel_col.button("Cancelar", width="stretch"):
                st.session_state["confirm_delete_session_id"] = None
                st.rerun()

    if not subjects:
        st.info("Cadastre uma disciplina para editar ou reagendar esta sessão.")
    else:
        with st.expander("Editar ou reagendar sessão"):
            subjects_by_id = {subject["_id"]: subject for subject in subjects}
            subject_ids = list(subjects_by_id)
            current_subject_id = (
                chosen["subject_id"] if chosen["subject_id"] in subjects_by_id else subject_ids[0]
            )
            with st.form("edit_session"):
                edit_subject_id = st.selectbox(
                    "Disciplina",
                    subject_ids,
                    index=subject_ids.index(current_subject_id),
                    format_func=lambda value: subjects_by_id[value]["name"],
                )
                edit_topic = st.text_input("Assunto", value=chosen["topic"])
                edit_goal = st.text_area("Objetivo", value=chosen.get("goal", ""))
                edit_col1, edit_col2, edit_col3 = st.columns(3)
                edit_date = edit_col1.date_input(
                    "Data",
                    value=date.fromisoformat(chosen["study_date"]),
                    format="DD/MM/YYYY",
                )
                edit_time = edit_col2.time_input(
                    "Horário", value=time.fromisoformat(chosen["study_time"]), step=900
                )
                durations = [25, 45, 60, 90, 120]
                if chosen["duration"] not in durations:
                    durations.append(chosen["duration"])
                    durations.sort()
                edit_duration = edit_col3.selectbox(
                    "Duração",
                    durations,
                    index=durations.index(chosen["duration"]),
                    format_func=lambda x: f"{x} minutos",
                )
                priorities = ["Baixa", "Média", "Alta"]
                if chosen["priority"] not in priorities:
                    priorities.append(chosen["priority"])
                edit_priority = st.selectbox(
                    "Prioridade", priorities, index=priorities.index(chosen["priority"])
                )
                edit_submitted = st.form_submit_button(
                    "Salvar alterações", type="primary", width="stretch"
                )
            if edit_submitted:
                try:
                    services.sessions.update(
                        session_id=chosen["_id"],
                        user_id=user["_id"],
                        subject_id=edit_subject_id,
                        topic=edit_topic,
                        goal=edit_goal,
                        study_date=edit_date,
                        study_time=edit_time,
                        duration=edit_duration,
                        priority=edit_priority,
                    )
                except ValueError as error:
                    st.error(str(error))
                except Exception as error:
                    show_action_error("salvar as alterações", error)
                else:
                    set_success_flash("Sessão atualizada.")
                    st.rerun()
