import unittest
from pprint import pformat
from tussle.general.testing.test_case_time_tracker import get_expected_time_for_test_case


def discover_complete_test_suite():
    """
    This will autodiscover all the tests within Articulon, and build up a python native unittest.TestSuite object
    composed of all of those tests.
    :return:
    """
    # Discover and run the unit tests
    loader = unittest.TestLoader()
    complete_suite = loader.discover("tussle", pattern="*_test.py")
    return complete_suite

def discover_fast_test_suite():
    """
    This will autodiscover all the tests within Articulon, but filter them for only tests that execute really
    fast. It returns a test suite that can be executed very quickly for pre-commit checks.
    :return:
    """
    return discover_filtered_test_suite(lambda test_case: does_test_case_have_any_tests(test_case) and is_test_case_fast(test_case))

def discover_slow_test_suite():
    """
    This will autodiscover all the tests within Articulon, but filter them for only tests that
    execute slowly. It returns the opposite of discover_fast_test_suite. The two of them together
    will execute all the tests within Articulon.
    :return:
    """

    return discover_filtered_test_suite(lambda test_case: does_test_case_have_any_tests(test_case) and not is_test_case_fast(test_case))

def discover_rapid_internal_only_test_suite():
    """
    This will autodiscover all the tests within Articulon, but filter them for tests that both
    execute fast and do not have external dependencies. It returns a test suite that can be executed
    very quickly with no external dependencies.

    :return:
    """

    return discover_filtered_test_suite(lambda test_case: does_test_case_have_any_tests(test_case) and is_test_case_internal_only(test_case) and is_test_case_fast(test_case))


def discover_internal_only_test_suite():
    """
    This will autodiscover all the tests within Articulon, but filter them for tests that don't depend
    upon amqp, mongodb or other external services.

    :return:
    """

    return discover_filtered_test_suite(lambda test_case: does_test_case_have_any_tests(test_case) and is_test_case_internal_only(test_case))


def discover_external_test_suite():
    """
    This will autodiscover all the tests within Articulon, but filter them for tests that don't depend
    upon amqp, mongodb or other external services.

    :return:
    """

    return discover_filtered_test_suite(lambda test_case: does_test_case_have_any_tests(test_case) and not is_test_case_internal_only(test_case))


def discover_filtered_test_suite(filter_func):
    """
    This will autodiscover all the tests within Articulon, but filter them for test cases that
    pass the given filter function.
    :return:
    """
    # Discover and run the unit tests
    complete_suite = discover_complete_test_suite()

    test_case_names = []

    # Filter the test suite for only test cases that run very fast
    filtered_test_suite = unittest.TestSuite()
    for sub_suite in complete_suite:
        for test_case in sub_suite:
            if filter_func(test_case):
                filtered_test_suite.addTest(test_case)
                test_case_names.append(get_name_of_test_case(test_case))

    print(f"Running the following test cases:\n{pformat(sorted(test_case_names))}")

    return filtered_test_suite

def is_test_case_fast(test_case):
    tests = list(test_case)
    if not len(tests):
        return False

    is_fast = True
    test_case_class_name = get_name_of_test_case(test_case)

    expected_time = get_expected_time_for_test_case(test_case_class_name=test_case_class_name)
    if expected_time is None:
        is_fast = False
    elif expected_time is not None and expected_time > 1.0:
        # hack, modify inner variable to not run these tests.
        is_fast = False

    return is_fast


def is_test_case_internal_only(test_case):
    # TODO: We need a better way of identifying which tests are internal only.
    # TODO: Plus too many of these cases are not actually internal only.
    # TODO: So there is lots of room for provement here
    ignore_keywords = [
        'amqp',
        'mongo',
        'openai',
        'gcs',
        'health',
        'db',
        'customid',
        'combinedembedding',
        'embeddingsimilarity',
        'stream',
        'task',
        'bulk',
        'textpatternmatcher',
        'resultclassifier',
        'promptcharteval',
        'imageprocessor',
        'singlecharteval',
    ]

    tests = list(test_case)
    if not len(tests):
        return False

    test_case_class_name = get_name_of_test_case(test_case)
    for keyword in ignore_keywords:
        if keyword in test_case_class_name.lower():
            return False

    return True



def does_test_case_have_any_tests(test_case):
    tests = list(test_case)
    if not len(tests):
        return False

    return True


def get_name_of_test_case(test_case):
    if issubclass(test_case.__class__, unittest.TestCase):
        return test_case.__class__.__name__

    tests = list(test_case)
    if len(tests) == 0:
        return test_case.__class__.__name__
    test_case_class_name = tests[0].__class__.__name__
    return test_case_class_name
