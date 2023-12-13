from abc import abstractmethod, ABCMeta

class CompletionProviderBase(metaclass=ABCMeta):
    """
    This is the base class for all the services that are able to provide LLM completions.
    This is our bridge over to services like OpenAI
    """

    @abstractmethod
    def get_completion(self, prompt, temperature, event_listener=None, metadata=None, randomized_value=None, stream_words=True):
        """
        This function is responsible for getting a completion using whatever strategy
        is implemented by the subclass.

        If a queue is provided, then it should send events to the given SSE event listener
        as it gets the completion. The queues are themselves subclasses of CompletionEventQueueBase.

        If stream_words is set to True (and an event listener is provided), then the provider should
        send an individual event for each word in the completion as its generated. This is useful
        for streaming the completion. Otherwise, just the start and end events are sent to the
        listener. Turning stream_words to False though can improve performance of getting the
        result.

        It should send a start event when it starts the completion, a word event for each word
        and a finish event when it finishes the completion.

        The randomized_value should be a value between 0 and 1 which is used to determine
        which completion to use when there are multiple completions available.

        The event should get send with the given optional metadata, which is a dictionary
        containing

        :return: A new string containing the text of the completion.
        """
        raise NotImplementedError("get_completion is not implemented - this is an abstract base class")
