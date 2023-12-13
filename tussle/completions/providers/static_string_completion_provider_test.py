from .static_string_completion_provider import StaticStringCompletionProvider
from .completion_provider_test_base import CompletionProviderTestBase
import unittest


class StaticStringCompletionProviderTest(CompletionProviderTestBase):
    provider = None

    def setUp(self):
        # Create a fresh static string completion provider instance for each test.
        self.provider = StaticStringCompletionProvider(None)

        # This just speeds up execution speed of the tests.
        self.provider.completion_events_per_second_limit = None

    def tearDown(self):
        pass

    test_prompt = "this is a testing prompt, used in unit tests and integrations."
    test_temp = 0.5
    test_randomized_value = 0.5

    def test_completion_static_result(self):
        """
        This tests that the provider always returns whatever its static result is
        set to.
        :return:
        """
        test_result = "This is a testing prompt result"
        # Tack on a short random number for good measure, to ensure
        # the match isn't a fluke.
        test_result += " " + str(self.test_randomized_value)

        self.provider.static_result = test_result
        result = self.get_completion_for_test_prompt()
        self.assertIsNotNone(result)
        self.assertEqual(result, test_result)

    def test_completion_static_result_none(self):
        """
        This tests that you can hard code the static result to None
        :return:
        """
        self.provider.static_result = None
        result = self.get_completion_for_test_prompt()
        self.assertIsNone(result)

    def test_save_completion(self):
        """
        This tests that you can call a function save_completion() on the provider.
        It doesn't have to actually do anything, it just serves as a placeholder
        for the function so that the StaticStringCompletionProvider can be used
        as a drop in replacement for other completion providers that do have a
        save_completion function.

        :return:
        """
        # Don't need to assert anything, just checking it doesn't crash.
        self.provider.save_completion(
            prompt=self.test_prompt,
            temperature=self.test_temp,
            randomized_value=self.test_randomized_value,
            result="test result"
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
