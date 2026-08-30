"""Cabeçalho consistente para páginas do produto."""

from __future__ import annotations

import streamlit as st


def render_page_header(eyebrow: str, title: str, description: str) -> None:
    """Apresenta contexto, título e objetivo da tela na mesma ordem."""
    st.caption(eyebrow)
    st.title(title)
    st.write(description)
