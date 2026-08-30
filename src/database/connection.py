"""Conexão compartilhada com o MongoDB Atlas."""

from __future__ import annotations

import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from src.config.settings import get_settings
from src.database.indexes import ensure_indexes


@st.cache_resource
def get_database():
    settings = get_settings()
    client = MongoClient(
        settings.mongodb_uri,
        server_api=ServerApi("1"),
        serverSelectionTimeoutMS=5000,
    )
    client.admin.command("ping")
    database = client[settings.database_name]
    ensure_indexes(database)
    return database
