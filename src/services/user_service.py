"""Casos de uso de usuário."""

from __future__ import annotations

from typing import Any


class UserService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def get_active_user(self) -> dict[str, Any]:
        user = self.repository.find_first()
        if not user:
            raise RuntimeError("Nenhum usuário configurado para a aplicação.")
        return user

    def update_weekly_goal(self, user_id: Any, hours: float) -> None:
        self.repository.update_weekly_goal(user_id, round(hours * 60))
