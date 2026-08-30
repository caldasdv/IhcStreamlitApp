"""Casos de uso de disciplinas."""

from __future__ import annotations

from typing import Any


class SubjectService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_for_user(self, user_id: Any) -> list[dict[str, Any]]:
        return self.repository.list_by_user(user_id)

    def create(self, user_id: Any, name: str, color: str) -> Any:
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("Informe o nome da disciplina.")
        return self.repository.create(user_id, cleaned_name, color)
