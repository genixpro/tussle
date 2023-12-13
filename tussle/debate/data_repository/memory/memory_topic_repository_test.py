from tussle.debate.data_repository.topic_repository_test_base import TopicRepositoryTestBase
from .memory_topic_repository import MemoryTopicRepository
from tussle.general.testing.test_case_base import TussleTestCaseBase


class MemoryTopicRepositoryTest(TopicRepositoryTestBase, TussleTestCaseBase):
    def create_topic_repository(self):
        return MemoryTopicRepository()

