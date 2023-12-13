from tussle.debate.data_repository.topic_repository_test_base import TopicRepositoryTestBase
from tussle.debate.data_repository.memory.memory_topic_repository import MemoryTopicRepository
from .combined_topic_repository import CombinedTopicRepository
from tussle.general.testing.test_case_base import TussleTestCaseBase
from tussle.debate.components.topic import Topic
import pkg_resources


class CombinedTopicRepositoryTest(TopicRepositoryTestBase, TussleTestCaseBase):
    def create_topic_repository(self):
        self.primary = MemoryTopicRepository()
        self.fallback1 = MemoryTopicRepository()
        self.fallback2 = MemoryTopicRepository()

        return CombinedTopicRepository(
            primary_repository=self.primary,
            fallback_repositories=[
                self.fallback1,
                self.fallback2,
            ]
        )

    def test_load_fallback(self):
        """
        This code checks that we are able to load a topic from the list of test fixtures.
        :return:
        """

        data_str = pkg_resources.resource_string("tussle", f"topics/test_fixtures/test_topic_1.json").decode("utf-8")
        topic = Topic.from_json(data_str)
        topic.id = "new_test_id"

        # Check that we can't load the topic initially
        loaded_topic = self.repository.get_by_id("new_test_id")
        self.assertIsNone(loaded_topic)

        # Save the topic into the fallback repository.
        self.fallback1.save(topic)

        # Now try to load it from the combined repository.
        loaded_topic = self.repository.get_by_id("new_test_id")

        self.assertIsNotNone(topic)
        self.assertEqual(loaded_topic, topic)

    def test_load_second_fallback(self):
        """
        This code checks that if you have multiple fallbacks, you can still load data from the second fallbacks.
        :return:
        """

        data_str = pkg_resources.resource_string("tussle", f"topics/test_fixtures/test_topic_1.json").decode("utf-8")
        topic = Topic.from_json(data_str)
        topic.id = "new_test_id"

        # Check that we can't load the topic initially
        loaded_topic = self.repository.get_by_id("new_test_id")
        self.assertIsNone(loaded_topic)

        # Save the topic into the second fallback repository.
        self.fallback2.save(topic)

        # Now try to load it from the combined repository.
        loaded_topic = self.repository.get_by_id("new_test_id")

        self.assertIsNotNone(topic)
        self.assertEqual(loaded_topic, topic)
