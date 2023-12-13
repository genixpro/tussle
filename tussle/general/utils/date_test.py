import unittest
import datetime
from .date import convert_date_from_iso_format

class DateTest(unittest.TestCase):
    """
    This function tests utility functions in the 'tussle.general.utils.date' module
    """


    def test_convert_date_from_iso_format(self):
        test_cases = [
            {
                "date_string": "2020-01-01T00:00:00.000",
                "expected": datetime.datetime(2020, 1, 1, 0, 0, 0)
            },
            {
                "date_string": "2020-01-01T00:00:00.000Z",
                "expected": datetime.datetime(2020, 1, 1, 0, 0, 0)
            },
            {
                "date_string": "2023-10-20T14:12:16.371Z",
                "expected": datetime.datetime(2023, 10, 20, 14, 12, 16, 371000)
            },
            {
                "date_string": datetime.datetime(2023, 10, 20, 14, 12, 16, 371000).isoformat(),
                "expected": datetime.datetime(2023, 10, 20, 14, 12, 16, 371000)
            }
        ]

        for test_case in test_cases:
            with self.subTest(date_string=test_case['date_string']):
                actual = convert_date_from_iso_format(test_case["date_string"])
                self.assertEqual(actual, test_case["expected"])
