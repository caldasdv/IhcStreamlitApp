"""Tela de disciplinas."""

from html import escape
import re

import streamlit as st

from src.ui.context import (
    load_current_period_subjects,
    load_legacy_subjects,
    load_page_context,
)
from src.ui.components.page_header import render_page_header
from src.ui.feedback import set_success_flash, show_action_error
from src.ui.sidebar import render_account_sidebar


services, user, _all_subjects = load_page_context()
render_account_sidebar(services, user)

current_period_id = user.get("current_academic_period_id")
subjects = load_current_period_subjects(
    services, user, retry_key="retry_current_period_subjects"
)
legacy_subjects = load_legacy_subjects(
    services, user, retry_key="retry_legacy_subjects"
)

render_page_header(
    "ORGANIZAÇÃO",
    "Disciplinas",
    "Organize as disciplinas do período atual e use cores para reconhecê-las rapidamente.",
)
if current_period_id is None:
    st.info("Defina um período acadêmico atual antes de adicionar disciplinas.")
    if st.button("Gerenciar períodos acadêmicos", icon=":material/date_range:"):
        st.switch_page("app_pages/academic_periods.py")
    if legacy_subjects:
        st.subheader("Disciplinas sem período")
        st.caption(
            "Estes registros antigos foram preservados e não serão associados automaticamente."
        )
        for subject in legacy_subjects:
            st.write(f"- {subject['name']}")
    st.stop()

if not subjects:
    st.info("Nenhuma disciplina cadastrada no período atual. Adicione a primeira abaixo.")
for subject in subjects:
    color = subject.get("color", "#787774")
    safe_color = color if re.fullmatch(r"#[0-9A-Fa-f]{6}", color) else "#787774"
    st.markdown(
        f'<span style="display:inline-block;width:0.8rem;height:0.8rem;'
        f'background:{safe_color};border-radius:50%;margin-right:0.45rem;" '
        f'aria-label="Cor {escape(safe_color)}"></span> **{escape(subject["name"])}** '
        f'<span style="color:#5f5e5b">({escape(safe_color)})</span>',
        unsafe_allow_html=True,
    )
st.divider()
with st.form("new_subject"):
    subject_name = st.text_input("Nome da nova disciplina")
    color = st.color_picker("Cor", "#5E6AD2")
    if st.form_submit_button("Adicionar disciplina", type="primary", width="stretch"):
        try:
            services.subjects.create(
                user["_id"], current_period_id, subject_name, color
            )
        except ValueError as error:
            st.error(str(error))
        except Exception as error:
            show_action_error("adicionar a disciplina", error)
        else:
            set_success_flash("Disciplina adicionada.")
            st.rerun()

if legacy_subjects:
    st.divider()
    st.subheader("Disciplinas sem período")
    st.caption(
        "Estes registros antigos continuam preservados e identificando sessões existentes. "
        "Eles não foram associados automaticamente para evitar colocá-los no semestre errado."
    )
    for subject in legacy_subjects:
        st.write(f"- {subject['name']}")
