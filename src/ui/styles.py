"""Estilos visuais legados do protótipo."""

from __future__ import annotations

import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp { background: #ffffff; color: #37352f; }
        :root { --plan-text: #37352f; --plan-muted: #5f5e5b; --plan-border: #e9e9e7; --plan-accent: #5e6ad2; }
        [data-testid="stSidebar"] { background: #f7f6f3; border-right: 1px solid #e9e9e7; }
        [data-testid="stSidebar"] section { padding-top: 1.5rem; }
        .block-container { max-width: 960px; padding-top: 3.5rem; padding-bottom: 5rem; }
        h1, h2, h3 { color: #37352f; font-weight: 650; letter-spacing: -0.02em; }
        h1 { font-size: 2.35rem; margin-bottom: .35rem; }
        h2 { font-size: 1.45rem; }
        h3 { font-size: 1.08rem; }
        [data-testid="stCaptionContainer"] p { color: #5f5e5b; letter-spacing: .04em; }
        [data-testid="stVerticalBlockBorderWrapper"] { border-color: var(--plan-border); border-radius: 8px; box-shadow: none; }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #787774; }
        .stButton button, .stFormSubmitButton button { border-radius: 4px; box-shadow: none; }
        .stButton button:focus-visible, .stFormSubmitButton button:focus-visible,
        input:focus-visible, textarea:focus-visible { outline: 3px solid #5e6ad2; outline-offset: 2px; }
        .subject-dot { display: inline-block; width: .7rem; height: .7rem; border-radius: 50%; margin-right: .35rem; vertical-align: .05rem; }
        @media (max-width: 640px) {
            .block-container { padding-top: 1.5rem; padding-left: 1rem; padding-right: 1rem; }
            h1 { font-size: 1.9rem; }
            [data-testid="stHorizontalBlock"] { gap: .5rem; }
        }
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after { scroll-behavior: auto !important; transition: none !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
