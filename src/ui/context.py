"""Contexto compartilhado das páginas Streamlit."""

from __future__ import annotations

import streamlit as st

from src.services.container import ApplicationServices, get_application_services
from src.ui.feedback import logger
from src.ui.feedback import show_action_error


def load_page_context() -> tuple[ApplicationServices, dict, list[dict]]:
    """Carrega dependências da página com feedback visível ao usuário."""
    try:
        with st.spinner("Conectando ao seu plano de estudos..."):
            services = get_application_services()
            user = services.users.get_active_user()
            subjects = services.subjects.list_for_user(user["_id"])
    except Exception:
        logger.exception("Falha ao carregar o contexto da página")
        st.error("Não foi possível carregar esta tela.")
        st.caption("Verifique sua conexão e tente novamente. Seus dados não foram alterados.")
        st.stop()
    return services, user, subjects


def load_page_sessions(
    services: ApplicationServices, user: dict, subjects: list[dict]
) -> list[dict]:
    """Carrega sessões com o mesmo tratamento de falha usado no contexto inicial."""
    try:
        return services.sessions.list_for_user(user["_id"], subjects)
    except Exception as error:
        show_action_error("carregar suas sessões", error)
        st.stop()
        return []
