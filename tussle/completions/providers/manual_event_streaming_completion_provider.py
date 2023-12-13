from .completion_provider_base import CompletionProviderBase
from tussle.completions.event_listeners.completion_event import CompletionEvent
from tussle.completions.event_listeners.completion_event import CompletionEventTypes
import datetime
import time
import random


class ManualEventStreamingCompletionProvider(CompletionProviderBase):
    """
    This class provides a base class completion providers that use alternative
    mechanisms to provide the completion. This class handles breaking apart
    that completion text and streaming it out to the client using events.
    """

    def __init__(self):
        """
        This initializes the provider.
        """
        super().__init__()

        self.completion_events_per_second_limit = 75.0

    def get_completion(self, prompt, temperature, event_listener=None, metadata=None, randomized_value=None, stream_words=True):
        if metadata is None:
            metadata = {}

        if randomized_value is None:
            # randomized_value = random.uniform(0, 1)
            randomized_value = 0

        completion_result = self.get_completion_internal(prompt, temperature, randomized_value)

        if completion_result is None:
            # Just return the null result directly. We don't need to create a bunch of fake events
            # for this.
            return None

        # Quickly stream out all the words in the cached completion at a fast speed.
        # This helps to ensure that there is consistent behavior regardless of whether
        # the completion is cached or not.
        target_time = datetime.datetime.now()
        if event_listener is not None:
            # Send the start event
            start = CompletionEvent(event=CompletionEventTypes.start_node_value_event, word=None, **metadata)
            event_listener(start)

            if stream_words:
                for wordIndex, word in enumerate(completion_result.split(' ')):
                    if wordIndex > 0:
                        word = ' ' + word

                    next_word_event = CompletionEvent(event=CompletionEventTypes.word_event, word=word, **metadata)
                    event_listener(next_word_event)

                    if self.completion_events_per_second_limit is not None:
                        # Sleep the clock if needed so that we match the rate that we are streaming
                        # words with the target rate
                        now_time = datetime.datetime.now()
                        target_time += datetime.timedelta(seconds=1.0 / self.completion_events_per_second_limit)
                        if now_time < target_time:
                            time.sleep((target_time - now_time).total_seconds())

            # Send the finish event
            finish_event = CompletionEvent(event=CompletionEventTypes.finish_node_value_event, word=completion_result, **metadata)
            event_listener(finish_event)

        return completion_result

    def get_completion_internal(self, prompt, temperature, randomized_value):
        """
        This function is meant to be implemented by sub-classes. It should return the text
        tha twill be broken up and fed out inside the completion.

        :param prompt:
        :param temperature:
        :param randomized_value:
        :return:
        """
        raise NotImplementedError("get_completion_internal is not implemented - this is an abstract base class")
