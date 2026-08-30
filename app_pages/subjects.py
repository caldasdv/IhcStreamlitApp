"""Tela de disciplinas."""

import streamlit as st
from html import escape
import re

from src.ui.context import load_page_context
from src.ui.feedback import show_action_error
from src.ui.sidebar import render_account_sidebar


services, user, subjects = load_page_context()
render_account_sidebar(services, user)

st.caption("ORGANIZAÇÃO")
st.title("Disciplinas")
st.write("Use poucas disciplinas e dê uma cor para reconhecer cada uma rapidamente.")
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
            services.subjects.create(user["_id"], subject_name, color)
        except ValueError as error:
            st.error(str(error))
        except Exception as error:
            show_action_error("adicionar a disciplina", error)
        else:
            st.success("Disciplina adicionada.")
            st.rerun()
