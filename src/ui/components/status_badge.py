"""Apresentação textual e visual dos estados de sessão."""

from __future__ import annotations

from html import escape

import streamlit as st


def render_status(status: str) -> None:
    """Comunica o estado sem depender exclusivamente de cor."""
    messages = {
        "Concluída": ("done", "✓ Concluída"),
        "Atrasada": ("overdue", "! Atrasada"),
        "Pendente": ("pending", "◷ Pendente"),
    }
    badge_class, label = messages.get(status, ("neutral", status))
    st.markdown(
        f'<span class="plan-status-badge plan-status-{badge_class}">{escape(label)}</span>',
        unsafe_allow_html=True,
    )
