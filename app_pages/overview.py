"""Tela de visão geral."""

from datetime import date, time, timedelta

import streamlit as st

from src.domain.session_rules import effective_status
from src.ui.components.session_card import render_session_card
from src.ui.components.study_rhythm import render_study_rhythm
from src.ui.components.page_header import render_flow_actions, render_page_header
from src.ui.context import (
    load_current_period_subjects,
    load_page_context,
    load_page_sessions,
)
from src.ui.feedback import show_action_error
from src.ui.feedback import set_success_flash
from src.ui.sidebar import render_account_sidebar


services, user, subjects = load_page_context()
render_account_sidebar(services, user)
current_period_id = user.get("current_academic_period_id")

render_page_header(
    "SEMANA DE ESTUDOS",
    f"Olá, {user['name'].split()[0]}",
    "Aqui está o que você planejou para os próximos dias.",
)
render_flow_actions("Hoje")
if current_period_id is None:
    with st.container(border=True):
        st.subheader("Vamos preparar seu plano")
        st.write("Crie um período acadêmico para depois adicionar disciplinas e sessões de estudo.")
        if st.button(
            "Criar período acadêmico",
            type="primary",
            icon=":material/date_range:",
        ):
            st.switch_page("app_pages/academic_periods.py")
    st.stop()

current_subjects = load_current_period_subjects(
    services, user, retry_key="retry_overview_subjects"
)
if not current_subjects:
    with st.container(border=True):
        st.subheader("Seu período está pronto")
        st.write("Adicione sua primeira disciplina para começar a planejar sessões de estudo.")
        if st.button(
            "Adicionar disciplina",
            type="primary",
            icon=":material/menu_book:",
        ):
            st.switch_page("app_pages/subjects.py")
    st.stop()

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
st.markdown(
    f"""
    <section class="plan-overview-hero" aria-label="Resumo da semana">
        <div class="plan-overview-hero-copy">
            <span class="plan-overview-hero-kicker">SEU RITMO, SUA SEMANA</span>
            <h2>Pequenos blocos.<br><em>Um semestre inteiro.</em></h2>
            <p>Você já tem um mapa. Agora é só escolher o próximo passo.</p>
        </div>
        <div class="plan-overview-orbit plan-overview-orbit-a"></div>
        <div class="plan-overview-orbit plan-overview-orbit-b"></div>
        <div class="plan-overview-hero-stat">
            <span>pulso da semana</span>
            <strong>{completed_minutes}<small> min</small></strong>
            <div class="plan-overview-hero-track"><i style="width:{min(completed_minutes / goal_minutes * 100, 100) if goal_minutes else 0:.0f}%"></i></div>
            <small>{len(completed)} sessões concluídas</small>
        </div>
        <div class="plan-overview-spark spark-one"></div><div class="plan-overview-spark spark-two"></div><div class="plan-overview-spark spark-three"></div>
    </section>
    """,
    unsafe_allow_html=True,
)
render_study_rhythm(week_sessions, week_start)
st.markdown(
    '<section class="plan-quick-actions" aria-label="Ações rápidas">'
    '<span>O que você quer fazer agora?</span></section>',
    unsafe_allow_html=True,
)
quick_columns = st.columns(3)
if quick_columns[0].button("Começar uma sessão", icon=":material/play_arrow:", width="stretch", key="overview_quick_session"):
    st.switch_page("app_pages/new_session.py")
if quick_columns[1].button("Revisar a semana", icon=":material/calendar_view_week:", width="stretch", key="overview_quick_week"):
    st.switch_page("app_pages/weekly.py")
if quick_columns[2].button("Organizar conteúdos", icon=":material/account_tree:", width="stretch", key="overview_quick_topics"):
    st.switch_page("app_pages/topics.py")
if pending:
    next_session = min(pending, key=lambda session: (session["study_date"], session["study_time"]))
    next_session_date = date.fromisoformat(next_session["study_date"])
    with st.container(border=True):
        st.caption("PRÓXIMO PASSO")
        st.subheader(next_session["topic"])
        st.write(
            f"{next_session['subject_name']} · {next_session_date:%d/%m/%Y} às "
            f"{next_session['study_time']} · {next_session['duration']} minutos"
        )
        if st.button("Abrir semana", icon=":material/calendar_view_week:", key="overview_open_week"):
            st.switch_page("app_pages/weekly.py")
else:
    st.success("Tudo em dia por aqui. Você pode planejar a próxima sessão.")
st.markdown('<div class="plan-overview-divider"></div>', unsafe_allow_html=True)
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
st.markdown(
    f'<h2 class="plan-overview-day-title">{weekdays[selected_date.weekday()]}, '
    f'{selected_date.day:02d}/{selected_date.month:02d}</h2>',
    unsafe_allow_html=True,
)
if not day_sessions:
    st.info("Nenhuma sessão planejada para este dia.")
for row in day_sessions:
    action = render_session_card(row, key=f"overview_session_{row['_id']}")
    if action == "complete":
        try:
            services.sessions.complete(row["_id"], user["_id"])
        except Exception as error:
            show_action_error("concluir a sessão", error)
        else:
            set_success_flash("Sessão concluída.")
            st.rerun()
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
    if st.button("Excluir sessão", width="stretch"):
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

    if not current_subjects:
        st.info("Cadastre uma disciplina no período atual para editar ou reagendar esta sessão.")
    else:
        with st.expander("Editar ou reagendar sessão"):
            subjects_by_id = {subject["_id"]: subject for subject in current_subjects}
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
                topics_service = getattr(services, "topics", None)
                edit_topics = (
                    topics_service.list_for_subject(
                        user["_id"], current_period_id, edit_subject_id
                    )
                    if topics_service is not None
                    else []
                )
                edit_topics_by_id = {topic["_id"]: topic for topic in edit_topics}
                topic_options = [None, *edit_topics_by_id]
                current_topic_id = chosen.get("topic_id")
                if current_topic_id not in topic_options:
                    current_topic_id = None
                edit_topic_id = st.selectbox(
                    "Conteúdo relacionado (opcional)",
                    topic_options,
                    index=topic_options.index(current_topic_id),
                    format_func=lambda value: "Sem conteúdo específico" if value is None else edit_topics_by_id[value]["title"],
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
                        academic_period_id=current_period_id,
                        subject_id=edit_subject_id,
                        topic=edit_topic,
                        goal=edit_goal,
                        study_date=edit_date,
                        study_time=edit_time,
                        duration=edit_duration,
                        priority=edit_priority,
                        topic_id=edit_topic_id,
                    )
                except ValueError as error:
                    st.error(str(error))
                except Exception as error:
                    show_action_error("salvar as alterações", error)
                else:
                    set_success_flash("Sessão atualizada.")
                    st.rerun()
