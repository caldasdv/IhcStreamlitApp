"""Casos de uso de tópicos e subtópicos."""

from __future__ import annotations

from typing import Any

from src.domain.topic_rules import normalize_topic_title, validate_topic


class TopicService:
    def __init__(self, repository, subject_repository, academic_period_repository) -> None:
        self.repository = repository
        self.subject_repository = subject_repository
        self.academic_period_repository = academic_period_repository

    def list_for_subject(self, user_id: Any, academic_period_id: Any, subject_id: Any) -> list[dict[str, Any]]:
        return self.repository.list_for_subject(user_id, academic_period_id, subject_id)

    def create(
        self, *, user_id: Any, academic_period_id: Any | None, subject_id: Any,
        parent_id: Any | None, title: str, status: str, difficulty: str
    ) -> Any:
        validate_topic(title, status, difficulty)
        if academic_period_id is None or not self.academic_period_repository.is_active_owned_by(user_id, academic_period_id):
            raise ValueError("Defina um período acadêmico ativo para criar tópicos.")
        if not self.subject_repository.belongs_to_user_period(user_id, subject_id, academic_period_id):
            raise ValueError("Selecione uma disciplina válida do período atual.")
        if parent_id is not None and not self.repository.belongs_to_subject(user_id, academic_period_id, subject_id, parent_id):
            raise ValueError("Selecione um tópico pai válido da mesma disciplina.")
        normalized = normalize_topic_title(title)
        if self.repository.exists_by_title(user_id, academic_period_id, subject_id, parent_id, normalized):
            raise ValueError("Já existe um tópico com esse nome neste nível.")
        return self.repository.create(
            user_id, academic_period_id, subject_id, parent_id,
            " ".join(title.split()), normalized, status, difficulty
        )
