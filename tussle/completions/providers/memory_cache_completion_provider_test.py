from .memory_cache_completion_provider import MemoryCacheCompletionProvider
from .completion_provider_test_base import CompletionProviderTestBase
import unittest


class MemoryCacheCompletionProviderTest(CompletionProviderTestBase):
    provider = None

    def setUp(self):
        # Create a fresh memory cache instance for each test.
        self.provider = MemoryCacheCompletionProvider()
        # This just speeds up execution speed of the tests.
        self.provider.completion_events_per_second_limit = None

    def tearDown(self):
        pass

    test_prompt = "this is a testing prompt, used in unit tests and integrations."
    test_temp = 0.5
    test_randomized_value = 0.5
    test_result = "This is a testing prompt result"

    def test_completion_not_in_cache(self):
        """
        This tests that the provider will return None if the completion is not in the cache
        :return:
        """
        result = self.get_completion_for_test_prompt()

        self.assertIsNone(result)
        self.assertNotEquals(result, self.test_result)

    def test_completion_in_cache(self):
        """
        This tests that the provider will return None if the completion is not in the cache
        :return:
        """
        self.save_test_completion_to_memory_cache()

        # Check that the completion is in the cache
        result = self.get_completion_for_test_prompt()

        self.assertIsNotNone(result)
        self.assertEqual(result, self.test_result)

    def test_completion_different_temperatures(self):
        """
        This test checks that if you use a different value for temperature,
        but everything else is the same, it will look for a different value
        in the cache.
        :return:
        """
        self.save_test_completion_to_memory_cache()

        result = self.get_completion_for_test_prompt(temperature=self.test_temp + 0.5)

        # Since the temperature is different, the result should be none
        self.assertIsNone(result)
        self.assertNotEquals(result, self.test_result)

    def test_completion_different_randomized_value(self):
        """
        This test checks that if you use a different randomized_value,
        but everything else is the same, it will look for a different value
        in the cache.
        :return:
        """
        self.save_test_completion_to_memory_cache()

        result = self.get_completion_for_test_prompt(randomized_value=self.test_randomized_value + 0.2)

        # Since the temperature is different, the result should be none
        self.assertIsNone(result)
        self.assertNotEquals(result, self.test_result)

    def test_completion_different_prompt(self):
        """
        This test checks that if you use a different prompt value, you get a
        different completion.

        :return:
        """
        self.save_test_completion_to_memory_cache()

        result = self.get_completion_for_test_prompt(prompt=self.test_prompt + " extra text")

        # Since the temperature is different, the result should be none
        self.assertIsNone(result)
        self.assertNotEquals(result, self.test_result)

    def test_event_listener_events(self):
        self.save_test_completion_to_memory_cache()

        self.run_event_listener_test(
            provider=self.provider,
            test_prompt=self.test_prompt,
            test_temp=self.test_temp,
            test_randomized_value=self.test_randomized_value
        )

    def test_event_listener_stream_words_false(self):
        self.save_test_completion_to_memory_cache()

        self.run_event_listener_stream_words_false(
            provider=self.provider,
            test_prompt=self.test_prompt,
            test_temp=self.test_temp,
            test_randomized_value=self.test_randomized_value
        )

    def save_test_completion_to_memory_cache(self):
        self.provider.save_completion(
            prompt=self.test_prompt,
            temperature=self.test_temp,
            randomized_value=self.test_randomized_value,
            result=self.test_result
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
