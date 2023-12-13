from tussle.debate.components.topic import Topic
import abc


class TopicRepositoryBase(metaclass=abc.ABCMeta):
    """
    This is a base class for a data repository that stores topics.
    It acts as a go-between for the API and the database or another data layer.

    This class just defines the interface and doesn't actually implement anything.
    """

    def create(self, topic: Topic) -> Topic:
        """
        Creates a brand new topic object.

        This function should assign the 'id' field to the topic.
        :return: The topic object with the 'id' field assigned.
        """
        raise NotImplementedError('TopicRepositoryBase.create not implemented')

    def get_by_id(self, topic_id: str) -> (Topic | None):
        """
        Gets a topic by its ID.
        """
        raise NotImplementedError('TopicRepositoryBase.get_by_id not implemented')

    def get_by_slug(self, slug: str) -> (Topic | None):
        """
        Gets a topic by its slug.
        """
        raise NotImplementedError('TopicRepositoryBase.slug not implemented')

    def get_all_by_owner(self, owner: str):
        """
        Fetches all the topics created for the given owner.
        """
        raise NotImplementedError('TopicRepositoryBase.get_all_by_owner not implemented')

    def get_all(self):
        """
        Fetches all the topics in the system.
        """
        raise NotImplementedError('TopicRepositoryBase.get_all not implemented')

    def get_all_published(self):
        """
        Fetches all the published topics found in the system.
        """
        raise NotImplementedError('TopicRepositoryBase.get_all_published not implemented')

    def delete_by_id(self, topic_id: str):
        """
        Deletes a topic by its ID.
        """
        raise NotImplementedError('TopicRepositoryBase.delete_by_id not implemented')

    def save(self, topic: Topic):
        """
        Saves the given topic.
        """
        raise NotImplementedError('TopicRepositoryBase.save not implemented')

    def delete_all(self):
        """
        Deletes all the topics.
        """
        raise NotImplementedError('TopicRepositoryBase.save not implemented')


