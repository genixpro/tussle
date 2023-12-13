from tussle.general.api_server.test_api_server import TestAPIServer
from tussle.general.testing.test_case_base import ArticulonTestCaseBase
import requests
import unittest

class HealthCheckAPITest(ArticulonTestCaseBase):
    test_api_port = 6007

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.worker = None

    def setUp(self):
        self.server = TestAPIServer()
        self.server.run_in_background(port=self.test_api_port)

    def tearDown(self):
        self.server.shutdown_background()
    def test_health_check_api(self):
        # This checks that we can make a request to the health check API, and that it returns healthy
        response = requests.request("GET", f"http://localhost:{self.test_api_port}/health_check")

        # Check that response content-type is application/json
        self.assertEqual("application/json", response.headers['Content-Type'])

        response_data = response.json()

        self.assertEqual(True, response_data['healthy'])
        self.assertEqual(True, response_data['details']['db_access']['healthy'])
        self.assertEqual(True, response_data['details']['openai_integration']['healthy'])

        self.check_response_metadata_fields(response_data)

    def check_response_metadata_fields(self, response_data):
        """
        This function checks that the response contains fields for host, version, check_start_time, and check_end_time
        and that the values are correct.

        :param response_data:
        :return:
        """
        # Check that the response contains fields for host, version, check_start_time, and check_end_time
        self.assertIn('host', response_data)
        self.assertIn('version', response_data)
        self.assertIn('check_start_time', response_data)
        self.assertIn('check_end_time', response_data)

        # Check the above fields are strings
        self.assertIsInstance(response_data['host'], str)
        self.assertIsInstance(response_data['version'], str)
        self.assertIsInstance(response_data['check_start_time'], str)
        self.assertIsInstance(response_data['check_end_time'], str)

        # Check that the strings aren't empty
        self.assertNotEqual("", response_data['host'])
        self.assertNotEqual("", response_data['version'])
        self.assertNotEqual("", response_data['check_start_time'])
        self.assertNotEqual("", response_data['check_end_time'])

    def test_health_check_api_pretty_print(self):
        """
        This function checks that the health check API returns JSON in pretty-printed format,
        instead of vanilla compact JSON.

        :return:
        """
        # This checks that we can make a request to the health check API, and that it returns healthy
        response = requests.request("GET", f"http://localhost:{self.test_api_port}/health_check")

        # This checks that the JSON in the response_data was pretty formatted
        response_text = response.text
        # Check that there is a newline character in the response, and not at the start or end.
        # JSON that isn't pretty formatted will not have any newline characters in the body
        # of the json object.
        self.assertIn('\n', response_text.strip())

if __name__ == '__main__':
    unittest.main()
