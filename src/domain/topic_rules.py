"""Regras puras para tópicos e subtópicos."""

from __future__ import annotations

import unicodedata


TOPIC_STATUSES = ("NOT_STARTED", "IN_PROGRESS", "REVIEWED", "MASTERED")
TOPIC_DIFFICULTIES = ("LOW", "MEDIUM", "HIGH")


def normalize_topic_title(title: str) -> str:
    return unicodedata.normalize("NFKC", " ".join(title.split())).casefold()


def validate_topic(title: str, status: str, difficulty: str) -> None:
    if not title.strip():
        raise ValueError("Informe o nome do tópico.")
    if status not in TOPIC_STATUSES:
        raise ValueError("Selecione um status válido para o tópico.")
    if difficulty not in TOPIC_DIFFICULTIES:
        raise ValueError("Selecione uma dificuldade válida para o tópico.")
