import unittest
import concurrent.futures
from tussle.general.testing.test_case_base import ArticulonTestCaseBase
from tussle.general.components.health_check.db_access_health_check import DbAccessHealthCheck

class DbAccessHealthCheckTest(ArticulonTestCaseBase):
    def test_health_check(self):
        """
        Checks that we can run the health check, and that it passes in the testing configuration.
        :return:
        """
        self.run_single_health_check_test()

    def run_single_health_check_test(self):
        """
        This creates the health check and runs a single test to ensure it passes.

        :return:
        """
        check = DbAccessHealthCheck()
        result = check.check()
        self.assertIn('healthy', result)
        self.assertIn('details', result)
        self.assertIn('result_count', result['details'])
        self.assertEqual(True, result['healthy'])

    def test_health_check_parallelism(self):
        """
        This ensures that the health check can be run in parallel without any issues
        or them conflicting with each other.
        :return:
        """
        # Now try to run a bunch of health checks in parallel.
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for n in range(25):
                futures.append(executor.submit(self.run_single_health_check_test))
            for future in futures:
                # Try and get the result. If there was a crash, the exception will be reraised here.
                future.result()


if __name__ == '__main__':
    unittest.main()
