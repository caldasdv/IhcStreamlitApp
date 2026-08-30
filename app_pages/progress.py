"""Tela de progresso."""

import streamlit as st

from src.domain.session_rules import effective_status
from src.ui.context import load_page_context
from src.ui.sidebar import render_account_sidebar


services, user, subjects = load_page_context()
render_account_sidebar(services, user)

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
