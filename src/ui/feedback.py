"""Feedback consistente para falhas de interação na UI."""

from __future__ import annotations

import logging

import streamlit as st


logger = logging.getLogger(__name__)


def show_action_error(action: str, error: Exception) -> None:
    """Registra detalhes técnicos sem expor infraestrutura ao usuário."""
    logger.exception("Falha ao %s", action)
    st.error(f"Não foi possível {action}.")
    st.caption("Verifique os dados e tente novamente. Se o problema continuar, tente mais tarde.")
