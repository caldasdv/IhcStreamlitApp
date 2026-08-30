"""Tela da grade semanal de aulas."""

from datetime import time

import streamlit as st

from src.ui.components.page_header import render_page_header
from src.ui.context import load_current_period_subjects, load_page_context
from src.ui.feedback import set_success_flash, show_action_error
from src.ui.sidebar import render_account_sidebar


WEEKDAYS = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
    "Domingo",
]

services, user, _all_subjects = load_page_context()
render_account_sidebar(services, user)
render_page_header(
    "ORGANIZAÇÃO ACADÊMICA",
    "Grade de aulas",
    "Cadastre os horários recorrentes das disciplinas do período atual.",
)

current_period_id = user.get("current_academic_period_id")
subjects = load_current_period_subjects(
    services, user, retry_key="retry_class_schedule_subjects"
)

if current_period_id is None:
    st.info("Defina um período acadêmico atual antes de montar sua grade.")
    if st.button("Gerenciar períodos acadêmicos", icon=":material/date_range:"):
        st.switch_page("app_pages/academic_periods.py")
    st.stop()

if not subjects:
    st.info("Cadastre ao menos uma disciplina no período atual antes de adicionar aulas.")
    if st.button("Gerenciar disciplinas", icon=":material/menu_book:"):
        st.switch_page("app_pages/subjects.py")
    st.stop()

try:
    meetings = services.class_meetings.list_for_period(
        user["_id"], current_period_id, subjects
    )
except Exception as error:
    show_action_error("carregar sua grade de aulas", error)
    if st.button("Tentar novamente", key="retry_class_schedule"):
        st.rerun()
    st.stop()

st.subheader("Adicionar aula recorrente")
subjects_by_id = {subject["_id"]: subject for subject in subjects}
with st.form("new_class_meeting"):
    subject_id = st.selectbox(
        "Disciplina",
        list(subjects_by_id),
        format_func=lambda value: subjects_by_id[value]["name"],
        key="class_schedule_subject",
    )
    weekday_name = st.selectbox("Dia da semana", WEEKDAYS, key="class_schedule_weekday")
    time_columns = st.columns(2)
    start_time = time_columns[0].time_input(
        "Início", value=time(8, 0), step=900, key="class_schedule_start"
    )
    end_time = time_columns[1].time_input(
        "Fim", value=time(9, 30), step=900, key="class_schedule_end"
    )
    location = st.text_input(
        "Local (opcional)", placeholder="Ex.: Bloco B, sala 204"
    )
    submitted = st.form_submit_button(
        "Adicionar à grade", type="primary", width="stretch"
    )

if submitted:
    try:
        services.class_meetings.create(
            user_id=user["_id"],
            academic_period_id=current_period_id,
            subject_id=subject_id,
            weekday=WEEKDAYS.index(weekday_name),
            start_time=start_time,
            end_time=end_time,
            location=location,
        )
    except ValueError as error:
        st.error(str(error))
    except Exception as error:
        show_action_error("adicionar a aula", error)
    else:
        set_success_flash("Aula adicionada à grade semanal.")
        st.rerun()

st.divider()
st.subheader("Sua semana")
if not meetings:
    st.info("Sua grade ainda está vazia. Adicione o primeiro horário acima.")

for weekday, weekday_name in enumerate(WEEKDAYS):
    day_meetings = [meeting for meeting in meetings if meeting["weekday"] == weekday]
    if not day_meetings:
        continue
    st.write(f"**{weekday_name}**")
    for meeting in day_meetings:
        with st.container(border=True):
            st.write(
                f"**{meeting['start_time']}–{meeting['end_time']} · "
                f"{meeting['subject_name']}**"
            )
            if meeting.get("location"):
                st.caption(f"Local: {meeting['location']}")
            confirm_key = f"confirm_delete_class_{meeting['_id']}"
            if st.button(
                "Remover",
                key=f"delete_class_{meeting['_id']}",
                icon=":material/delete:",
            ):
                st.session_state[confirm_key] = True
                st.rerun()
            if st.session_state.get(confirm_key):
                st.warning("Remover este horário da grade?")
                with st.container(horizontal=True):
                    if st.button(
                        "Confirmar remoção",
                        key=f"confirm_class_{meeting['_id']}",
                        type="primary",
                    ):
                        try:
                            services.class_meetings.delete(
                                user["_id"], current_period_id, meeting["_id"]
                            )
                        except Exception as error:
                            show_action_error("remover a aula", error)
                        else:
                            st.session_state.pop(confirm_key, None)
                            set_success_flash("Horário removido da grade.")
                            st.rerun()
                    if st.button(
                        "Cancelar", key=f"cancel_class_{meeting['_id']}"
                    ):
                        st.session_state.pop(confirm_key, None)
                        st.rerun()
