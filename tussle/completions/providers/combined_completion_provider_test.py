from .completion_provider_test_base import CompletionProviderTestBase
from .combined_completion_provider import CombinedCompletionProvider
import unittest
from .static_string_completion_provider import StaticStringCompletionProvider
from flexmock import flexmock

class CombinedCompletionProviderTest(CompletionProviderTestBase):
    container = None

    def setUp(self):
        self.magic_string_provider = flexmock(StaticStringCompletionProvider("magic string"))
        self.memory_cache_provider = flexmock(StaticStringCompletionProvider("memory cache"))
        self.db_cache_provider = flexmock(StaticStringCompletionProvider("db cache"))
        self.openai_provider = flexmock(StaticStringCompletionProvider("openai"))

        self.provider = CombinedCompletionProvider(
            magic_string_provider=self.magic_string_provider,
            memory_cache_provider=self.memory_cache_provider,
            db_cache_provider=self.db_cache_provider,
            openai_provider=self.openai_provider,
        )

    def tearDown(self):
        pass

    test_prompt = "this is a testing prompt, used in unit tests and integrations."
    test_temp = 0.5
    test_randomized_value = 0.5

    def test_completion_order_first_magic_string(self):
        """
        This tests that the provider always starts with magic string completions
        if available.
        :return:
        """

        self.magic_string_provider.should_call("get_completion").once()
        self.memory_cache_provider.should_call("get_completion").never()
        self.db_cache_provider.should_call("get_completion").never()
        self.openai_provider.should_call("get_completion").never()

        # Fetch the completion
        result = self.get_completion_for_test_prompt()

        # It should try to get the completion from the magic string provider first
        self.assertIsNotNone(result)
        self.assertEqual(result, "magic string")


    def test_completion_order_second_memory_cache(self):
        """
        This tests that the provider goes to the memory cache if a magic
        string completion isn't available.

        :return:
        """

        self.magic_string_provider.should_call("get_completion").once()
        self.memory_cache_provider.should_call("get_completion").once()
        self.db_cache_provider.should_call("get_completion").never()
        self.openai_provider.should_call("get_completion").never()

        # Disable the magic string provider so that it falls back to the memory cache
        self.magic_string_provider.static_result = None

        # Now if magic string doesn't return a result (e.g. we hard code its result to None),
        # then it should next try the memory cache provider
        result = self.get_completion_for_test_prompt()
        self.assertIsNotNone(result)
        self.assertEqual(result, "memory cache")


    def test_completion_order_third_db_cache(self):
        """
        This tests that the provider goes to the db cache if the memory
        cache didn't return a completion.

        :return:
        """

        self.magic_string_provider.should_call("get_completion").once()
        self.memory_cache_provider.should_call("get_completion").once()
        self.db_cache_provider.should_call("get_completion").once()
        self.openai_provider.should_call("get_completion").never()

        # Set first two providers to return None
        self.magic_string_provider.static_result = None
        self.memory_cache_provider.static_result = None

        # It should return the result from the db cache
        result = self.get_completion_for_test_prompt()
        self.assertIsNotNone(result)
        self.assertEqual(result, "db cache")


    def test_completion_order_fourth_openai(self):
        """
        This tests that the provider goes to openai if the other three
        providers didn't return a completion.

        :return:
        """

        self.magic_string_provider.should_call("get_completion").once()
        self.memory_cache_provider.should_call("get_completion").once()
        self.db_cache_provider.should_call("get_completion").once()
        self.openai_provider.should_call("get_completion").once()

        # Set the first three providers to return None
        self.magic_string_provider.static_result = None
        self.memory_cache_provider.static_result = None
        self.db_cache_provider.static_result = None

        # Finally, if the db provider doesn't return a result,
        # it should try the openai provider
        result = self.get_completion_for_test_prompt()
        self.assertIsNotNone(result)
        self.assertEqual(result, "openai")

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
