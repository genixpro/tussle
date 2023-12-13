from tussle.debate.data_repository.topic_repository_base import TopicRepositoryBase
from tussle.debate.components.topic import Topic
from tussle.general.db_models.custom_id_field import CustomIDField


class MongoTopicRepository(TopicRepositoryBase):
    """
    This is a repository for topics which stores them in MongoDB.
    """
    def __init__(self, mongo_db_connection):
        self.mongo_db_connection = mongo_db_connection
        self.collection = self.mongo_db_connection['topics']
        self.create_indexes()

    def create_indexes(self):
        """
        This method is responsible for ensuring any indexes that are required
        to perform queries are created.
        """
        # Create an index on slug
        self.collection.create_index('slug', unique=True)

        # Create an index on published
        self.collection.create_index('published')

    def create(self, topic: Topic):
        """
        Creates a brand new topic
        """
        if topic.id is None:
            topic.id = CustomIDField.generate_id("Topic", topic.owner)

        self.collection.insert_one(topic.to_dict())

        return topic


    def get_by_id(self, topic_id: str):
        """
        Gets a bulk chart evaluation by its ID.
        """
        result = self.collection.find_one({'_id': topic_id})
        if result is None:
            return None

        return Topic.from_dict(result)

    def get_by_slug(self, slug: str) -> (Topic | None):
        """
        Gets an topic by its slug.
        """
        result = self.collection.find_one({'slug': slug})
        if result is None:
            return None

        return Topic.from_dict(result)

    def get_all_by_owner(self, owner: str):
        """
        Fetches all the topics created for the given owner.
        """
        return [Topic.from_dict(result) for result in self.collection.find({'owner': owner})]

    def get_all(self):
        """
        Fetches all the topics in the system.
        """
        return [Topic.from_dict(result) for result in self.collection.find()]

    def get_all_published(self):
        """
        Fetches all the published topics found in the system.
        """
        return [Topic.from_dict(result) for result in self.collection.find({'published': True})]

    def delete_by_id(self, topic_id: str):
        """
        Deletes a bulk chart evaluation by its ID.
        """
        self.collection.delete_one({'_id': topic_id})

    def save(self, topic: Topic):
        """
        Saves the given bulk chart evaluation json data.
        """
        self.collection.update_one({'_id': topic.id}, {'$set': topic.to_dict()})

    def delete_all(self):
        """
        Deletes all the bulk chart evaluations.
        """
        self.collection.delete_many({})


