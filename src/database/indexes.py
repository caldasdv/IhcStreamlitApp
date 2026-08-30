"""Índices necessários para as consultas atuais."""


def ensure_indexes(database) -> None:
    existing_user_indexes = {index["name"]: index for index in database.users.list_indexes()}
    email_index = existing_user_indexes.get("email_1")
    if email_index and email_index.get("unique"):
        database.users.drop_index("email_1")
    database.users.create_index(
        [("identity.provider", 1), ("identity.subject", 1)],
        unique=True,
        partialFilterExpression={
            "identity.provider": {"$exists": True},
            "identity.subject": {"$exists": True},
        },
    )
    existing_subject_indexes = {
        index["name"]: index for index in database.subjects.list_indexes()
    }
    legacy_unique_subject_index = existing_subject_indexes.get(
        "user_id_1_name_normalized_1"
    )
    if legacy_unique_subject_index and legacy_unique_subject_index.get("unique"):
        database.subjects.drop_index("user_id_1_name_normalized_1")
    database.subjects.create_index(
        [("user_id", 1), ("academic_period_id", 1), ("name", 1)]
    )
    database.subjects.create_index(
        [("user_id", 1), ("academic_period_id", 1), ("name_normalized", 1)],
        unique=True,
        partialFilterExpression={
            "academic_period_id": {"$exists": True},
            "name_normalized": {"$exists": True},
        },
    )
    database.academic_periods.create_index(
        [("user_id", 1), ("name_normalized", 1)],
        unique=True,
        partialFilterExpression={"name_normalized": {"$exists": True}},
    )
    database.academic_periods.create_index(
        [("user_id", 1), ("status", 1), ("start_date", -1)]
    )
    database.study_sessions.create_index([("user_id", 1), ("study_date", 1), ("study_time", 1)])
