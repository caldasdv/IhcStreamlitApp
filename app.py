"""Shell principal do Streamlit Community Cloud."""

from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.ui.styles import apply_styles


PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIR / ".env")
st.set_page_config(page_title="Plano", page_icon="◷", layout="wide")
apply_styles()

page = st.navigation(
    [
        st.Page("app_pages/overview.py", title="Visão geral", icon=":material/home:"),
        st.Page("app_pages/new_session.py", title="Nova sessão", icon=":material/add_circle:"),
        st.Page("app_pages/progress.py", title="Progresso", icon=":material/analytics:"),
        st.Page("app_pages/subjects.py", title="Disciplinas", icon=":material/menu_book:"),
    ],
    position="sidebar",
)
page.run()
