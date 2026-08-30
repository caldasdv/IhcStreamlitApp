"""Integração mínima entre a identidade OIDC e a camada de aplicação."""

from __future__ import annotations

import streamlit as st


def require_login() -> None:
    """Interrompe a execução até que o usuário conclua o login."""
    if st.user.is_logged_in:
        return

    st.title("Plano de estudos")
    st.write("Entre para acessar suas disciplinas, sessões e progresso.")
    st.button("Entrar com Google", on_click=st.login)
    st.stop()


def get_current_identity() -> dict[str, str]:
    """Converte os claims necessários do OIDC em uma estrutura estável."""
    subject = str(st.user.get("sub", "")).strip()
    if not subject:
        raise RuntimeError("A identidade do provedor não possui um identificador válido.")
    return {
        "provider": "google",
        "subject": subject,
        "name": str(st.user.get("name", "Estudante")).strip() or "Estudante",
        "email": str(st.user.get("email", "")).strip(),
    }
