from tussle.debate.data_repository.answer_repository_base import AnswerRepositoryBase
from tussle.debate.components.answer import Answer
from tussle.general.db_models.custom_id_field import CustomIDField


class MongoAnswerRepository(AnswerRepositoryBase):
    """
    This is a repository for answers which stores them in MongoDB.
    """
    def __init__(self, mongo_db_connection):
        self.mongo_db_connection = mongo_db_connection
        self.collection = self.mongo_db_connection['answers']
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

    def create(self, answer: Answer):
        """
        Creates a brand new answer
        """
        if answer.id is None:
            answer.id = CustomIDField.generate_id("Answer", answer.owner)

        self.collection.insert_one(answer.to_dict())

        return answer


    def get_by_id(self, answer_id: str):
        """
        Gets a bulk chart evaluation by its ID.
        """
        result = self.collection.find_one({'_id': answer_id})
        if result is None:
            return None

        return Answer.from_dict(result)

    def get_by_slug(self, slug: str) -> (Answer | None):
        """
        Gets an answer by its slug.
        """
        result = self.collection.find_one({'slug': slug})
        if result is None:
            return None

        return Answer.from_dict(result)

    def get_all_by_owner(self, owner: str):
        """
        Fetches all the answers created for the given owner.
        """
        return [Answer.from_dict(result) for result in self.collection.find({'owner': owner})]

    def get_all(self):
        """
        Fetches all the answers in the system.
        """
        return [Answer.from_dict(result) for result in self.collection.find()]

    def get_all_published(self):
        """
        Fetches all the published answers found in the system.
        """
        return [Answer.from_dict(result) for result in self.collection.find({'published': True})]

    def delete_by_id(self, answer_id: str):
        """
        Deletes a bulk chart evaluation by its ID.
        """
        self.collection.delete_one({'_id': answer_id})

    def save(self, answer: Answer):
        """
        Saves the given bulk chart evaluation json data.
        """
        self.collection.update_one({'_id': answer.id}, {'$set': answer.to_dict()})

    def delete_all(self):
        """
        Deletes all the bulk chart evaluations.
        """
        self.collection.delete_many({})


