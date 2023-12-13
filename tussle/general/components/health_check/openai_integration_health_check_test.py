import unittest
from tussle.general.testing.test_case_base import ArticulonTestCaseBase
from tussle.general.components.health_check.openai_integration_health_check import OpenAIIntegrationHealthCheck

class OpenAIIntegrationHealthCheckTest(ArticulonTestCaseBase):
    def test_health_check(self):
        """
        Checks that we can run the health check, and that it passes in the testing configuration.
        :return:
        """
        check = OpenAIIntegrationHealthCheck()
        result = check.check()
        self.assertIn('healthy', result)
        self.assertIn('details', result)
        self.assertIn('message_content', result['details'])

        self.assertEqual(True, result['healthy'])


if __name__ == '__main__':
    unittest.main()
