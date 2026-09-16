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
