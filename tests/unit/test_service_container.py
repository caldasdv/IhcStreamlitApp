from types import SimpleNamespace

from src.services import container


def test_application_services_are_rebuilt_while_database_remains_external(
    monkeypatch,
) -> None:
    """Evita manter instâncias de classes antigas após hot reload/deploy."""
    database = SimpleNamespace(
        users=object(),
        academic_periods=object(),
        subjects=object(),
        class_meetings=object(),
        study_sessions=object(),
    )
    monkeypatch.setattr(container, "get_database", lambda: database)

    first = container.get_application_services()
    second = container.get_application_services()

    assert first is not second
    assert first.subjects is not second.subjects
    assert first.subjects.repository.collection is database.subjects
    assert second.subjects.repository.collection is database.subjects
