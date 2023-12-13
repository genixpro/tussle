import unittest
import requests
import pkg_resources
import json
from tussle.general.testing.test_case_base import TussleTestCaseBase
from tussle.general.api_server.test_api_server import TestAPIServer


class TopicAPITest(TussleTestCaseBase):
    test_api_port = 6005

    def setUp(self):
        self.server = TestAPIServer()
        self.server.run_in_background(port=self.test_api_port)

    def tearDown(self):
        self.server.shutdown_background()

    def test_create_topic(self):
        test_topic = self.load_test_topic_fixture()

        # Delete ID off the test topic
        del test_topic['_id']

        # This checks that we can make a request to the home api
        response = requests.request("POST", f"http://localhost:{self.test_api_port}/topic", json=test_topic)

        # Check the status code is 200
        self.assertEqual(200, response.status_code)

        response_data = response.json()

        # Check that a value has been assigned to the '_id' field in the return
        self.assertIsNotNone(response_data['_id'])

    def load_test_topic_fixture(self):
        test_topic_data = pkg_resources.resource_string("tussle", f"topics/test_fixtures/test_topic_1.json").decode("utf-8")
        test_topic = json.loads(test_topic_data)

        return test_topic

    def test_delete_topic(self):
        test_topic = self.load_test_topic_fixture()

        # First create the topic
        response = requests.request("POST", f"http://localhost:{self.test_api_port}/topic", json=test_topic)
        response_data = response.json()

        topic_id = response_data['_id']

        # If we then request the topic, with GET, we should get 200 because it exists.
        response = requests.request("GET", f"http://localhost:{self.test_api_port}/topic/{topic_id}")
        self.assertEqual(200, response.status_code)

        # Now attempt to delete the topic
        response = requests.request("DELETE", f"http://localhost:{self.test_api_port}/topic/{topic_id}")
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
