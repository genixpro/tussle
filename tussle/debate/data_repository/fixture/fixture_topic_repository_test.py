from tussle.debate.data_repository.topic_repository_test_base import TopicRepositoryTestBase
from .fixture_topic_repository import FixtureTopicRepository
from tussle.general.testing.test_case_base import TussleTestCaseBase
from tussle.debate.components.topic import Topic


class FixtureTopicRepositoryTest(TopicRepositoryTestBase, TussleTestCaseBase):
    def create_topic_repository(self):
        return FixtureTopicRepository()



    def test_load_test_case_topic(self):
        """
        This code checks that we are able to load a topic from the list of test fixtures.
        :return:
        """

        topic = self.repository.get_by_id("test_topic_1")

        self.assertIsNotNone(topic)

        self.assertIsInstance(topic, Topic)

