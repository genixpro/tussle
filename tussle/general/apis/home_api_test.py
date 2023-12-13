from tussle.general.api_server.test_api_server import TestAPIServer
from tussle.general.testing.test_case_base import ArticulonTestCaseBase
import datetime
import requests
import unittest

class HomeAPITest(ArticulonTestCaseBase):
    test_api_port = 6006

    def setUp(self):
        self.server = TestAPIServer()
        self.server.run_in_background(port=self.test_api_port)

    def tearDown(self):
        self.server.shutdown_background()

    def test_home_api(self):
        # This checks that we can make a request to the home api
        response = requests.request("GET", f"http://localhost:{self.test_api_port}/")

        # Check that response content-type is application/json
        self.assertEqual("application/json", response.headers['Content-Type'])

        response_data = response.json()

        self.check_response_host_is_correct(response_data)
        self.check_response_version_is_correct(response_data)
        self.check_response_start_time_is_correct(response_data)
        self.check_response_current_time_is_correct(response_data)

    def check_response_name_is_correct(self, response_data):
        # Check the response contains a name field
        self.assertIn('name', response_data, msg="The home endpoint response does not contain a 'name' field")

        # Check the response contains a 'name' field that is a string
        self.assertIsInstance(response_data['name'], str)

        # Check that name isn't empty
        self.assertNotEqual("", response_data['name'])

        # Check the name is the correct value
        self.assertEqual("Articulon API Server", response_data['name'])

    def check_response_host_is_correct(self, response_data):
        # Check the response contains a host field
        self.assertIn('host', response_data, msg="The home endpoint response does not contain a 'host' field")

        # Check the response contains a 'host' field that is a string
        self.assertIsInstance(response_data['host'], str)

        # Check that host isn't empty
        self.assertNotEqual("", response_data['host'])

    def check_response_version_is_correct(self, response_data):
        # Check the response contains a 'version' field
        self.assertIn('version', response_data, msg="The home endpoint response does not contain a 'version' field")

        # Check the response contains a 'version' field that is a string
        self.assertIsInstance(response_data['version'], str)

        # Check that version isn't empty
        self.assertNotEqual("", response_data['version'])

    def check_response_start_time_is_correct(self, response_data):
        """
        This function checks that the response_data contains a start_time field, and that the value of the start_time
        field is a string in ISO-8601 format.

        :param response_data:
        :return:
        """
        # Check the response contains a 'start_time' field
        self.assertIn('start_time', response_data,
                      msg="The home endpoint response does not contain a 'start_time' field")

        # Check the response contains a 'start_time' field that is a string
        self.assertIsInstance(response_data['start_time'], str)

        # Check that start_time isn't empty
        self.assertNotEqual("", response_data['start_time'])

        # Check that start_time is in ISO-8601 format
        # https://en.wikipedia.org/wiki/ISO_8601
        # This will throw an exception of the string isn't in ISO-8601 format
        datetime.datetime.fromisoformat(response_data['start_time'])

    def check_response_current_time_is_correct(self, response_data):
        """
        This function checks that the response_data contains a current_time field, and that the value of the
        current_time field is a string in ISO-8601 format.
        :param response_data:
        :return:
        """
        # Check the response contains a 'current_time' field
        self.assertIn('current_time', response_data,
                      msg="The home endpoint response does not contain a 'current_time' field")

        # Check that the value for 'current_time' is a string
        self.assertIsInstance(response_data['current_time'], str)

        # Check that current_time isn't empty.
        self.assertNotEqual("", response_data['current_time'])

        # Check that current_time is in ISO-8601 format
        # https://en.wikipedia.org/wiki/ISO_8601
        # This will throw an exception of the string isn't in ISO-8601 format
        datetime.datetime.fromisoformat(response_data['current_time'])

    def test_home_api_pretty_print(self):
        """
        This function checks that the home api returns pretty formatted JSON, rather then compact format.
        This makes it much easier to read the API output when requesting the endpoint manually.

        :return:
        """
        # This checks that we can make a request to the home api
        response = requests.request("GET", f"http://localhost:{self.test_api_port}/")

        # This checks that the JSON in the response_data was pretty formatted
        response_text = response.text

        # Check that there is a newline character in the response, and not at the start or end.
        # JSON that isn't pretty formatted will not have any newline characters in the body
        # of the json object.
        self.assertIn('\n', response_text.strip())

if __name__ == '__main__':
    unittest.main()
