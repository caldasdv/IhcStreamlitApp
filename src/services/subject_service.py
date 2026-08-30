"""Casos de uso de disciplinas."""

from __future__ import annotations

import re
from typing import Any

from src.domain.exceptions import DuplicateSubjectError
from src.domain.subject_rules import normalize_subject_name


class SubjectService:
    def __init__(self, repository, academic_period_repository) -> None:
        self.repository = repository
        self.academic_period_repository = academic_period_repository

    def list_for_user(self, user_id: Any) -> list[dict[str, Any]]:
        return self.repository.list_by_user(user_id)

    def list_for_period(
        self, user_id: Any, academic_period_id: Any | None
    ) -> list[dict[str, Any]]:
        if academic_period_id is None:
            return []
        return self.repository.list_by_period(user_id, academic_period_id)

    def list_without_period(self, user_id: Any) -> list[dict[str, Any]]:
        return self.repository.list_without_period(user_id)

    def create(
        self,
        user_id: Any,
        academic_period_id: Any | None,
        name: str,
        color: str,
    ) -> Any:
        if academic_period_id is None or not self.academic_period_repository.is_active_owned_by(
            user_id, academic_period_id
        ):
            raise ValueError("Escolha um período acadêmico ativo antes de adicionar disciplinas.")
        cleaned_name = " ".join(name.split())
        if not cleaned_name:
            raise ValueError("Informe o nome da disciplina.")
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
            raise ValueError("Selecione uma cor válida para a disciplina.")
        normalized_name = normalize_subject_name(cleaned_name)
        period_duplicate = any(
            normalize_subject_name(str(subject.get("name", ""))) == normalized_name
            for subject in self.repository.list_by_period(user_id, academic_period_id)
        )
        if period_duplicate or self.repository.exists_by_normalized_name(
            user_id, academic_period_id, normalized_name
        ):
            raise DuplicateSubjectError("Você já possui uma disciplina com esse nome.")
        return self.repository.create(
            user_id, academic_period_id, cleaned_name, normalized_name, color
        )
