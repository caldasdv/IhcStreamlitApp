"""Contexto compartilhado das páginas Streamlit."""

from __future__ import annotations

from datetime import date

import streamlit as st

from src.services.container import ApplicationServices, get_application_services
from src.ui.auth import get_current_identity
from src.ui.feedback import logger
from src.ui.feedback import show_action_error


def load_page_context() -> tuple[ApplicationServices, dict, list[dict]]:
    """Carrega dependências da página com feedback visível ao usuário."""
    try:
        with st.spinner("Conectando ao seu plano de estudos..."):
            services = get_application_services()
            user = services.users.get_or_create_authenticated_user(get_current_identity())
            subjects = services.subjects.list_for_user(user["_id"])
    except Exception:
        logger.exception("Falha ao carregar o contexto da página")
        st.error("Não foi possível carregar esta tela.")
        st.caption("Verifique sua conexão e tente novamente. Seus dados não foram alterados.")
        st.stop()
    return services, user, subjects


def load_page_sessions(
    services: ApplicationServices,
    user: dict,
    subjects: list[dict],
    *,
    start_date: date | None = None,
    end_date: date | None = None,
    retry_key: str = "retry_sessions_loading",
) -> list[dict]:
    """Carrega sessões com o mesmo tratamento de falha usado no contexto inicial."""
    try:
        return services.sessions.list_for_user(
            user["_id"], subjects, start_date=start_date, end_date=end_date
        )
    except Exception as error:
        show_action_error("carregar suas sessões", error)
        if st.button("Tentar novamente", key=retry_key):
            st.rerun()
        st.stop()
        return []


def load_current_period_subjects(
    services: ApplicationServices,
    user: dict,
    *,
    retry_key: str,
) -> list[dict]:
    """Carrega disciplinas do período atual sem deixar uma falha apagar a página."""
    try:
        return services.subjects.list_for_period(
            user["_id"], user.get("current_academic_period_id")
        )
    except Exception as error:
        show_action_error("carregar as disciplinas do período atual", error)
        if st.button("Tentar novamente", key=retry_key):
            st.rerun()
        st.stop()
        return []


def load_legacy_subjects(
    services: ApplicationServices,
    user: dict,
    *,
    retry_key: str,
) -> list[dict]:
    """Carrega registros sem período de forma explícita e recuperável."""
    try:
        return services.subjects.list_without_period(user["_id"])
    except Exception as error:
        show_action_error("carregar as disciplinas sem período", error)
        if st.button("Tentar novamente", key=retry_key):
            st.rerun()
        st.stop()
        return []
