"""Casos de uso de disciplinas."""

from __future__ import annotations

import re
from typing import Any

from src.domain.exceptions import DuplicateSubjectError
from src.domain.subject_rules import normalize_subject_name


class SubjectService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_for_user(self, user_id: Any) -> list[dict[str, Any]]:
        return self.repository.list_by_user(user_id)

    def create(self, user_id: Any, name: str, color: str) -> Any:
        cleaned_name = " ".join(name.split())
        if not cleaned_name:
            raise ValueError("Informe o nome da disciplina.")
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
            raise ValueError("Selecione uma cor válida para a disciplina.")
        normalized_name = normalize_subject_name(cleaned_name)
        legacy_duplicate = any(
            normalize_subject_name(str(subject.get("name", ""))) == normalized_name
            for subject in self.repository.list_by_user(user_id)
        )
        if legacy_duplicate or self.repository.exists_by_normalized_name(user_id, normalized_name):
            raise DuplicateSubjectError("Você já possui uma disciplina com esse nome.")
        return self.repository.create(user_id, cleaned_name, normalized_name, color)
