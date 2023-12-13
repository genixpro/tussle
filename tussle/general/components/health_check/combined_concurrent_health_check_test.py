import unittest
from tussle.general.testing.test_case_base import TussleTestCaseBase
from tussle.general.components.health_check.combined_concurrent_health_check import CombinedConcurrentHealthCheck

class CombinedConcurrentHealthCheckTest(TussleTestCaseBase):

    def test_health_check(self):
        """
        Checks that we can run the health check, and that it passes in the testing configuration.
        :return:
        """
        check = CombinedConcurrentHealthCheck()
        result = check.check()
        self.assertIn('healthy', result)
        self.assertIn('details', result)

        self.assertIsInstance(result['healthy'], bool)
        self.assertTrue(result['healthy'])

        self.assertIn('db_access', result['details'])
        self.assertIn('openai_integration', result['details'])

        self.assertEqual(True, result['details']['db_access']['healthy'])
        self.assertEqual(True, result['details']['openai_integration']['healthy'])

        self.assertTrue(result['details']['db_access']['required'])
        self.assertTrue(result['details']['openai_integration']['required'])




if __name__ == '__main__':
    unittest.main()
