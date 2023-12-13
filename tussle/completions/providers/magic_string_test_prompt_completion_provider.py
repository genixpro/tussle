from .manual_event_streaming_completion_provider import ManualEventStreamingCompletionProvider
import lorem


class MagicStringTestPromptCompletionProvider(ManualEventStreamingCompletionProvider):
    """
    This class provides completions that are used in testing. It does so by looking
    for very specific magic strings within the prompt, and if one of those strings
    matches, it will return a lorem-ipsum.

    This allows us to run tests in production that don't hit the openai API.
    """
    magic_strings = [
        "test_prompt_value_NodFabDaic9Ot"
    ]

    def __init__(self):
        """
        This initializes the provider.
        """
        super().__init__()

    def get_completion_internal(self, prompt, temperature, randomized_value):
        """
        This checks to see if the given prompt has one of the defined magic strings. If it does,
        it will return the completion text for it. If the prompt doesn't match any of the predefined
        testing prompts, it will return None

        :param prompt:
        :param temperature:
        :param randomized_value:
        :return:
        """

        prompt_lower = prompt.lower()

        for check_value in self.magic_strings:
            if check_value in prompt:
                if 'title' in prompt_lower:
                    result = " ".join(lorem.sentence().split()[0:2])
                else:
                    result = lorem.paragraph()

                # We don't save the test completions since they are hard coded.
                return result

        return None
