from tussle.debate.data_repository.memory.memory_topic_repository import MemoryTopicRepository
from tussle.debate.components.topic import Topic
import pkg_resources

class FixtureTopicRepository(MemoryTopicRepository):
    """
    This is a simple repository for bulk chart evaluations which just store them in memory.

    Chiefly useful for testing.
    """

    def get_by_id(self, topic_id: str):
        """
        Gets a topic by its ID. Will try loading from memory first,
        and if that fails, loads from the test fixture files
        """
        # First attempt to get it from the super class, the memory repository.
        topic = super().get_by_id(topic_id)
        if topic:
            return topic

        # Now attempt to load it from a fixture file.
        topic = self._load_from_fixture(topic_id)

        return topic

    def _load_from_fixture(self, id):
        try:
            data_str = pkg_resources.resource_string("tussle", f"topics/test_fixtures/{id}.json").decode("utf-8")
        except FileNotFoundError:
            return None

            data_str = pkg_resources.resource_string("tussle", f"topics/test_fixtures/{id}.json").decode("utf-8")
        obj = Topic.from_json(data_str)
        return obj
