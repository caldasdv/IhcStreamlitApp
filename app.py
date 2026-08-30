"""Entrypoint de compatibilidade para o Streamlit Community Cloud."""

# O Community Cloud pode continuar configurado para executar app.py na raiz.
# A aplicação real fica organizada em src/app.py.
from src import app  # noqa: F401
