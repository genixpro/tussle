from .manual_event_streaming_completion_provider import ManualEventStreamingCompletionProvider
from ..utils import completion_utils
import datetime


class DbCacheCompletionProvider(ManualEventStreamingCompletionProvider):
    """
    This class provides completions from a database cache.
    """

    def __init__(self, mongo_db_connection):
        """
        This initializes the provider.
        """
        super().__init__()
        self.mongo_db_connection = mongo_db_connection
        if mongo_db_connection is None:
            raise ValueError("mongo_db_connection must be set")

        self.collection = self.mongo_db_connection['cached_completions']
        self.create_indexes()

    def create_indexes(self):
        """
        This method is responsible for ensuring any indexes that are required
        to perform queries are created.
        """
        # Create an index used to lookup cached completion
        self.collection.create_index(('random_index', 'prompt_hash', 'temperature', 'result'))

        # Create an index on created_at to automatically delete completions if they get too old
        self.collection.create_index(('created_at',), expireAfterSeconds=60 * 60 * 24 * 30)

    def get_completion_internal(self, prompt, temperature, randomized_value):
        """
        This function is meant to be implemented by sub-classes. It should return the text
        tha twill be broken up and fed out inside the completion.

        :param prompt:
        :param temperature:
        :param randomized_value:
        :return:
        """

        # compute the hash in base64
        prompt_hash = completion_utils.compute_hash_for_prompt(prompt)

        random_index = completion_utils.compute_random_completion_index_from_randomized_value(randomized_value, temperature)

        # Look up just the result field from the database. This can be done very
        # efficiently with just the mongo index, known as a covered query
        completion = self.collection.find_one({
            'prompt_hash': prompt_hash,
            'random_index': random_index,
            'temperature': temperature,
        }, projection=['result'])

        if completion is None:
            return None
        else:
            return completion['result']

    def save_completion(self, prompt, temperature, randomized_value, result):
        prompt_hash = completion_utils.compute_hash_for_prompt(prompt)
        random_index = completion_utils.compute_random_completion_index_from_randomized_value(randomized_value, temperature)
        created_at = datetime.datetime.now()

        query = {
            'prompt_hash': prompt_hash,
            'random_index': random_index,
            'temperature': temperature,
        }

        new_completion = {
            'prompt_hash': prompt_hash,
            'prompt': prompt,
            'random_index': random_index,
            'temperature': temperature,
            'result': result,
            'created_at': created_at
        }

        self.collection.update_one(query, {"$set": new_completion}, upsert=True)

    def clear_completion_cache(self):
        """
        This method clears the completion cache.
        """
        self.collection.delete_many({})


