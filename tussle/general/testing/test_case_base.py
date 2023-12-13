from tussle.general.testing.initialization import initialize_container_for_tests
from tussle.general.logger import get_logger
from tussle.general.testing.test_case_time_tracker import record_test_case_time_taken, record_test_method_time_taken
import unittest
import time
import datetime
import timeout_decorator

class ArticulonTestCaseBase(unittest.TestCase):
    logger = get_logger("ArticulonTestCaseBase")

    container = None
    start_time: datetime.datetime = None
    single_test_timeout = 60
    test_retry_count = 3

    @classmethod
    def setUpClass(cls):
        cls.container = initialize_container_for_tests()
        # Sleep for a second. for some reason this reduces
        # flakiness. Need to come up with a better solution
        # eventually.
        time.sleep(0.01)

        cls.start_time = datetime.datetime.now()

        # Change all the functions within this class that start with "test_*" to have a timeout.
        # This is to prevent tests from hanging forever.
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if attr_name.startswith("test_") and callable(attr):
                setattr(cls, attr_name, timeout_decorator.timeout(ArticulonTestCaseBase.single_test_timeout)(attr))

    @classmethod
    def tearDownClass(cls):
        end_time = datetime.datetime.now()

        time_taken_seconds = (end_time - cls.start_time).total_seconds()

        # Record the time taken for this test to run
        record_test_case_time_taken(cls.__name__, time_taken_seconds)


        # if cls.container is not None:
        #     self.logger.info("Unwiring and shutting down the DI container for tests")
        #     cls.container.shutdown_resources()
        #     cls.container.unwire()
        #     cls.container = None
    # Wrapping each test method so that a retry would take place.

    def run(self, result=None):
        """
        A customized test run method which will automatically retry failed tests, in order to reduce the
        effect of any flakiness.

        :param result:
        :return:
        """
        self.origTestMethodName = self._testMethodName

        for attempt_number in range(ArticulonTestCaseBase.test_retry_count):
            error_count_before_test_run = len(result.errors)  # check how many tests that are marked as failed before starting
            failure_count_before_test_run = len(result.failures)  # check how many tests that are marked as failed before starting

            start_time = datetime.datetime.now()

            super().run(result)

            end_time = datetime.datetime.now()

            time_used = (end_time - start_time).total_seconds()

            error_count_after_test_run = len(result.errors)
            failure_count_after_test_run = len(result.failures)

            had_error = False
            if error_count_after_test_run > error_count_before_test_run:
                had_error = True

            had_failure = False
            if failure_count_after_test_run > failure_count_before_test_run:
                had_failure = True

            if not had_error and not had_failure:
                # We're good. Test passed.
                record_test_method_time_taken(self.__class__.__name__,  str(self.origTestMethodName), time_used)
                break
            elif attempt_number == ArticulonTestCaseBase.test_retry_count - 1:
                # We're out of retries. Test failed.
                break
            else:
                # Remove the last error and/or failure from the internal list and try again.
                while len(result.errors) > error_count_before_test_run:
                    result.errors.pop(-1)
                while len(result.failures) > failure_count_before_test_run:
                    result.failures.pop(-1)

                self.logger.error(f"Test failed - {self.__class__.__name__}.{str(self.origTestMethodName)} - attempt {attempt_number + 1} of {ArticulonTestCaseBase.test_retry_count}. Retrying...")

                # A small exponential backoff on retrying
                time.sleep(2 ** attempt_number)
