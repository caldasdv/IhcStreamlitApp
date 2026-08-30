"""Estilos visuais legados do protótipo."""

from __future__ import annotations

import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp { background: #ffffff; color: #37352f; }
        [data-testid="stSidebar"] { background: #f7f6f3; border-right: 1px solid #e9e9e7; }
        [data-testid="stSidebar"] section { padding-top: 1.5rem; }
        .block-container { max-width: 960px; padding-top: 3.5rem; padding-bottom: 5rem; }
        h1, h2, h3 { color: #37352f; font-weight: 650; letter-spacing: -0.02em; }
        h1 { font-size: 2.35rem; margin-bottom: .35rem; }
        h2 { font-size: 1.45rem; }
        h3 { font-size: 1.08rem; }
        [data-testid="stCaptionContainer"] p { color: #9b9a97; letter-spacing: .04em; }
        [data-testid="stVerticalBlockBorderWrapper"] { border-color: #e9e9e7; border-radius: 5px; box-shadow: none; }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #787774; }
        .stButton button, .stFormSubmitButton button { border-radius: 4px; box-shadow: none; }
        </style>
        """,
        unsafe_allow_html=True,
    )
