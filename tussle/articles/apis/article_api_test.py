import unittest
import requests
import pkg_resources
import json
from tussle.general.testing.test_case_base import ArticulonTestCaseBase
from tussle.general.api_server.test_api_server import TestAPIServer


class ArticleAPITest(ArticulonTestCaseBase):
    test_api_port = 6005

    def setUp(self):
        self.server = TestAPIServer()
        self.server.run_in_background(port=self.test_api_port)

    def tearDown(self):
        self.server.shutdown_background()

    def test_create_article(self):
        test_article = self.load_test_article_fixture()

        # Delete ID off the test article
        del test_article['_id']

        # This checks that we can make a request to the home api
        response = requests.request("POST", f"http://localhost:{self.test_api_port}/article", json=test_article)

        # Check the status code is 200
        self.assertEqual(200, response.status_code)

        response_data = response.json()

        # Check that a value has been assigned to the '_id' field in the return
        self.assertIsNotNone(response_data['_id'])

    def load_test_article_fixture(self):
        test_article_data = pkg_resources.resource_string("tussle", f"articles/test_fixtures/test_article_1.json").decode("utf-8")
        test_article = json.loads(test_article_data)

        return test_article

    def test_delete_article(self):
        test_article = self.load_test_article_fixture()

        # First create the article
        response = requests.request("POST", f"http://localhost:{self.test_api_port}/article", json=test_article)
        response_data = response.json()

        article_id = response_data['_id']

        # If we then request the article, with GET, we should get 200 because it exists.
        response = requests.request("GET", f"http://localhost:{self.test_api_port}/article/{article_id}")
        self.assertEqual(200, response.status_code)

        # Now attempt to delete the article
        response = requests.request("DELETE", f"http://localhost:{self.test_api_port}/article/{article_id}")
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
