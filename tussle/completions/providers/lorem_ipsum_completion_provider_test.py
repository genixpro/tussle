from .lorem_ipsum_completion_provider import LoremIpsumCompletionProvider
from .completion_provider_test_base import CompletionProviderTestBase
import unittest


class LoremIpsumCompletionProviderTest(CompletionProviderTestBase):
    provider = None

    def setUp(self):
        # Create a fresh provider for each test
        self.provider = LoremIpsumCompletionProvider()
        # This just speeds up execution speed of the tests.
        self.provider.completion_events_per_second_limit = None

    def tearDown(self):
        pass

    test_prompt = "this is a testing prompt, used in unit tests and integrations."
    test_temp = 0.5
    test_randomized_value = 0.5

    def test_completion(self):
        """
        This tests that the provider will return a lorem ipsum completion
        """
        result = self.get_completion_for_test_prompt()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

        # Check that we have more than 4 words in the result.
        self.assertGreater(len(result.split(" ")), 4)

    def test_completion_with_title_in_prompt(self):
        """
        This tests that the provider will return a shorter completion
        if it finds the word 'title' in the prompt. This is purely
        for testing purposes, so that we get reasonable completions
        on prompts used for generating titles.
        """
        test_prompt = "generate me a title"

        # Check that a completion is now provided, when the test prompt is used
        result = self.get_completion_for_test_prompt(prompt=test_prompt)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

        # Check that we have only 2 words in the result
        self.assertEqual(len(result.split(" ")), 2)

    def get_completion_for_test_prompt(self, **kwargs):
        values = {
            "prompt": self.test_prompt,
            "temperature": self.test_temp,
            "event_listener": None,
            "metadata": None,
            "randomized_value": self.test_randomized_value,
        }

        values.update(kwargs)

        return self.provider.get_completion(**values)

    def test_event_listener_events(self):
        self.run_event_listener_test(
            provider=self.provider,
            test_prompt=self.test_prompt,
            test_temp=self.test_temp,
            test_randomized_value=self.test_randomized_value
        )

    def test_event_listener_stream_words_false(self):
        self.run_event_listener_stream_words_false(
            provider=self.provider,
            test_prompt=self.test_prompt,
            test_temp=self.test_temp,
            test_randomized_value=self.test_randomized_value
        )


if __name__ == '__main__':
    unittest.main()
