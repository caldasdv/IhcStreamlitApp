"""Implementações MongoDB dos repositories do MVP."""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from src.domain.exceptions import (
    DuplicateAcademicPeriodError,
    DuplicateSubjectError,
    EntityNotFoundError,
)


class MongoUserRepository:
    def __init__(self, database) -> None:
        self.collection = database.users

    def find_or_create_by_identity(self, identity: dict[str, str]) -> dict[str, Any]:
        return self.collection.find_one_and_update(
            {
                "identity.provider": identity["provider"],
                "identity.subject": identity["subject"],
            },
            {
                "$setOnInsert": {
                    "identity": {
                        "provider": identity["provider"],
                        "subject": identity["subject"],
                    },
                    "name": identity["name"],
                    "email": identity["email"],
                    "weekly_goal_minutes": 300,
                }
            },
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

    def update_weekly_goal(self, user_id: Any, minutes: int) -> None:
        self.collection.update_one({"_id": user_id}, {"$set": {"weekly_goal_minutes": minutes}})

    def update_current_academic_period(self, user_id: Any, period_id: Any) -> None:
        result = self.collection.update_one(
            {"_id": user_id}, {"$set": {"current_academic_period_id": period_id}}
        )
        if result.matched_count == 0:
            raise EntityNotFoundError("O usuário autenticado não foi encontrado.")


class MongoAcademicPeriodRepository:
    def __init__(self, database) -> None:
        self.collection = database.academic_periods

    def list_by_user(self, user_id: Any) -> list[dict[str, Any]]:
        return list(
            self.collection.find({"user_id": user_id}).sort(
                [("start_date", -1), ("name", 1)]
            )
        )

    def exists_by_normalized_name(self, user_id: Any, normalized_name: str) -> bool:
        return self.collection.find_one(
            {"user_id": user_id, "name_normalized": normalized_name}, {"_id": 1}
        ) is not None

    def create(
        self,
        user_id: Any,
        name: str,
        normalized_name: str,
        start_date: date,
        end_date: date,
    ) -> Any:
        now = datetime.now(UTC)
        try:
            return self.collection.insert_one(
                {
                    "user_id": user_id,
                    "name": name,
                    "name_normalized": normalized_name,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "status": "ACTIVE",
                    "created_at": now,
                    "updated_at": now,
                }
            ).inserted_id
        except DuplicateKeyError as error:
            raise DuplicateAcademicPeriodError(
                "Você já possui um período acadêmico com esse nome."
            ) from error

    def is_active_owned_by(self, user_id: Any, period_id: Any) -> bool:
        return self.collection.find_one(
            {"_id": period_id, "user_id": user_id, "status": "ACTIVE"}, {"_id": 1}
        ) is not None

    def archive(self, user_id: Any, period_id: Any) -> None:
        result = self.collection.update_one(
            {"_id": period_id, "user_id": user_id, "status": "ACTIVE"},
            {"$set": {"status": "ARCHIVED", "updated_at": datetime.now(UTC)}},
        )
        if result.matched_count == 0:
            raise EntityNotFoundError("O período não foi encontrado ou já está arquivado.")


class MongoSubjectRepository:
    def __init__(self, database) -> None:
        self.collection = database.subjects

    def list_by_user(self, user_id: Any) -> list[dict[str, Any]]:
        return list(self.collection.find({"user_id": user_id}).sort("name", 1))

    def belongs_to_user(self, user_id: Any, subject_id: Any) -> bool:
        return self.collection.find_one({"_id": subject_id, "user_id": user_id}, {"_id": 1}) is not None

    def exists_by_normalized_name(self, user_id: Any, normalized_name: str) -> bool:
        return self.collection.find_one(
            {"user_id": user_id, "name_normalized": normalized_name}, {"_id": 1}
        ) is not None

    def create(self, user_id: Any, name: str, normalized_name: str, color: str) -> Any:
        try:
            return self.collection.insert_one(
                {
                    "user_id": user_id,
                    "name": name,
                    "name_normalized": normalized_name,
                    "color": color,
                }
            ).inserted_id
        except DuplicateKeyError as error:
            raise DuplicateSubjectError("Você já possui uma disciplina com esse nome.") from error


class MongoStudySessionRepository:
    def __init__(self, database) -> None:
        self.collection = database.study_sessions

    def list_by_user(
        self, user_id: Any, start_date: date | None = None, end_date: date | None = None
    ) -> list[dict[str, Any]]:
        query: dict[str, Any] = {"user_id": user_id}
        if start_date is not None or end_date is not None:
            date_range: dict[str, str] = {}
            if start_date is not None:
                date_range["$gte"] = start_date.isoformat()
            if end_date is not None:
                date_range["$lte"] = end_date.isoformat()
            query["study_date"] = date_range
        return list(self.collection.find(query).sort([("study_date", 1), ("study_time", 1)]))

    def list_pending_by_date(self, user_id: Any, study_date: date) -> list[dict[str, Any]]:
        return list(
            self.collection.find(
                {"user_id": user_id, "study_date": study_date.isoformat(), "status": "Pendente"},
                {"study_time": 1, "duration": 1},
            )
        )

    def create(self, data: dict[str, Any]) -> Any:
        return self.collection.insert_one(data).inserted_id

    def update(self, session_id: Any, user_id: Any, data: dict[str, Any]) -> None:
        result = self.collection.update_one({"_id": session_id, "user_id": user_id}, {"$set": data})
        if result.matched_count == 0:
            raise EntityNotFoundError("A sessão não foi encontrada ou não está mais disponível.")

    def mark_completed(self, session_id: Any, user_id: Any) -> None:
        result = self.collection.update_one(
            {"_id": session_id, "user_id": user_id}, {"$set": {"status": "Concluída"}}
        )
        if result.matched_count == 0:
            raise EntityNotFoundError("A sessão não foi encontrada ou não está mais disponível.")

    def delete(self, session_id: Any, user_id: Any) -> None:
        result = self.collection.delete_one({"_id": session_id, "user_id": user_id})
        if result.deleted_count == 0:
            raise EntityNotFoundError("A sessão não foi encontrada ou não está mais disponível.")
