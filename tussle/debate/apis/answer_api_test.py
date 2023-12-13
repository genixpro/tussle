import unittest
import requests
import pkg_resources
import json
from tussle.general.testing.test_case_base import TussleTestCaseBase
from tussle.general.api_server.test_api_server import TestAPIServer


class AnswerAPITest(TussleTestCaseBase):
    test_api_port = 6005

    def setUp(self):
        self.server = TestAPIServer()
        self.server.run_in_background(port=self.test_api_port)

    def tearDown(self):
        self.server.shutdown_background()

    def test_create_answer(self):
        test_answer = self.load_test_answer_fixture()

        # Delete ID off the test answer
        del test_answer['_id']

        # This checks that we can make a request to the home api
        response = requests.request("POST", f"http://localhost:{self.test_api_port}/answer", json=test_answer)

        # Check the status code is 200
        self.assertEqual(200, response.status_code)

        response_data = response.json()

        # Check that a value has been assigned to the '_id' field in the return
        self.assertIsNotNone(response_data['_id'])

    def load_test_answer_fixture(self):
        test_answer_data = pkg_resources.resource_string("tussle", f"answers/test_fixtures/test_answer_1.json").decode("utf-8")
        test_answer = json.loads(test_answer_data)

        return test_answer

    def test_delete_answer(self):
        test_answer = self.load_test_answer_fixture()

        # First create the answer
        response = requests.request("POST", f"http://localhost:{self.test_api_port}/answer", json=test_answer)
        response_data = response.json()

        answer_id = response_data['_id']

        # If we then request the answer, with GET, we should get 200 because it exists.
        response = requests.request("GET", f"http://localhost:{self.test_api_port}/answer/{answer_id}")
        self.assertEqual(200, response.status_code)

        # Now attempt to delete the answer
        response = requests.request("DELETE", f"http://localhost:{self.test_api_port}/answer/{answer_id}")
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
