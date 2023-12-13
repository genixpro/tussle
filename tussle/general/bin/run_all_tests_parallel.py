from tussle.general.testing.test_suite_discovery import discover_complete_test_suite
from tussle.general.testing.test_parallel_runner import run_test_suite_parallel
from tussle.general.logger import create_global_logger
import logging

def main():
    # Set the logger with a warning log level
    create_global_logger(logging.WARNING)

    # Discover and run the unit tests
    complete_suite = discover_complete_test_suite()
    error_count = run_test_suite_parallel(complete_suite)

    if error_count > 0:
        # Return exit code 1 indicating failure
        return 1
    else:
        return 0


if __name__ == "__main__":
    code = main()
    exit(code)
