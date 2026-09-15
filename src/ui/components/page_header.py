"""Cabeçalho consistente para páginas do produto."""

from __future__ import annotations

from html import escape

import streamlit as st


def render_page_header(eyebrow: str, title: str, description: str) -> None:
    """Apresenta contexto, título e objetivo da tela na mesma ordem."""
    st.markdown(
        f'<div class="plan-eyebrow">{escape(eyebrow.capitalize())}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<h1 class="plan-page-title">{escape(title)}</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="plan-page-description">{escape(description)}</div>',
        unsafe_allow_html=True,
    )
