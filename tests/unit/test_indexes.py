from types import SimpleNamespace

from src.database.indexes import ensure_indexes


class FakeCollection:
    def __init__(self, indexes=None) -> None:
        self.indexes = indexes or []
        self.dropped = []
        self.created = []

    def list_indexes(self):
        return self.indexes

    def drop_index(self, name):
        self.dropped.append(name)

    def create_index(self, keys, **options):
        self.created.append((keys, options))


def test_indexes_replace_email_identity_with_oidc_and_subject_scope() -> None:
    users = FakeCollection([{"name": "email_1", "unique": True}])
    subjects = FakeCollection()
    sessions = FakeCollection()
    academic_periods = FakeCollection()
    database = SimpleNamespace(
        users=users,
        subjects=subjects,
        study_sessions=sessions,
        academic_periods=academic_periods,
    )

    ensure_indexes(database)

    assert users.dropped == ["email_1"]
    assert any(
        keys == [("identity.provider", 1), ("identity.subject", 1)]
        and options["unique"] is True
        for keys, options in users.created
    )
    assert any(
        keys == [("user_id", 1), ("name_normalized", 1)]
        and options["unique"] is True
        for keys, options in subjects.created
    )
    assert any(
        keys == [("user_id", 1), ("name_normalized", 1)]
        and options["unique"] is True
        for keys, options in academic_periods.created
    )
