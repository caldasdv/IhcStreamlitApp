"""Implementações MongoDB dos repositories do MVP."""

from __future__ import annotations

from datetime import date
from typing import Any


class MongoUserRepository:
    def __init__(self, database) -> None:
        self.collection = database.users

    def find_first(self) -> dict[str, Any] | None:
        return self.collection.find_one({})

    def update_weekly_goal(self, user_id: Any, minutes: int) -> None:
        self.collection.update_one({"_id": user_id}, {"$set": {"weekly_goal_minutes": minutes}})


class MongoSubjectRepository:
    def __init__(self, database) -> None:
        self.collection = database.subjects

    def list_by_user(self, user_id: Any) -> list[dict[str, Any]]:
        return list(self.collection.find({"user_id": user_id}).sort("name", 1))

    def create(self, user_id: Any, name: str, color: str) -> Any:
        return self.collection.insert_one({"user_id": user_id, "name": name, "color": color}).inserted_id


class MongoStudySessionRepository:
    def __init__(self, database) -> None:
        self.collection = database.study_sessions

    def list_by_user(self, user_id: Any) -> list[dict[str, Any]]:
        return list(self.collection.find({"user_id": user_id}).sort([("study_date", 1), ("study_time", 1)]))

    def list_pending_by_date(self, user_id: Any, study_date: date) -> list[dict[str, Any]]:
        return list(
            self.collection.find(
                {"user_id": user_id, "study_date": study_date.isoformat(), "status": "Pendente"},
                {"study_time": 1, "duration": 1},
            )
        )

    def create(self, data: dict[str, Any]) -> Any:
        return self.collection.insert_one(data).inserted_id

    def mark_completed(self, session_id: Any, user_id: Any) -> None:
        self.collection.update_one({"_id": session_id, "user_id": user_id}, {"$set": {"status": "Concluída"}})

    def delete(self, session_id: Any, user_id: Any) -> None:
        self.collection.delete_one({"_id": session_id, "user_id": user_id})
