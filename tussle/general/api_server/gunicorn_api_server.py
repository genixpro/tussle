import gunicorn.app.base
from tussle.general.api_server.flask_app import create_flask_app
from tussle.general.components.health_check.combined_concurrent_health_check import CombinedConcurrentHealthCheck
from tussle.application import create_and_initialization_application_container
from pprint import pformat
import gunicorn.workers.gthread

class GunicornApiServer(gunicorn.app.base.BaseApplication):
    """
        This class is used for booting a production ready API server using gunicorn,
        to serve our API in production.
    """

    def __init__(self):
        # This is the hardcoded configuration used for booting the gunicorn server.
        self.options = {
            'bind': "0.0.0.0:5496",
            'workers': 1,
            'threads': 12,
            'timeout': 600,
            'worker_class':  'tussle.general.api_server.gunicorn_api_server.GunicornThreadWorkerWithInitialization',
        }

        self.application = create_flask_app()
        super().__init__()

    def health_check(self):
        # Run the initial health check to make sure that the server is healthy before we start serving requests
        health_check = CombinedConcurrentHealthCheck()
        result = health_check.check()
        if not result['healthy']:
            raise Exception(f"Server is not healthy. Health check result:\n{pformat(result)}")

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

class GunicornThreadWorkerWithInitialization(gunicorn.workers.gthread.ThreadWorker):
    def run(self):
        # The worker runs in its own sub-process. Therefore, we need to rewire the application container
        # so we don't attempt to reuse connections or other resources from the parent process.
        container = create_and_initialization_application_container()

        # Now just run the worker as normal.
        super().run()

        # Shutdown the container after the worker is done.
        container.shutdown_resources()


if __name__ == '__main__':
    server = GunicornApiServer()
    server.health_check()
    server.run()

