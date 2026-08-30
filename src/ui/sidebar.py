"""Elementos compartilhados da barra lateral."""

from __future__ import annotations

import streamlit as st

from src.services.container import ApplicationServices
from src.ui.feedback import show_action_error


def render_account_sidebar(services: ApplicationServices, user: dict) -> None:
    st.sidebar.markdown("## Plano")
    st.sidebar.caption("Seu espaço de estudos")
    st.sidebar.divider()
    st.sidebar.write(user["name"])
    st.sidebar.caption(user["email"])
    st.sidebar.divider()
    st.sidebar.caption("Meta semanal")
    goal_hours = st.sidebar.number_input(
        "Horas",
        min_value=1.0,
        max_value=80.0,
        value=user.get("weekly_goal_minutes", 300) / 60,
        step=0.5,
        label_visibility="collapsed",
        key="weekly_goal_hours",
    )
    if st.sidebar.button("Salvar meta", width="stretch"):
        try:
            services.users.update_weekly_goal(user["_id"], goal_hours)
        except Exception as error:
            show_action_error("atualizar sua meta", error)
        else:
            st.sidebar.success("Meta atualizada.")
            st.rerun()
