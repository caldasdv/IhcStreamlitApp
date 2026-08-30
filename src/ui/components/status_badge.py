"""Apresentação textual e visual dos estados de sessão."""

from __future__ import annotations

import streamlit as st


def render_status(status: str) -> None:
    """Comunica o estado sem depender exclusivamente de cor."""
    messages = {
        "Concluída": (st.success, "✓ Concluída"),
        "Atrasada": (st.error, "! Atrasada"),
        "Pendente": (st.warning, "◷ Pendente"),
    }
    render, label = messages.get(status, (st.info, status))
    render(label)
