"""Integração mínima entre a identidade OIDC e a camada de aplicação."""

from __future__ import annotations

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError


def _auth_is_configured() -> bool:
    """Verifica se o provedor OIDC local possui as credenciais necessárias."""
    try:
        auth = st.secrets.get("auth", {})
    except StreamlitSecretNotFoundError:
        return False
    required_keys = ("redirect_uri", "cookie_secret", "client_id", "client_secret")
    return all(str(auth.get(key, "")).strip() for key in required_keys)


def require_login() -> None:
    """Interrompe a execução até que o usuário conclua o login."""
    if st.user.get("is_logged_in", False):
        return

    st.title("Plano de estudos")
    st.write("Entre para acessar suas disciplinas, sessões e progresso.")
    if not _auth_is_configured():
        st.warning("O login ainda não está configurado neste ambiente.")
        st.caption(
            "Crie `.streamlit/secrets.toml` a partir do arquivo `.streamlit/secrets.toml.example` "
            "e preencha as credenciais do Google."
        )
        st.stop()
    st.button("Entrar com Google", type="primary", on_click=st.login, width="stretch")
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
