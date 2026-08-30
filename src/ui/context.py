"""Contexto compartilhado das páginas Streamlit."""

from __future__ import annotations

import streamlit as st

from src.services.container import ApplicationServices, get_application_services


def load_page_context() -> tuple[ApplicationServices, dict, list[dict]]:
    """Carrega dependências da página com feedback visível ao usuário."""
    try:
        with st.spinner("Conectando ao seu plano de estudos..."):
            services = get_application_services()
            user = services.users.get_active_user()
            subjects = services.subjects.list_for_user(user["_id"])
    except Exception as error:
        st.error("Não foi possível carregar esta tela.")
        st.caption(f"Detalhe técnico: {type(error).__name__}")
        st.stop()
    return services, user, subjects
