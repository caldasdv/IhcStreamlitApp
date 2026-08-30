from src.domain.subject_rules import normalize_subject_name


def test_subject_name_normalization_collapses_spaces_and_case() -> None:
    assert normalize_subject_name("  Interação   Humano-Computador ") == (
        "interação humano-computador"
    )
