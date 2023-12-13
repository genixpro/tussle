import unittest
import logging
from tussle.general.logger import create_global_logger
from tussle.general.testing.test_suite_discovery import discover_slow_test_suite
from tussle.general.testing.test_parallel_runner import run_test_suite_parallel


def main():
    # Set the logger with a warning log level
    create_global_logger(logging.WARNING)

    slow_suite = discover_slow_test_suite()

    total_errors = run_test_suite_parallel(slow_suite)

    if total_errors > 0:
        # Return exit code 1 indicating failure
        return 1
    else:
        return 0


if __name__ == "__main__":
    code = main()
    exit(code)
