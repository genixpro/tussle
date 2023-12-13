import unittest
import logging
from tussle.general.logger import create_global_logger
from tussle.general.testing.test_suite_discovery import discover_fast_test_suite


def main():
    # Set the logger with a warning log level
    create_global_logger(logging.WARNING)

    fast_suite = discover_fast_test_suite()

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
