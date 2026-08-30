"""Índices necessários para as consultas atuais."""


def ensure_indexes(database) -> None:
    database.users.create_index("email", unique=True)
    database.subjects.create_index([("user_id", 1), ("name", 1)])
    database.study_sessions.create_index([("user_id", 1), ("study_date", 1), ("study_time", 1)])
