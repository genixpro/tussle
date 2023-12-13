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


if __name__ == '__main__':
    unittest.main()
