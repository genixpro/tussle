import unittest
import datetime
from tussle.general.testing.test_case_base import TussleTestCaseBase
from tussle.general.components.health_check.health_check_base import HealthCheckBase
import time


class UnitTestHealthCheck(HealthCheckBase):
    def __init__(self):
        super().__init__()
        self.should_throw = False
        self.should_wait = False

    def check(self):
        if self.should_throw:
            raise Exception("This is an exception")
        elif self.should_wait:
            for n in range(10):
                time.sleep(0.2)
            return {
                "healthy": True,
                "details": {}
            }
        else:
            return {
                "healthy": True,
                "details": {}
            }

class HealthCheckBaseTest(TussleTestCaseBase):
    def test_run_error_handling(self):
        """
        This function tests the handling of the run() function in the HealthCheckBase class.
        :return:
        """
        # Initialize the unit test health check, which is derived from HealthCheckBase.
        health_check = UnitTestHealthCheck()

        # Run the health check, and ensure that it returns healthy.
        result = health_check.run()

        self.assertEqual(True, result['healthy'])

        # Set the should_throw flag to True, and run the health check again.
        # This time, it should return unhealthy. It shouldn't let the exception
        # bubble.
        health_check.should_throw = True

        result = health_check.run()
        self.assertEqual(False, result['healthy'])

        # Check that the error details have been stored.
        self.assertIn('error', result['details'])
        self.assertIn('This is an exception', result['details']['error'])


    def test_run_add_time_taken(self):
        """
        This function tests the handling of the run() function in the HealthCheckBase class.

        It verifies that the time_taken field is added to the details in the result.
        :return:
        """
        # Initialize the unit test health check, which is derived from HealthCheckBase.
        health_check = UnitTestHealthCheck()

        # Run the health check, and ensure that it returns healthy.
        result = health_check.run()

        # Check that the time_taken field is added to the details in the result.
        self.assertIn('time_taken', result['details'])

        # Check that it can be interpreted as a float
        float(result['details']['time_taken'])

    @unittest.skip
    def test_run_timeout(self):
        """
        This function tests that the run() function will time out the health check if it
        takes too long to run.
        :return:
        """
        # Initialize the unit test health check, which is derived from HealthCheckBase.
        health_check = UnitTestHealthCheck()
        health_check.should_wait = True

        start = datetime.datetime.now()

        # Run the health check, and ensure that it returns unhealthy,
        # because the unit test health check is set to wait for 10 seconds.
        health_check.timeout = 0.10
        result = health_check.run()

        self.assertFalse(result['healthy'])

        # Check that it didn't wait for 10 seconds to return unhealthy, since the timeout was set at 100ms
        finish = datetime.datetime.now()

        time_taken = (finish - start).total_seconds()

        self.assertLess(time_taken, 0.5)

        # Check that the time_taken field is added to the details in the result.
        self.assertIn('time_taken', result['details'])


if __name__ == '__main__':
    unittest.main()
