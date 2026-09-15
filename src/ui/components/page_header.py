"""Cabeçalho consistente para páginas do produto."""

from __future__ import annotations

import streamlit as st


def render_page_header(eyebrow: str, title: str, description: str) -> None:
    """Apresenta contexto, título e objetivo da tela na mesma ordem."""
    st.markdown(f'<div class="plan-eyebrow">{eyebrow.capitalize()}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<div class="plan-page-description">{description}</div>', unsafe_allow_html=True)
