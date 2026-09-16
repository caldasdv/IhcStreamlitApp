"""Fundação visual do Plano: uma mesa de estudos calma e orientada à ação."""

from __future__ import annotations

import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --plan-bg: #f5f6f1;
            --plan-surface: #fbfcf8;
            --plan-input: #eef3ed;
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
        .block-container { max-width: 1080px; padding-top: 4rem; padding-bottom: 5rem; }
        h1, h2, h3 { color: var(--plan-text); font-weight: 700; letter-spacing: -0.025em; overflow: visible; white-space: normal; overflow-wrap: break-word; }
        h1 { font-size: clamp(2rem, 4vw, 3.1rem); line-height: 1.15; margin-bottom: .55rem; }
        .plan-page-title { font-size: clamp(2rem, 4vw, 3.1rem); line-height: 1.15; margin: 0 0 .55rem; }
        h2 { font-size: 1.55rem; line-height: 1.25; margin-top: 1.8rem; }
        h3 { font-size: 1.1rem; line-height: 1.3; }
        .plan-eyebrow { color: var(--plan-accent); display: block; font-size: .76rem; font-weight: 750; letter-spacing: .08em; line-height: 1.35; margin-bottom: .7rem; overflow: visible; white-space: normal; overflow-wrap: break-word; }
        .plan-page-description { color: var(--plan-muted); font-size: 1.05rem; line-height: 1.55; max-width: 48rem; }
        [data-testid="stCaptionContainer"] p { color: var(--plan-muted); }
        [data-testid="stVerticalBlockBorderWrapper"] { background: var(--plan-surface); border-color: var(--plan-border); border-radius: 14px; box-shadow: 0 4px 18px rgba(30, 45, 49, .045); }
        [data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div { background: var(--plan-input); border-color: var(--plan-border); }
        [data-baseweb="input"] input, [data-baseweb="textarea"] textarea { color: var(--plan-text); }
        [data-testid="stMetric"] { background: var(--plan-surface); border: 1px solid var(--plan-border); border-radius: 14px; padding: 1rem; }
        .plan-session-meta { color: var(--plan-muted); font-size: .82rem; margin-bottom: .3rem; }
        .plan-session-topic { color: var(--plan-text); font-size: 1.2rem; font-weight: 700; line-height: 1.25; }
        .plan-session-goal { color: var(--plan-muted); line-height: 1.45; margin-top: .45rem; }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: var(--plan-muted); }
        [data-testid="stSidebar"] h2 { color: var(--plan-accent-dark); letter-spacing: -.04em; line-height: 1.25; overflow: visible; }
        .stButton button, .stFormSubmitButton button { border-radius: 9px; border-width: 1px; box-shadow: none; font-weight: 650; min-height: 2.7rem; }
        .stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] { background: var(--plan-accent); border-color: var(--plan-accent); color: #ffffff; }
        .stButton button[kind="primary"]:hover, .stFormSubmitButton button[kind="primary"]:hover { background: var(--plan-accent-dark); border-color: var(--plan-accent-dark); }
        .stButton button:focus-visible, .stFormSubmitButton button:focus-visible,
        input:focus-visible, textarea:focus-visible, [role="combobox"]:focus-visible { outline: 3px solid var(--plan-attention); outline-offset: 2px; }
        button, input, textarea, select { min-height: 2.5rem; }
        .subject-dot { display: inline-block; width: .7rem; height: .7rem; border-radius: 50%; margin-right: .35rem; vertical-align: .05rem; }
        .plan-subject-swatch { width: 1rem; height: 1rem; border-radius: 50%; margin-bottom: .7rem; }
        .plan-timetable-hint { color: var(--plan-muted); display: none; font-size: .8rem; margin: -.25rem 0 .5rem; }
        .plan-timetable-scroll { max-width: 100%; overflow-x: auto; overscroll-behavior-inline: contain; padding: .15rem .15rem .75rem; scrollbar-color: var(--plan-accent) var(--plan-input); scrollbar-width: thin; }
        .plan-timetable { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: .8rem; min-width: 0; }
        .plan-timetable-day { background: var(--plan-input); border: 1px solid var(--plan-border); border-radius: 14px; min-height: 16rem; padding: 1rem; }
        .plan-timetable-day h3 { border-bottom: 1px solid var(--plan-border); color: var(--plan-accent-dark); font-size: .95rem; letter-spacing: .06em; margin: 0 0 .9rem; padding-bottom: .7rem; text-transform: uppercase; }
        .plan-meeting { background: var(--plan-surface); border-left: 5px solid var(--meeting-color); border-radius: 9px; box-shadow: 0 2px 8px rgba(30, 45, 49, .06); display: flex; flex-direction: column; gap: .3rem; margin-bottom: .7rem; padding: .8rem; }
        .plan-meeting strong { color: var(--plan-text); font-size: .95rem; }
        .plan-meeting span { color: var(--plan-text); font-size: .9rem; line-height: 1.3; }
        .plan-meeting-location { color: var(--plan-muted) !important; font-size: .8rem !important; }
        .plan-timetable-empty { color: var(--plan-muted); font-size: .85rem; margin: 3.8rem 0 0; text-align: center; }
        .plan-progress-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .8rem; }
        .plan-progress-card { background: var(--plan-surface); border: 1px solid var(--plan-border); border-radius: 14px; padding: 1rem; }
        .plan-progress-card-heading { align-items: baseline; display: flex; justify-content: space-between; gap: 1rem; }
        .plan-progress-card-heading strong { color: var(--plan-text); font-size: 1rem; }
        .plan-progress-card-heading span { color: var(--plan-accent-dark); font-size: .95rem; font-weight: 750; }
        .plan-progress-track { background: var(--plan-input); border-radius: 999px; height: .6rem; margin: .8rem 0 .55rem; overflow: hidden; }
        .plan-progress-track span { background: var(--plan-accent); border-radius: inherit; display: block; height: 100%; }
        .plan-progress-card-meta, .plan-progress-card-status { color: var(--plan-muted); font-size: .82rem; line-height: 1.4; }
        .plan-progress-card-status { margin-top: .2rem; }
        @media (max-width: 640px) {
            .block-container { padding-top: 2.75rem; padding-left: 1rem; padding-right: 1rem; }
            h1 { font-size: 2rem; }
            [data-testid="stHorizontalBlock"] { gap: .5rem; }
        }
        @media (max-width: 768px) {
            .plan-timetable-hint { display: block; }
            .plan-timetable-scroll { -webkit-overflow-scrolling: touch; }
            .plan-timetable { grid-template-columns: repeat(7, minmax(155px, 1fr)); min-width: 1140px; }
        }
        @media (max-width: 640px) {
            .plan-progress-grid { grid-template-columns: 1fr; }
        }
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after { scroll-behavior: auto !important; transition: none !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
