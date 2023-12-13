from .completion_provider_base import CompletionProviderBase
from tussle.completions.event_listeners.completion_event import CompletionEvent, CompletionEventTypes


class OpenAICompletionProvider(CompletionProviderBase):
    """
    This class provides completions using the OpenAI API
    """

    def __init__(self, openai_integration):
        """
        This initializes the provider with the given openai integration class.
        """
        super().__init__()

        self.openai_integration = openai_integration
        self.max_completion_length = 1000

    def get_completion(self, prompt, temperature, event_listener=None, metadata=None, randomized_value=None, stream_words=True):
        if metadata is None:
            metadata = {}

        # Randomized value is ignored here. Anytime we go to the openai API, we are getting a freshly
        # generated completion.

        stream_from_openai = (event_listener is not None and stream_words)

        if event_listener is not None:
            start = CompletionEvent(event=CompletionEventTypes.start_node_value_event, word=None, **metadata)
            event_listener(start)

        # Fetch a completion from openai and save it to the database
        response = self.openai_integration.completion_with_retry(
            model="gpt-3.5-turbo",
            # model="gpt-4-1106-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            stream=stream_from_openai,
            max_tokens=self.max_completion_length,
        )

        if stream_from_openai:
            # create variables to collect the stream of chunks
            collected_words = []

            # iterate through the stream of events
            for chunk in response:
                chunk_message = chunk.choices[0].delta  # extract the message
                chunk_word = chunk_message.content  # extract the word
                # Only append the word to our collected words if it is not empty
                if chunk_word:
                    collected_words.append(chunk_word)  # save the message
                    if event_listener is not None:
                        next_word_event = CompletionEvent(event=CompletionEventTypes.word_event, word=chunk_word, **metadata)
                        event_listener(next_word_event)

            full_reply_content = ''.join(collected_words)
        else:
            full_reply_content = response.choices[0].message.content

        if event_listener is not None:
            finish_event = CompletionEvent(event=CompletionEventTypes.finish_node_value_event, word=full_reply_content, **metadata)
            event_listener(finish_event)

        return full_reply_content
