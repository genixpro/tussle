from .openai_completion_provider import OpenAICompletionProvider
import unittest
from tussle.completions.providers.completion_provider_test_base import CompletionProviderTestBase
from tussle.integrations.openai.openai_integration import OpenAIIntegration
from tussle.general.config.config import load_cloud_configuration


class OpenAICompletionProviderTest(CompletionProviderTestBase):
    provider = None

    @classmethod
    def setUpClass(cls):
        CompletionProviderTestBase.setUpClass()

        integration = OpenAIIntegration(load_cloud_configuration())
        cls.provider = OpenAICompletionProvider(integration)

    @classmethod
    def tearDownClass(cls):
        CompletionProviderTestBase.tearDownClass()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    test_prompt = "this is a testing prompt, used in unit tests and integrations. please just print 'yes sir. acknowledged' and nothing else."
    # Get a completion with a temperature of 0. Then we can check the exact value of the
    # result since it should always be the same
    test_temp = 0.0
    test_randomized_value = 0.5
    test_result = "yes sir. acknowledged"

    def test_get_completion(self):
        result = self.provider.get_completion(
            prompt=self.test_prompt,
            temperature=self.test_temp,
            event_listener=None,
            metadata=None,
            randomized_value=self.test_randomized_value
        )

        self.assertIsInstance(result, str)
        self.assertEqual(self.test_result.lower(), result.lower())

    def test_get_completion_length_limit(self):
        self.provider.max_completion_length = 1

        result = self.provider.get_completion(
            prompt=self.test_prompt,
            temperature=self.test_temp,
            event_listener=None,
            metadata=None,
            randomized_value=self.test_randomized_value
        )

        self.assertIsInstance(result, str)
        self.assertEqual("yes", result.lower())

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
