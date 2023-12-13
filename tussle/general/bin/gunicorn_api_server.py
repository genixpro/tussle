# This script is used for booting the API server within gunicorn
from tussle.application import create_and_initialization_application_container
from tussle.general.api_server.gunicorn_api_server import GunicornApiServer

def main():
    container = create_and_initialization_application_container()

    # Create the gunicorn app to serve the flask app.
    app = GunicornApiServer()

    app.run()

    container.shutdown_resources()


if __name__ == "__main__":
    main()
