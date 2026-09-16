import pytest

from src.services.topic_service import TopicService


class FakeTopicRepository:
    def __init__(self):
        self.topics = []
        self.created = []

    def list_for_subject(self, user_id, period_id, subject_id):
        return self.topics

    def belongs_to_subject(self, user_id, period_id, subject_id, topic_id):
        return any(topic["_id"] == topic_id and topic["subject_id"] == subject_id for topic in self.topics)

    def exists_by_title(self, user_id, period_id, subject_id, parent_id, title_normalized):
        return any(topic.get("parent_id") == parent_id and topic["title_normalized"] == title_normalized for topic in self.topics)

    def create(self, user_id, period_id, subject_id, parent_id, title, normalized, status, difficulty):
        self.created.append((user_id, period_id, subject_id, parent_id, title, normalized, status, difficulty))
        return "topic-id"


class FakeSubjectRepository:
    def belongs_to_user_period(self, user_id, subject_id, period_id):
        return (user_id, subject_id, period_id) == ("user-id", "subject-id", "period-id")


class FakePeriodRepository:
    def is_active_owned_by(self, user_id, period_id):
        return (user_id, period_id) == ("user-id", "period-id")


def build_service(repository=None):
    return TopicService(repository or FakeTopicRepository(), FakeSubjectRepository(), FakePeriodRepository())


def test_create_topic_normalizes_title():
    repository = FakeTopicRepository()

    result = build_service(repository).create(
        user_id="user-id", academic_period_id="period-id", subject_id="subject-id",
        parent_id=None, title="  SQL   básico ", status="NOT_STARTED", difficulty="MEDIUM"
    )

    assert result == "topic-id"
    assert repository.created[0][4:6] == ("SQL básico", "sql básico")


def test_create_subtopic_requires_parent_from_same_subject():
    repository = FakeTopicRepository()
    repository.topics.append({"_id": "other", "subject_id": "other-subject", "title_normalized": "sql"})

    with pytest.raises(ValueError, match="tópico pai válido"):
        build_service(repository).create(
            user_id="user-id", academic_period_id="period-id", subject_id="subject-id",
            parent_id="other", title="JOIN", status="IN_PROGRESS", difficulty="HIGH"
        )
