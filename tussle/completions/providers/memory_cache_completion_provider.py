from tussle.completions.utils import completion_utils
from tussle.completions.providers.manual_event_streaming_completion_provider import ManualEventStreamingCompletionProvider
from cachetools import TTLCache


class MemoryCacheCompletionProvider(ManualEventStreamingCompletionProvider):
    """
    This class provides completions from a small in-memory cache. This ensures
    really popular completions don't end up making db calls
    """

    def __init__(self):
        """
        This initializes the provider.
        """
        super().__init__()

        # Create the local completion cache with expiring entries. This is used to cache a small
        # number of popular completions, so that we can serve them quickly without having to
        # hit the database or openai API.
        self.local_completion_cache = TTLCache(maxsize=1024 * 4, ttl=60 * 60 * 24)

    def get_completion_internal(self, prompt, temperature, randomized_value):
        """
        This function is meant to be implemented by sub-classes. It should return the text
        tha twill be broken up and fed out inside the completion.

        :param prompt:
        :param temperature:
        :param randomized_value:
        :return:
        """

        cache_key = self._compute_local_cache_key(prompt, temperature, randomized_value)

        try:
            completion = self.local_completion_cache[cache_key]

            if completion is None:
                return None
            else:
                return completion
        except KeyError as e:
            return None

    def save_completion(self, prompt, temperature, randomized_value, result):
        cache_key = self._compute_local_cache_key(prompt, temperature, randomized_value)
        self.local_completion_cache[cache_key] = result

    def _compute_local_cache_key(self, prompt, temperature, randomized_value):
        random_index = completion_utils.compute_random_completion_index_from_randomized_value(randomized_value, temperature)

        return (completion_utils.compute_hash_for_prompt(prompt), temperature, random_index)

