"""Leitura centralizada da configuração sem expor credenciais."""

from __future__ import annotations

import os
from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class Settings:
    mongodb_uri: str
    database_name: str


def _secret_value(name: str) -> str | None:
    try:
        value = st.secrets.get(name)
    except Exception:
        return None
    return str(value) if value else None


def get_settings() -> Settings:
    """Obtém Secrets do Streamlit e usa ambiente como fallback local."""
    try:
        mongodb = st.secrets.get("mongodb", {})
        nested_uri = mongodb.get("uri") if hasattr(mongodb, "get") else None
        nested_database = mongodb.get("database") if hasattr(mongodb, "get") else None
    except Exception:
        nested_uri = None
        nested_database = None

    uri = nested_uri or _secret_value("MONGODB_URI") or os.getenv("MONGODB_URI")
    database_name = (
        nested_database
        or _secret_value("MONGODB_DATABASE")
        or os.getenv("MONGODB_DATABASE")
        or "plano_estudos"
    )
    if not uri:
        raise RuntimeError("MONGODB_URI não foi configurada nos Secrets ou no ambiente.")
    return Settings(mongodb_uri=str(uri), database_name=str(database_name))
