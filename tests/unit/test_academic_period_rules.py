from datetime import date

import pytest

from src.domain.academic_period_rules import (
    AcademicPeriodValidationError,
    normalize_academic_period_name,
    validate_academic_period,
)


def test_period_name_normalization_collapses_spaces_and_case() -> None:
    assert normalize_academic_period_name("  Semestre   2026.2 ") == "semestre 2026.2"


def test_period_rejects_inverted_date_range() -> None:
    with pytest.raises(AcademicPeriodValidationError, match="data final"):
        validate_academic_period(
            "2026.2", date(2026, 12, 31), date(2026, 7, 1)
        )
