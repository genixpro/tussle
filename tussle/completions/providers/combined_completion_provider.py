from .completion_provider_base import CompletionProviderBase
import random


class CombinedCompletionProvider(CompletionProviderBase):
    """
    This class combines several other Completion providers, including the cache
    completion providers, to put together a full logic for getting a completion.

    """

    def __init__(self, memory_cache_provider, db_cache_provider, magic_string_provider, openai_provider):
        """
        This initializes the provider.
        """
        super().__init__()

        self.db_cache_provider = db_cache_provider
        self.memory_cache_provider = memory_cache_provider
        self.openai_provider = openai_provider
        self.magic_string_provider = magic_string_provider

    def get_completion(self, prompt, temperature, event_listener=None, metadata=None, randomized_value=None, stream_words=True):
        if metadata is None:
            metadata = {}

        if randomized_value is None:
            # randomized_value = random.uniform(0, 1)
            randomized_value = 0

        # First lets check the magic string provider
        completion_result = self.magic_string_provider.get_completion(prompt, temperature, event_listener, metadata, randomized_value, stream_words)
        if completion_result is not None:
            return completion_result

        # Now lets see if the prompt has been stored in the local memory cache.
        # If so, serve that.
        completion_result = self.memory_cache_provider.get_completion(prompt, temperature, event_listener, metadata, randomized_value, stream_words)
        if completion_result is not None:
            return completion_result

        # Next check the db cache provider
        completion_result = self.db_cache_provider.get_completion(prompt, temperature, event_listener, metadata, randomized_value, stream_words)
        if completion_result is not None:
            # Store the completion result from the db in our local memory cache.
            # This will help us to serve it faster next time.
            self.memory_cache_provider.save_completion(
                prompt=prompt,
                temperature=temperature,
                randomized_value=randomized_value,
                result=completion_result
            )

            return completion_result

        # So it wasn't in any of the caches. Let's go to the openai API
        completion_result = self.openai_provider.get_completion(prompt, temperature, event_listener, metadata, randomized_value, stream_words)
        if completion_result is not None:
            # Record the completion result into the local db completion cache.
            # This will help us to serve it faster next time.
            self.db_cache_provider.save_completion(
                prompt=prompt,
                temperature=temperature,
                randomized_value=randomized_value,
                result=completion_result
            )

            return completion_result

        raise RuntimeError("Unable to get a completion from any of the completion providers.")

