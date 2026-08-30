"""Tela de disciplinas."""

import streamlit as st

from src.ui.context import load_page_context
from src.ui.sidebar import render_account_sidebar


services, user, subjects = load_page_context()
render_account_sidebar(services, user)

st.caption("ORGANIZAÇÃO")
st.title("Disciplinas")
st.write("Use poucas disciplinas e dê uma cor para reconhecer cada uma rapidamente.")
for subject in subjects:
    st.markdown(f"`{subject['color']}`  **{subject['name']}**")
st.divider()
with st.form("new_subject"):
    subject_name = st.text_input("Nome da nova disciplina")
    color = st.color_picker("Cor", "#5E6AD2")
    if st.form_submit_button("Adicionar disciplina", type="primary", width="stretch"):
        try:
            services.subjects.create(user["_id"], subject_name, color)
        except ValueError as error:
            st.error(str(error))
        else:
            st.success("Disciplina adicionada.")
            st.rerun()
