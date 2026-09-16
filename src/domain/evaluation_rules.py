"""Regras puras para avaliações acadêmicas."""

from __future__ import annotations

from datetime import date


EVALUATION_TYPES = ("Prova", "Trabalho", "Exercício")


def validate_evaluation(title: str, evaluation_type: str, evaluation_date: date, score: float, max_score: float) -> str:
    cleaned_title = " ".join(title.split())
    if not cleaned_title:
        raise ValueError("Informe o nome da avaliação.")
    if evaluation_type not in EVALUATION_TYPES:
        raise ValueError("Escolha um tipo de avaliação válido.")
    if not isinstance(evaluation_date, date):
        raise ValueError("Informe uma data válida.")
    if max_score <= 0:
        raise ValueError("A nota máxima deve ser maior que zero.")
    if score < 0 or score > max_score:
        raise ValueError("A nota obtida deve ficar entre zero e a nota máxima.")
    return cleaned_title
