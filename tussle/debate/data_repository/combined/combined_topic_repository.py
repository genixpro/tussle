from tussle.debate.data_repository.memory.memory_topic_repository import MemoryTopicRepository
from tussle.debate.components.topic import Topic
from tussle.debate.data_repository.topic_repository_base import TopicRepositoryBase
import pkg_resources


class CombinedTopicRepository(TopicRepositoryBase):
    """
    This is a data repository that combines together other data repositories.
    It has a main repository which is where data is saved and loaded from.
    But it has a secondary function where it will load things from the
    fallback repositories if it can.
    """

    def __init__(self, primary_repository: TopicRepositoryBase, fallback_repositories: list[TopicRepositoryBase]):
        self.primary_repository = primary_repository
        self.fallback_repositories = fallback_repositories

    def get_by_id(self, topic_id: str):
        """
        Gets a topic by its ID. Will try loading from memory first,
        and if that fails, loads from the test fixture files
        """
        # First attempt to get it from the primary repository.
        topic = self.primary_repository.get_by_id(topic_id)
        if topic:
            return topic

        # Now attempt to find it in the fallback repositories.
        for fallback_repository in self.fallback_repositories:
            topic = fallback_repository.get_by_id(topic_id)
            if topic:
                # Save it into the primary repository
                self.primary_repository.save(topic)
                return topic

        return None

    def get_by_slug(self, slug: str) -> (Topic | None):
        """
        Gets an topic by its slug.
        """
        # First attempt to get it from the primary repository.
        topic = self.primary_repository.get_by_slug(slug)
        if topic:
            return topic

        # Now attempt to find it in the fallback repositories.
        for fallback_repository in self.fallback_repositories:
            topic = fallback_repository.get_by_slug(slug)
            if topic:
                # Save it into the primary repository
                self.primary_repository.save(topic)
                return topic

        return None

    def create(self, topic: Topic):
        """
        Creates a brand new topic object.

        This function will assign the 'id' field if it hasn't been assigned yet.

        :return: The topic object with the 'id' field assigned.
        """
        return self.primary_repository.create(topic)

    def get_all_by_owner(self, owner: str):
        """
        Fetches all the topics created for the given owner.
        """
        return self.primary_repository.get_all_by_owner(owner)

    def get_all(self):
        """
        Fetches all the topics created for the given owner.
        """
        return self.primary_repository.get_all()

    def get_all_published(self):
        """
        Fetches all the published topics found in the system.
        """
        return self.primary_repository.get_all_published()

    def delete_by_id(self, topic_id: str):
        """
        Deletes a topic by its ID.
        """
        return self.primary_repository.delete_by_id(topic_id)

    def save(self, topic: Topic):
        """
        Saves the given topic.
        """
        return self.primary_repository.save(topic)

    def delete_all(self):
        """
        Deletes all the topics.
        """
        return self.primary_repository.delete_all()
