from .manual_event_streaming_completion_provider import ManualEventStreamingCompletionProvider
import lorem


class LoremIpsumCompletionProvider(ManualEventStreamingCompletionProvider):
    """
    This class provides completions by generating a lorem ipsum paragraph. It will always
    generate a lipsum response regardless of what prompt is given to it.
    """

    def __init__(self):
        """
        This initializes the provider.
        """
        super().__init__()

    def get_completion_internal(self, prompt, temperature, randomized_value):
        """
        This generates a lorem-ipsum paragraph as the response. The input prompt and temperature
        are completely ignored.

        :param prompt:
        :param temperature:
        :param randomized_value:
        :return:
        """
        prompt_lower = prompt.lower()

        if 'title' in prompt_lower:
            result = " ".join(lorem.sentence().split()[0:2])
        else:
            result = lorem.paragraph()

        return result
