from datetime import date

import pytest

from src.services.academic_period_service import AcademicPeriodService


class FakeAcademicPeriodRepository:
    def __init__(self) -> None:
        self.periods = []
        self.created = []
        self.archived = []
        self.active_owned_ids = set()

    def list_by_user(self, user_id):
        return [period for period in self.periods if period["user_id"] == user_id]

    def exists_by_normalized_name(self, user_id, normalized_name):
        return any(
            period.get("name_normalized") == normalized_name
            for period in self.list_by_user(user_id)
        )

    def create(self, user_id, name, normalized_name, start_date, end_date):
        period_id = f"period-{len(self.created) + 1}"
        self.created.append(
            (user_id, name, normalized_name, start_date, end_date)
        )
        self.active_owned_ids.add((user_id, period_id))
        return period_id

    def is_active_owned_by(self, user_id, period_id):
        return (user_id, period_id) in self.active_owned_ids

    def archive(self, user_id, period_id):
        self.archived.append((user_id, period_id))


class FakeUserRepository:
    def __init__(self) -> None:
        self.current_updates = []

    def update_current_academic_period(self, user_id, period_id):
        self.current_updates.append((user_id, period_id))


def test_first_period_becomes_current() -> None:
    periods = FakeAcademicPeriodRepository()
    users = FakeUserRepository()
    service = AcademicPeriodService(periods, users)

    period_id = service.create(
        user_id="user-id",
        current_period_id=None,
        name="  Semestre  2026.2 ",
        start_date=date(2026, 7, 1),
        end_date=date(2026, 12, 31),
    )

    assert period_id == "period-1"
    assert periods.created[0][1:3] == ("Semestre 2026.2", "semestre 2026.2")
    assert users.current_updates == [("user-id", "period-1")]


def test_additional_period_does_not_replace_current_automatically() -> None:
    periods = FakeAcademicPeriodRepository()
    users = FakeUserRepository()
    service = AcademicPeriodService(periods, users)

    service.create(
        user_id="user-id",
        current_period_id="current-period",
        name="Semestre 2027.1",
        start_date=date(2027, 1, 1),
        end_date=date(2027, 6, 30),
    )

    assert users.current_updates == []


def test_duplicate_legacy_period_name_is_rejected() -> None:
    periods = FakeAcademicPeriodRepository()
    periods.periods.append(
        {"_id": "legacy", "user_id": "user-id", "name": "Semestre 2026.2"}
    )
    service = AcademicPeriodService(periods, FakeUserRepository())

    with pytest.raises(ValueError, match="já possui"):
        service.create(
            user_id="user-id",
            current_period_id=None,
            name=" semestre   2026.2 ",
            start_date=date(2026, 7, 1),
            end_date=date(2026, 12, 31),
        )


def test_current_period_must_be_active_and_owned() -> None:
    service = AcademicPeriodService(
        FakeAcademicPeriodRepository(), FakeUserRepository()
    )

    with pytest.raises(ValueError, match="período ativo"):
        service.set_current("user-id", "another-period")


def test_active_owned_period_can_become_current() -> None:
    periods = FakeAcademicPeriodRepository()
    periods.active_owned_ids.add(("user-id", "period-id"))
    users = FakeUserRepository()

    AcademicPeriodService(periods, users).set_current("user-id", "period-id")

    assert users.current_updates == [("user-id", "period-id")]


def test_current_period_cannot_be_archived() -> None:
    service = AcademicPeriodService(
        FakeAcademicPeriodRepository(), FakeUserRepository()
    )

    with pytest.raises(ValueError, match="outro período atual"):
        service.archive("user-id", "period-id", "period-id")


def test_non_current_period_can_be_archived() -> None:
    periods = FakeAcademicPeriodRepository()

    AcademicPeriodService(periods, FakeUserRepository()).archive(
        "user-id", "old-period", "current-period"
    )

    assert periods.archived == [("user-id", "old-period")]
