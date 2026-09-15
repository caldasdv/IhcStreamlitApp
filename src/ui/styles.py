"""Fundação visual do Plano: uma mesa de estudos calma e orientada à ação."""

from __future__ import annotations

import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --plan-bg: #f5f6f1;
            --plan-surface: #ffffff;
            --plan-text: #1e2d31;
            --plan-muted: #627174;
            --plan-border: #dfe6df;
            --plan-accent: #176b5d;
            --plan-accent-dark: #0f5147;
            --plan-attention: #d69a28;
        }
        .stApp { background: var(--plan-bg); color: var(--plan-text); }
        [data-testid="stSidebar"] { background: #eaf0e9; border-right: 1px solid var(--plan-border); }
        [data-testid="stSidebar"] section { padding-top: 1.25rem; }
        .block-container { max-width: 1080px; padding-top: 2.25rem; padding-bottom: 5rem; }
        h1, h2, h3 { color: var(--plan-text); font-weight: 700; letter-spacing: -0.025em; }
        h1 { font-size: clamp(2rem, 4vw, 3.1rem); line-height: 1.05; margin-bottom: .55rem; }
        h2 { font-size: 1.55rem; margin-top: 1.8rem; }
        h3 { font-size: 1.1rem; }
        .plan-eyebrow { color: var(--plan-accent); font-size: .76rem; font-weight: 750; letter-spacing: .08em; margin-bottom: .7rem; }
        .plan-page-description { color: var(--plan-muted); font-size: 1.05rem; line-height: 1.55; max-width: 48rem; }
        [data-testid="stCaptionContainer"] p { color: var(--plan-muted); }
        [data-testid="stVerticalBlockBorderWrapper"] { background: var(--plan-surface); border-color: var(--plan-border); border-radius: 14px; box-shadow: 0 4px 18px rgba(30, 45, 49, .045); }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: var(--plan-muted); }
        [data-testid="stSidebar"] h2 { color: var(--plan-accent-dark); letter-spacing: -.04em; }
        .stButton button, .stFormSubmitButton button { border-radius: 9px; border-width: 1px; box-shadow: none; font-weight: 650; min-height: 2.7rem; }
        .stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] { background: var(--plan-accent); border-color: var(--plan-accent); }
        .stButton button[kind="primary"]:hover, .stFormSubmitButton button[kind="primary"]:hover { background: var(--plan-accent-dark); border-color: var(--plan-accent-dark); }
        .stButton button:focus-visible, .stFormSubmitButton button:focus-visible,
        input:focus-visible, textarea:focus-visible, [role="combobox"]:focus-visible { outline: 3px solid var(--plan-attention); outline-offset: 2px; }
        button, input, textarea, select { min-height: 2.5rem; }
        .subject-dot { display: inline-block; width: .7rem; height: .7rem; border-radius: 50%; margin-right: .35rem; vertical-align: .05rem; }
        @media (max-width: 640px) {
            .block-container { padding-top: 1.5rem; padding-left: 1rem; padding-right: 1rem; }
            h1 { font-size: 2rem; }
            [data-testid="stHorizontalBlock"] { gap: .5rem; }
        }
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after { scroll-behavior: auto !important; transition: none !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
