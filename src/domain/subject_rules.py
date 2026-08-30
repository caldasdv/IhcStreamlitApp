"""Regras puras do domínio de disciplinas."""

from __future__ import annotations

import unicodedata


def normalize_subject_name(name: str) -> str:
    """Normaliza um nome para comparação sem alterar o texto exibido."""
    collapsed = " ".join(name.split())
    return unicodedata.normalize("NFKC", collapsed).casefold()
