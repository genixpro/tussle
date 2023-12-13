from .manual_event_streaming_completion_provider import ManualEventStreamingCompletionProvider


class StaticStringCompletionProvider(ManualEventStreamingCompletionProvider):
    """
    This class provides completions by returning a static string that is provided
    to it during initialization. It always returns the same static string,
    regardless of what prompt is given to it.

    This can be useful in unit tests when we want to ensure that specific values
    are provided by the completion provider.
    """

    def __init__(self, static_result):
        """
        This initializes the provider.
        """
        super().__init__()

        self.static_result = static_result

    def get_completion_internal(self, prompt, temperature, randomized_value):
        """
        This just returns the fixed standard string. The input prompt and temperature
        are completely ignored.

        :param prompt:
        :param temperature:
        :param randomized_value:
        :return:
        """
        return self.static_result

    def save_completion(self, prompt, temperature, randomized_value, result):
        """This function is just a stub and doesn't do anything.
            It allows the StaticStringCompletionProvider to be used as a drop-in replacement
            for other completion providers that do have a save_completion function.
        """
        pass