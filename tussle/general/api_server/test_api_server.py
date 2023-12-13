from tussle.general.api_server.flask_app import create_flask_app
import werkzeug.serving
import time
import requests
import threading

class TestAPIServer:
    """
    This just wraps our API server in such a way that it can be run in the background behind unit tests.
    """
    default_port = 6001

    def __init__(self, port=default_port):
        self.app = create_flask_app()

        self.port = port

        self.thread = None
        self.port = None
        self.httpd = None

    def run(self, port=default_port):
        self.port = port

        with self.app.app_context():
            self.httpd = werkzeug.serving.make_server('localhost', port, self.app, request_handler=None, threaded=True)
            self.httpd.serve_forever()


    def wait_for_status_endpoint_ready(self):
        for n in range(100):
            try:
                requests.get(f"http://localhost:{self.port}/")
                return
            except:
                time.sleep(0.1)
        raise Exception("Could not connect to status endpoint. Appears that the action prediction server background thread did not start successfully.")

    def run_in_background(self, port):
        self.thread = threading.Thread(target=self.run, args=(port,), daemon=True)
        self.thread.start()

        self.wait_for_status_endpoint_ready()

    def shutdown_background(self):
        if self.httpd is not None:
            self.httpd.shutdown()
        if self.thread is not None:
            self.thread.join()
