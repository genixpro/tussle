from .manual_event_streaming_completion_provider import ManualEventStreamingCompletionProvider
from .completion_provider_test_base import CompletionProviderTestBase
from tussle.completions.event_listeners.unit_test_completion_event_listener import UnitTestCompletionEventListener
import unittest
import datetime


class TestImplementationCompletionProviderTest(ManualEventStreamingCompletionProvider):
    def __init__(self):
        super().__init__()

        self.testing_prompt_result = "this is my testing prompt result value!"

    def get_completion_internal(self, prompt, temperature, randomized_value):
        # We just ignore the parameters here
        return self.testing_prompt_result


class ManualEventStreamingCompletionProviderTest(CompletionProviderTestBase):
    provider = None

    def setUp(self):
        # Create a fresh memory cache instance for each test.
        self.provider = TestImplementationCompletionProviderTest()

        # This just speeds up execution speed of the tests.
        self.provider.completion_events_per_second_limit = None

    def tearDown(self):
        pass

    test_prompt = "this is a testing prompt, used in unit tests and integrations."
    test_temp = 0.5
    test_randomized_value = 0.5
    test_chart_id = "test_chart_id_12345"
    test_node_id = "my_node_id_456"
    test_value_index = 2

    def test_completion(self):
        """
        This tests that the provider will pass along whatever value is given
        to it by the get_completion_internal method.
        :return:
        """
        result = self.get_completion_for_test_prompt()

        self.assertIsNotNone(result)
        self.assertEquals(result, self.provider.testing_prompt_result)

    def test_pass_through_none(self):
        """
        This tests that the provider won't do anything and just passes
        through any None values that it may get from the sub-class
        :return:
        """
        self.provider.testing_prompt_result = None
        result = self.get_completion_for_test_prompt()

        self.assertIsNone(result)
        self.assertEquals(result, self.provider.testing_prompt_result)

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

    def test_pass_through_none_with_event_listener(self):
        """
        This tests that the provider won't do anything and just passes
        through any None values that it may get from the sub-class.

        Also checks that nothing is published to the event listener in
        this case.
        :return:
        """

        self.provider.testing_prompt_result = None
        unit_test_event_listener = UnitTestCompletionEventListener()

        result = self.get_completion_for_test_prompt(
            event_listener=unit_test_event_listener,
            metadata={
                "chart_id": self.test_chart_id,
                "node_id": self.test_node_id,
                "value_index": self.test_value_index
            },
        )

        self.assertIsNone(result)
        self.assertEquals(len(unit_test_event_listener.events), 0)

    def test_completion_with_delay(self):
        """
        This tests that the provider will slow down sending the events to at most
        the target rate based on the number of events per second.
        :return:
        """
        unit_test_event_listener = UnitTestCompletionEventListener()

        self.provider.completion_events_per_second_limit = 100.0
        time_per_word = 1.0 / float(self.provider.completion_events_per_second_limit)

        start = datetime.datetime.now()
        result = self.get_completion_for_test_prompt(
            event_listener=unit_test_event_listener,
            metadata={
                "chart_id": self.test_chart_id,
                "node_id": self.test_node_id,
                "value_index": self.test_value_index
            }
        )
        self.assertIsNotNone(result)
        end = datetime.datetime.now()

        words = result.split(" ")
        expected_min_time = len(words) * time_per_word
        time_taken = (end - start).total_seconds()

        # Check that the time taken is at least the expected minimum time
        self.assertGreaterEqual(time_taken, expected_min_time)

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
