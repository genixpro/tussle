import unittest
import logging
import os
from tussle.general.logger import create_global_logger
from tussle.general.testing.test_suite_discovery import discover_internal_only_test_suite


def main():
    # Set the logger with a warning log level
    create_global_logger(logging.WARNING)

    # Set the environment variable that indicates we are running the internal only test suite
    os.environ['FLOWTHOUGHT_ENV'] = 'internal_only'

    fast_suite = discover_internal_only_test_suite()

    runner = unittest.TextTestRunner()
    result = runner.run(fast_suite)

    total_errors = len(result.failures) + len(result.errors)

    if total_errors > 0:
        # Return exit code 1 indicating failure
        return 1
    else:
        return 0


if __name__ == "__main__":
    code = main()
    exit(code)
