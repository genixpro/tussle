from .magic_string_test_prompt_completion_provider import MagicStringTestPromptCompletionProvider
from .completion_provider_test_base import CompletionProviderTestBase
import unittest


class MagicStringTestPromptCompletionProviderTest(CompletionProviderTestBase):
    provider = None

    def setUp(self):
        # Create a fresh memory cache instance for each test.
        self.provider = MagicStringTestPromptCompletionProvider()
        # This just speeds up execution speed of the tests.
        self.provider.completion_events_per_second_limit = None

    def tearDown(self):
        pass

    test_prompt = "this is a testing prompt, used in unit tests and integrations."
    test_temp = 0.5
    test_randomized_value = 0.5

    def test_completion_no_magic_string(self):
        """
        This tests that the provider will return None if the magic string is not
        found in the prompt.
        :return:
        """
        result = self.get_completion_for_test_prompt()

        self.assertIsNone(result)

    def test_completion_with_magic_string(self):
        """
        This tests that the provider will return a completion if the magic
        string is found within the prompt
        """
        test_prompt = self.test_prompt + " " + self.provider.magic_strings[0]

        # Check that a completion is now provided, when the test prompt is used
        result = self.get_completion_for_test_prompt(prompt=test_prompt)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

        # Check that we have more than 4 words in the result.
        self.assertGreater(len(result.split(" ")), 4)

    def test_completion_with_magic_string_at_beginning(self):
        """
        This tests that the provider will return a completion if the magic
        string is found at the beginning of a prompt
        """
        test_prompt = self.provider.magic_strings[0] + " " + self.test_prompt

        # Check that a completion is now provided, when the test prompt is used
        result = self.get_completion_for_test_prompt(prompt=test_prompt)

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
        test_prompt = self.provider.magic_strings[0] + " generate me a title"

        # Check that a completion is now provided, when the test prompt is used
        result = self.get_completion_for_test_prompt(prompt=test_prompt)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

        # Check that we have only 2 words in the result
        self.assertEqual(len(result.split(" ")), 2)

    def test_event_listener_events(self):
        test_prompt = self.test_prompt + " " + self.provider.magic_strings[0]

        self.run_event_listener_test(
            provider=self.provider,
            test_prompt=test_prompt,
            test_temp=self.test_temp,
            test_randomized_value=self.test_randomized_value
        )

    def test_event_listener_stream_words_false(self):
        test_prompt = self.test_prompt + " " + self.provider.magic_strings[0]

        self.run_event_listener_stream_words_false(
            provider=self.provider,
            test_prompt=test_prompt,
            test_temp=self.test_temp,
            test_randomized_value=self.test_randomized_value
        )

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


if __name__ == '__main__':
    unittest.main()
