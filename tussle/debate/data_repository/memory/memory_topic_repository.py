from tussle.debate.data_repository.topic_repository_base import TopicRepositoryBase
from tussle.debate.components.topic import Topic


class MemoryTopicRepository(TopicRepositoryBase):
    """
    This is a simple repository for topics which just store them in memory.

    Chiefly useful for testing.
    """

    def __init__(self):
        self.id_counter = 0
        self.topics = {}

    def create(self, topic: Topic):
        """
        Creates a brand new topic object.

        This function will assign the 'id' field if it hasn't been assigned yet.

        :return: The topic object with the 'id' field assigned.
        """
        if topic.id is None:
            topic.id = f"topic-{self.id_counter}"
        self.id_counter += 1

        self.topics[topic.id] = topic
        return topic

    def get_by_id(self, topic_id: str):
        """
        Gets a topic by its ID.
        """
        return self.topics.get(topic_id)

    def get_by_slug(self, slug: str) -> (Topic | None):
        """
        Gets an topic by its slug.
        """
        for topic in self.topics.values():
            if topic.slug == slug:
                return topic
        return None

    def get_all_by_owner(self, owner: str):
        """
        Fetches all the topics created for the given owner.
        """
        return [topic for topic in self.topics.values() if topic.owner == owner]

    def get_all(self):
        """
        Fetches all the topics in the system.
        """
        return [topic for topic in self.topics.values()]

    def get_all_published(self):
        """
        Fetches all the published topics found in the system.
        """
        return [topic for topic in self.topics.values() if topic.published]

    def delete_by_id(self, topic_id: str):
        """
        Deletes a topic by its ID.
        """
        del self.topics[topic_id]

    def save(self, topic: Topic):
        """
        Saves the given topic.
        """
        self.topics[topic.id] = topic

    def delete_all(self):
        """
        Deletes all the topics.
        """
        self.topics = {}
