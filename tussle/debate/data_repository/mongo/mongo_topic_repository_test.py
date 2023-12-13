from tussle.debate.data_repository.topic_repository_test_base import TopicRepositoryTestBase
from .mongo_topic_repository import MongoTopicRepository
from tussle.general.testing.test_case_base import TussleTestCaseBase


class MongoTopicRepositoryTest(TopicRepositoryTestBase, TussleTestCaseBase):
    def create_topic_repository(self):
        return MongoTopicRepository(
            mongo_db_connection=self.container.mongo_db_connection(),
        )

