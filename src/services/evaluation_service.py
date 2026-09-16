"""Casos de uso de avaliações."""

from __future__ import annotations

from datetime import date
from typing import Any

from src.domain.evaluation_rules import validate_evaluation


class EvaluationService:
    def __init__(self, repository, subject_repository, academic_period_repository) -> None:
        self.repository = repository
        self.subject_repository = subject_repository
        self.academic_period_repository = academic_period_repository

    def list_for_period(self, user_id: Any, academic_period_id: Any, subjects: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return self.repository.list_by_period(user_id, academic_period_id, subjects)

    def create(
        self, *, user_id: Any, academic_period_id: Any, subject_id: Any,
        title: str, evaluation_type: str, evaluation_date: date,
        score: float, max_score: float,
    ) -> Any:
        cleaned_title = validate_evaluation(title, evaluation_type, evaluation_date, score, max_score)
        if not self.academic_period_repository.is_active_owned_by(user_id, academic_period_id):
            raise ValueError("Escolha um período acadêmico ativo.")
        if not self.subject_repository.belongs_to_user_period(user_id, subject_id, academic_period_id):
            raise ValueError("Selecione uma disciplina válida do período atual.")
        return self.repository.create(
            {
                "user_id": user_id,
                "academic_period_id": academic_period_id,
                "subject_id": subject_id,
                "title": cleaned_title,
                "type": evaluation_type,
                "evaluation_date": evaluation_date.isoformat(),
                "score": float(score),
                "max_score": float(max_score),
            }
        )
