"""Regras puras do domínio de períodos acadêmicos."""

from __future__ import annotations

import unicodedata
from datetime import date


class AcademicPeriodValidationError(ValueError):
    """Indica dados inválidos para um período acadêmico."""


def normalize_academic_period_name(name: str) -> str:
    """Normaliza o nome para comparação por usuário."""
    return unicodedata.normalize("NFKC", " ".join(name.split())).casefold()


def validate_academic_period(name: str, start_date: date, end_date: date) -> None:
    """Valida nome e intervalo de um período acadêmico."""
    if not name.strip():
        raise AcademicPeriodValidationError("Informe o nome do período acadêmico.")
    if end_date < start_date:
        raise AcademicPeriodValidationError("A data final deve ser igual ou posterior à inicial.")
