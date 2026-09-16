from datetime import date

import pytest

from src.services.evaluation_service import EvaluationService


class EvaluationRepository:
    def __init__(self):
        self.created = []

    def create(self, data):
        self.created.append(data)
        return "evaluation-id"

    def list_by_period(self, user_id, period_id, subjects):
        return []


class PeriodRepository:
    def is_active_owned_by(self, user_id, period_id):
        return (user_id, period_id) == ("user-id", "period-id")


class SubjectRepository:
    def belongs_to_user_period(self, user_id, subject_id, period_id):
        return (user_id, subject_id, period_id) == ("user-id", "subject-id", "period-id")


def test_create_evaluation_validates_ownership_and_persists_data():
    repository = EvaluationRepository()
    service = EvaluationService(repository, SubjectRepository(), PeriodRepository())

    result = service.create(
        user_id="user-id", academic_period_id="period-id", subject_id="subject-id",
        title="  Prova de SQL  ", evaluation_type="Prova", evaluation_date=date(2026, 9, 16),
        score=8.5, max_score=10,
    )

    assert result == "evaluation-id"
    assert repository.created[0]["title"] == "Prova de SQL"


def test_create_evaluation_rejects_foreign_subject():
    repository = EvaluationRepository()
    service = EvaluationService(repository, SubjectRepository(), PeriodRepository())
    with pytest.raises(ValueError, match="disciplina válida"):
        service.create(
            user_id="user-id", academic_period_id="period-id", subject_id="other",
            title="Exercício", evaluation_type="Exercício", evaluation_date=date.today(),
            score=7, max_score=10,
        )
    assert repository.created == []
