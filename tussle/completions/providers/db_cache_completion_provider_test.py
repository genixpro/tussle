from .db_cache_completion_provider import DbCacheCompletionProvider
from tussle.completions.providers.completion_provider_test_base import CompletionProviderTestBase
import unittest
import copy


class DbCacheCompletionProviderTest(CompletionProviderTestBase):
    provider = None

    def setUp(self):
        # Also override the config value for the number of different completions
        # to keep in the cache.
        new_config = copy.deepcopy(self.container.config())
        new_config['completion']['completion_cache_number_of_variants_per_temperature_unit'] = 10.0
        self.container.config.override(new_config)

        self.provider = DbCacheCompletionProvider(mongo_db_alias='default')
        # This just speeds up execution speed of the tests.
        self.provider.completion_events_per_second_limit = None
        # This resets the db so that we have a fresh test each time.
        self.provider.clear_completion_cache()

    def tearDown(self):
        self.container.config.reset_last_overriding()

    test_prompt = "this is a testing prompt, used in unit tests and integrations."
    test_temp = 0.5
    test_randomized_value = 0.5
    test_result = "this is a testing prompt result"

    def test_completion_not_in_db(self):
        """
        This tests that the provider will return None if the completion is not in the db
        :return:
        """
        result = self.get_completion_for_test_prompt()

        self.assertIsNone(result)
        self.assertNotEquals(result, self.test_result)

    def test_completion_in_db(self):
        """
        This tests that the provider will return the completion if it is present in the db.
        :return:
        """
        self.save_test_completion_to_db()

        # Check that the completion is in the db
        result = self.get_completion_for_test_prompt()

        self.assertIsNotNone(result)
        self.assertEqual(result, self.test_result)

    def test_completion_different_temperatures(self):
        """
        This test checks that if you use a different value for temperature,
        but everything else is the same, it will look for a different value
        in the db.
        :return:
        """
        self.save_test_completion_to_db()

        result = self.get_completion_for_test_prompt(temperature=self.test_temp + 0.5)

        # Since the temperature is different, the result should be none
        self.assertIsNone(result)
        self.assertNotEquals(result, self.test_result)

    def test_completion_different_randomized_value(self):
        """
        This test checks that if you use a different randomized_value,
        but everything else is the same, it will look for a different value
        in the db.
        :return:
        """
        self.save_test_completion_to_db()

        result = self.get_completion_for_test_prompt(randomized_value=self.test_randomized_value + 0.2)

        # Since the temperature is different, the result should be none
        self.assertIsNone(result)
        self.assertNotEquals(result, self.test_result)

    def test_completion_different_prompt(self):
        """
        This test checks that if you use a different prompt value, you get a different
        completion.

        :return:
        """
        self.save_test_completion_to_db()

        result = self.get_completion_for_test_prompt(prompt=self.test_prompt + " extra text")

        # Since the temperature is different, the result should be none
        self.assertIsNone(result)
        self.assertNotEquals(result, self.test_result)

    def test_event_listener_events(self):
        self.save_test_completion_to_db()

        self.run_event_listener_test(
            provider=self.provider,
            test_prompt=self.test_prompt,
            test_temp=self.test_temp,
            test_randomized_value=self.test_randomized_value
        )

    def test_event_listener_stream_words_false(self):
        self.save_test_completion_to_db()

        self.run_event_listener_stream_words_false(
            provider=self.provider,
            test_prompt=self.test_prompt,
            test_temp=self.test_temp,
            test_randomized_value=self.test_randomized_value
        )

    def save_test_completion_to_db(self):
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
