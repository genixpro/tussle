from abc import ABCMeta, abstractmethod
import datetime
import traceback
import concurrent.futures

class HealthCheckBase(metaclass=ABCMeta):
    """
    This is a base class for internal health checks that the system can perform on itself.
    """
    def __init__(self):
        self.timeout = 10.0

    @abstractmethod
    def check(self):
        """
        This function is responsible for performing the health check whether the system is healthy or
        not. This function is meant to be overridden by child classes.

        :return: A dictionary, containing two values.
                    healthy: A boolean indicating whether the health check passed or failed.
                    details: A dictionary containing additional information, such as errors or sub checks that were performed

        """
        raise NotImplementedError('HealthCheckBase.test not implemented')


    def run(self):
        """
        This function will run the health check defined in check(). It does some additional goodies,
        such as check to see if the check() function through an exception and returning unhealthy if
        it did.
        :return:
        """
        start = datetime.datetime.now()

        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(self.check)
                result = future.result(timeout=0.1)
        except Exception as e:
            result = {
                "healthy": False,
                "details": {
                    "error": traceback.format_exc()
                }
            }

        finish = datetime.datetime.now()
        result['details']['time_taken'] = f"{(finish - start).total_seconds():.3f}"
        return result
