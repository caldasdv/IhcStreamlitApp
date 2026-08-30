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


def test_indexes_replace_email_identity_and_scope_subjects_by_period() -> None:
    users = FakeCollection([{"name": "email_1", "unique": True}])
    subjects = FakeCollection(
        [{"name": "user_id_1_name_normalized_1", "unique": True}]
    )
    sessions = FakeCollection()
    academic_periods = FakeCollection()
    class_meetings = FakeCollection()
    database = SimpleNamespace(
        users=users,
        subjects=subjects,
        study_sessions=sessions,
        academic_periods=academic_periods,
        class_meetings=class_meetings,
    )

    ensure_indexes(database)

    assert users.dropped == ["email_1"]
    assert any(
        keys == [("identity.provider", 1), ("identity.subject", 1)]
        and options["unique"] is True
        for keys, options in users.created
    )
    assert any(
        keys
        == [
            ("user_id", 1),
            ("academic_period_id", 1),
            ("name_normalized", 1),
        ]
        and options["unique"] is True
        for keys, options in subjects.created
    )
    assert subjects.dropped == ["user_id_1_name_normalized_1"]
    assert any(
        keys == [("user_id", 1), ("name_normalized", 1)]
        and options["unique"] is True
        for keys, options in academic_periods.created
    )
    assert any(
        keys
        == [
            ("user_id", 1),
            ("academic_period_id", 1),
            ("weekday", 1),
            ("start_time", 1),
        ]
        for keys, _options in class_meetings.created
    )
