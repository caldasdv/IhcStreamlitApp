"""Índices necessários para as consultas atuais."""


def ensure_indexes(database) -> None:
    database.users.create_index("email", unique=True)
    database.users.create_index(
        [("identity.provider", 1), ("identity.subject", 1)],
        unique=True,
        partialFilterExpression={
            "identity.provider": {"$exists": True},
            "identity.subject": {"$exists": True},
        },
    )
    database.subjects.create_index([("user_id", 1), ("name", 1)])
    database.study_sessions.create_index([("user_id", 1), ("study_date", 1), ("study_time", 1)])
