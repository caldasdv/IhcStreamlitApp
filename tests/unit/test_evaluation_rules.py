from datetime import date

import pytest

from src.domain.evaluation_rules import validate_evaluation


def test_validate_evaluation_cleans_title():
    assert validate_evaluation("  Lista 1  ", "Exercício", date.today(), 7, 10) == "Lista 1"


@pytest.mark.parametrize("score,max_score", [(-1, 10), (11, 10), (1, 0)])
def test_validate_evaluation_rejects_invalid_range(score, max_score):
    with pytest.raises(ValueError):
        validate_evaluation("Prova", "Prova", date.today(), score, max_score)
