import unittest
from tussle.completions.event_listeners.unit_test_completion_event_listener import UnitTestCompletionEventListener
from tussle.general.testing.test_case_base import ArticulonTestCaseBase
from tussle.completions.event_listeners.completion_event import CompletionEventTypes

class CompletionProviderTestBase(ArticulonTestCaseBase):
    """
        A base class for all the completion provider tests.
    """
    def run_event_listener_test(self, provider, test_prompt, test_temp, test_randomized_value):
        """
        This is a function that runs a test against the given provider to ensure that it
        is returning the correct events in the correct order to the completion event
        listener.

        :return:
        """
        unit_test_event_listener = UnitTestCompletionEventListener()

        test_chart_id = "test_chart_id_12345"
        test_node_id = "my_node_id_456"
        test_value_index = 2

        result = provider.get_completion(
            prompt=test_prompt,
            temperature=test_temp,
            event_listener=unit_test_event_listener,
            metadata={
                "chart_id": test_chart_id,
                "node_id": test_node_id,
                "value_index": test_value_index
            },
            randomized_value=test_randomized_value
        )

        # One assertion to check the result value
        self.assertIsInstance(result, str)

        # Check that we have at-least 3 events. start, finish, and at-least one word in between
        self.assertGreaterEqual(len(unit_test_event_listener.events), 3)

        # Now check the event stream. First event should be a start event for a specific node value
        self.assertEqual(unit_test_event_listener.events[0].event, CompletionEventTypes.start_node_value_event)
        # Start event should have a 'word' of None
        self.assertIsNone(unit_test_event_listener.events[0].word)

        # Last event should be a finish event
        self.assertEqual(unit_test_event_listener.events[-1].event, CompletionEventTypes.finish_node_value_event)
        # The finish event should have its 'word' set to the completion result
        self.assertEqual(unit_test_event_listener.events[-1].word, result)

        # Check that everything in-between are word-events with real words
        for event in unit_test_event_listener.events[1:-1]:
            self.assertEqual(event.event, CompletionEventTypes.word_event)
            self.assertIsInstance(event.word, str)
            self.assertGreater(len(event.word), 0)
            self.assertNotEqual(event.word, " ")
            self.assertNotEqual(event.word, "")
            self.assertNotEqual(event.word, None)
            self.assertNotEqual(event.word, "None")
            self.assertNotEqual(event.word, "none")
            self.assertNotEqual(event.word, "NONE")
            self.assertNotEqual(event.word, "null")
            self.assertNotEqual(event.word, "NULL")
            self.assertNotEqual(event.word, "nil")
            self.assertNotEqual(event.word, "NIL")

        # Check that if we concatenate together all the word events, we get the same result
        # as the result string.
        concatenated_words = ''.join([event.word for event in unit_test_event_listener.events[1:-1]])
        self.assertEqual(concatenated_words, result)

        # Now check all the events to ensure they have the correct metadata
        for event in unit_test_event_listener.events:
            self.assertEqual(event.chart_id, test_chart_id)
            self.assertEqual(event.node_id, test_node_id)
            self.assertEqual(event.value_index, test_value_index)

    def run_event_listener_stream_words_false(self, provider, test_prompt, test_temp, test_randomized_value):
        """
        This is a function checks that if stream_words is set to False, then the provider
        will not stream individual words, just the start and finish events.

        :return:
        """
        unit_test_event_listener = UnitTestCompletionEventListener()

        test_chart_id = "test_chart_id_12345"
        test_node_id = "my_node_id_456"
        test_value_index = 2

        result = provider.get_completion(
            prompt=test_prompt,
            temperature=test_temp,
            event_listener=unit_test_event_listener,
            metadata={
                "chart_id": test_chart_id,
                "node_id": test_node_id,
                "value_index": test_value_index
            },
            randomized_value=test_randomized_value,
            stream_words=False
        )

        # One assertion to check the result value
        self.assertIsInstance(result, str)

        # Check that we have exactly 2 events, the start and finish events.
        self.assertEqual(len(unit_test_event_listener.events), 2)

        # Now check the event stream. First event should be a start event for a specific node value
        self.assertEqual(unit_test_event_listener.events[0].event, CompletionEventTypes.start_node_value_event)
        # Start event should have a 'word' of None
        self.assertIsNone(unit_test_event_listener.events[0].word)

        # Last event should be a finish event
        self.assertEqual(unit_test_event_listener.events[1].event, CompletionEventTypes.finish_node_value_event)
        # The finish event should have its 'word' set to the completion result
        self.assertEqual(unit_test_event_listener.events[1].word, result)


if __name__ == '__main__':
    unittest.main()
