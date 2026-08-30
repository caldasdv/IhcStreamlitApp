"""Contratos mínimos usados pelos services."""

from __future__ import annotations

from datetime import date
from typing import Any, Iterable, Protocol


class UserRepository(Protocol):
    def find_first(self) -> dict[str, Any] | None: ...

    def update_weekly_goal(self, user_id: Any, minutes: int) -> None: ...


class SubjectRepository(Protocol):
    def list_by_user(self, user_id: Any) -> list[dict[str, Any]]: ...

    def create(self, user_id: Any, name: str, color: str) -> Any: ...


class StudySessionRepository(Protocol):
    def list_by_user(self, user_id: Any) -> list[dict[str, Any]]: ...

    def list_pending_by_date(self, user_id: Any, study_date: date) -> Iterable[dict[str, Any]]: ...

    def create(self, data: dict[str, Any]) -> Any: ...

    def mark_completed(self, session_id: Any, user_id: Any) -> None: ...

    def delete(self, session_id: Any, user_id: Any) -> None: ...
