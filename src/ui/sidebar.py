"""Elementos compartilhados da barra lateral."""

from __future__ import annotations

from html import escape

import streamlit as st

from src.services.container import ApplicationServices
from src.ui.feedback import set_success_flash, show_action_error


def render_account_sidebar(services: ApplicationServices, user: dict) -> None:
    st.sidebar.markdown(
        '<div class="plan-sidebar-brand"><span class="plan-sidebar-mark">P</span>'
        '<div><strong>Plano</strong><small>Seu espaço de estudos</small></div></div>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        f'<div class="plan-sidebar-user"><strong>{escape(str(user["name"]))}</strong>'
        f'<span>{escape(str(user["email"]))}</span></div>',
        unsafe_allow_html=True,
    )
    if st.sidebar.button("Sair", width="stretch"):
        st.logout()
    st.sidebar.divider()
    dark_mode = bool(user.get("dark_mode", False))
    st.session_state["plan_dark_mode"] = dark_mode
    if st.sidebar.button(
        "Usar modo claro" if dark_mode else "Usar modo escuro",
        icon=":material/light_mode:" if dark_mode else ":material/dark_mode:",
        width="stretch",
        key="toggle_plan_theme",
    ):
        next_mode = not dark_mode
        try:
            services.users.update_dark_mode(user["_id"], next_mode)
        except Exception as error:
            show_action_error("salvar a preferência visual", error)
        else:
            user["dark_mode"] = next_mode
            st.session_state["plan_dark_mode"] = next_mode
            st.rerun()
    dark_mode = bool(user.get("dark_mode", False))
    st.session_state["plan_dark_mode"] = dark_mode
    if dark_mode:
        st.sidebar.markdown(
            '<span class="plan-dark-mode-marker" aria-hidden="true"></span>',
            unsafe_allow_html=True,
        )
    st.sidebar.divider()
    st.sidebar.markdown(
        '<div class="plan-sidebar-section-label">Meta semanal</div>',
        unsafe_allow_html=True,
    )
    goal_hours = st.sidebar.number_input(
        "Horas por semana",
        min_value=1.0,
        max_value=80.0,
        value=user.get("weekly_goal_minutes", 300) / 60,
        step=0.5,
        key="weekly_goal_hours",
    )
    if st.sidebar.button("Salvar meta", width="stretch"):
        try:
            services.users.update_weekly_goal(user["_id"], goal_hours)
        except Exception as error:
            show_action_error("atualizar sua meta", error)
        else:
            set_success_flash("Meta atualizada.")
            st.rerun()
