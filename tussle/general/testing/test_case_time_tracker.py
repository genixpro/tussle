"""
This module contains functions used to record how long tests take to run.
"""
import pkg_resources
import json
import os
import functools


def record_test_case_time_taken(test_case_class_name: str, time_taken_seconds: float):
    """
    Records the time taken for a test to run. This is used to track the performance of tests over time
    and allow us to identify which tests are fast enough to be included in the 'fast' test suite.

    :param test_case_class_name: The class name for the test case object
    :param time_taken_seconds: The time taken for the test to run in seconds.
    """
    time_taken_file_path = pkg_resources.resource_filename('tussle', 'general/testing/test_case_times.json')

    # Round seconds down to three decimal places
    time_taken_seconds = round(time_taken_seconds * 1000) / 1000

    try:
        # Add the time taken for this test into the shared test times file
        if os.path.exists(time_taken_file_path):
            with open(time_taken_file_path, 'rt') as f:
                times = json.load(f)
                if test_case_class_name in times:
                    # Check if the difference is greater then both 50% of the current time or 0.75 seconds
                    # So yes these times can get a little out of date but it also means the test case times
                    # file isn't constantly changing and fluctuating.
                    if abs(times[test_case_class_name] - time_taken_seconds) > max(times[test_case_class_name] * 0.5, 0.75):
                        times[test_case_class_name] = time_taken_seconds
                else:
                    times[test_case_class_name] = time_taken_seconds
        else:
            times = {
                test_case_class_name: time_taken_seconds
            }
    except json.decoder.JSONDecodeError:
        # This means two processes were trying to modify the file at the same time.
        # We will just ignore this case and not record the test time this time.
        return

    try:
        with open(time_taken_file_path, 'wt') as f:
            json.dump(times, f, indent=4, sort_keys=True)
    except PermissionError:
        # Probably means that this code is running inside a container or installed
        # version instead of your local repo. Ignore the error.
        pass

def record_test_method_time_taken(test_case_class_name: str, test_method_name: str, time_taken_seconds: float):
    """
    Records the time taken for individual test methods to run. This is used to track the performance
    of tests over time and allow us to identify which tests are fast enough to be included in the
    'fast' test suite.

    :param test_case_class_name: The class name for the test case object
    :param test_method_name: The name of the specific test function
    :param time_taken_seconds: The time taken for the test to run in seconds.
    """
    time_taken_file_path = pkg_resources.resource_filename('tussle', 'general/testing/test_method_times.json')

    time_taken_key = f"{test_case_class_name}.{test_method_name}"

    # Round milliseconds down to one decimal place.
    time_taken_milliseconds = round(time_taken_seconds * 10000) / 10

    try:
        # Add the time taken for this test into the shared test times file
        if os.path.exists(time_taken_file_path):
            with open(time_taken_file_path, 'rt') as f:
                times = json.load(f)
                if time_taken_key in times:
                    # Check if the difference is greater then both 50% of the current time or 10 milliseconds (0.01 seconds)
                    # So yes these times can get a little out of date but it also means the test case times
                    # file isn't constantly changing and fluctuating.
                    if abs(times[time_taken_key] - time_taken_milliseconds) > max(times[time_taken_key] * 0.5, 10):
                        times[time_taken_key] = time_taken_milliseconds
                else:
                    times[time_taken_key] = time_taken_milliseconds
        else:
            times = {
                time_taken_key: time_taken_milliseconds
            }
    except json.decoder.JSONDecodeError:
        # This means two processes were trying to modify the file at the same time.
        # We will just ignore this case and not record the test time this time.
        return

    try:
        with open(time_taken_file_path, 'wt') as f:
            json.dump(times, f, indent=4, sort_keys=True)
    except PermissionError:
        # Probably means that this code is running inside a container or installed
        # version instead of your local repo. Ignore the error.
        pass



@functools.cache
def load_time_taken_file_cached():
    """
    Loads the time taken for each test from the shared file.

    :return: A dictionary mapping test class names to the time taken for the test to run.
    """
    time_taken_file_data = pkg_resources.resource_string('tussle', 'general/testing/test_case_times.json')
    return json.loads(time_taken_file_data)

def get_expected_time_for_test_case(test_case_class_name: str):
    times = load_time_taken_file_cached()
    return times.get(test_case_class_name)


@functools.cache
def load_time_taken_by_method_file_cached():
    """
    Loads the time taken for each test from the shared file.

    :return: A dictionary mapping test class names to the time taken for the test to run.
    """
    time_taken_file_data = pkg_resources.resource_string('tussle', 'general/testing/test_method_times.json')
    return json.loads(time_taken_file_data)


def get_expected_time_for_test_method(test_case_class_name: str, test_method_name: str):
    times = load_time_taken_by_method_file_cached()
    time_taken_key = f"{test_case_class_name}.{test_method_name}"
    return times.get(time_taken_key)
