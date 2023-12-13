import unittest
import concurrent.futures
import random
import os
from .test_case_time_tracker import get_expected_time_for_test_case
from .test_suite_discovery import get_name_of_test_case

number_of_parallel_test_processes = 8

def run_test_suite_parallel(test_suite):
    """
    This will run the given test suite with parallelism.

    :param test_suite:
    :return: The number of errors observed.
    """

    split_suites = split_test_suite(test_suite, number_of_parallel_test_processes)

    total_errors = 0
    total_failures = 0

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        for sub_suite_index, sub_suite in enumerate(split_suites):
            future = executor.submit(run_sub_suite, sub_suite, sub_suite_index)
            futures.append(future)

        sub_suite_results = [future.result() for future in futures]

    for result in sub_suite_results:
        error_count, failure_count = result
        total_errors += error_count
        total_failures += failure_count

    print(f"Final overall results from parallel test run:")
    print(f"Errors: {total_errors}")
    print(f"Failures: {total_failures}")


    return total_errors + total_failures


def run_sub_suite(sub_suite, sub_suite_index):
    # Set a global environment variable that gets picked up by AMQP to connect to one of the separate virtual hosts.
    # TODO: There needs to be a better way to pass through this configuration.
    os.environ['AMQP_VIRTUAL_HOST_SUFFIX'] = f"-{sub_suite_index}"

    # Do the same with mongodb. Ensure each parallel process uses a separate mongodb database.
    # TODO: Also improve this
    os.environ['MONGO_DATABASE_NAME_SUFFIX'] = f"-{sub_suite_index}"

    runner = unittest.TextTestRunner()
    result = runner.run(sub_suite)
    return (len(result.errors), len(result.failures))



def split_test_suite(test_suite, count_splits=number_of_parallel_test_processes):
    sub_suites = [
        unittest.TestSuite()
        for _ in range(count_splits)
    ]

    time_required_by_suite = [0] * count_splits

    all_test_cases = []
    for sub_suite in test_suite:
        for test_case in sub_suite:
            time_required = get_expected_time_for_test_case(test_case_class_name=get_name_of_test_case(test_case))

            # Add some random jitter to the time required, so that tests don't always get sorted to the exact same
            # sub suite.
            if time_required is not None:
                time_required = random.uniform(0.5, 1.5) * time_required + random.uniform(0, 0.01)

            all_test_cases.append((time_required, test_case))

    # Sort all the test cases in descending order of how long they take.
    all_test_cases = sorted(all_test_cases, key=lambda x: x[0] if x[0] is not None else 0, reverse=True)

    current_index = 0
    for time_required, test_case in all_test_cases:
        current_index += 1

        if time_required is not None:
            min_time_required_index = time_required_by_suite.index(min(time_required_by_suite))

            sub_suites[min_time_required_index].addTest(test_case)
            time_required_by_suite[min_time_required_index] += time_required
        else:
            sub_suites[current_index % count_splits].addTest(test_case)


    return sub_suites

