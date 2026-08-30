"""Casos de uso de períodos acadêmicos."""

from __future__ import annotations

from datetime import date
from typing import Any

from src.domain.academic_period_rules import (
    normalize_academic_period_name,
    validate_academic_period,
)
from src.domain.exceptions import DuplicateAcademicPeriodError


class AcademicPeriodService:
    def __init__(self, repository, user_repository) -> None:
        self.repository = repository
        self.user_repository = user_repository

    def list_for_user(self, user_id: Any) -> list[dict[str, Any]]:
        return self.repository.list_by_user(user_id)

    def create(
        self,
        *,
        user_id: Any,
        current_period_id: Any | None,
        name: str,
        start_date: date,
        end_date: date,
    ) -> Any:
        cleaned_name = " ".join(name.split())
        validate_academic_period(cleaned_name, start_date, end_date)
        normalized_name = normalize_academic_period_name(cleaned_name)
        legacy_duplicate = any(
            normalize_academic_period_name(str(period.get("name", ""))) == normalized_name
            for period in self.repository.list_by_user(user_id)
        )
        if legacy_duplicate or self.repository.exists_by_normalized_name(user_id, normalized_name):
            raise DuplicateAcademicPeriodError(
                "Você já possui um período acadêmico com esse nome."
            )
        period_id = self.repository.create(
            user_id, cleaned_name, normalized_name, start_date, end_date
        )
        if current_period_id is None:
            self.user_repository.update_current_academic_period(user_id, period_id)
        return period_id

    def set_current(self, user_id: Any, period_id: Any) -> None:
        if not self.repository.is_active_owned_by(user_id, period_id):
            raise ValueError("Selecione um período ativo do seu plano.")
        self.user_repository.update_current_academic_period(user_id, period_id)

    def archive(self, user_id: Any, period_id: Any, current_period_id: Any | None) -> None:
        if period_id == current_period_id:
            raise ValueError("Escolha outro período atual antes de arquivar este período.")
        self.repository.archive(user_id, period_id)
