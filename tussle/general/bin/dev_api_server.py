# This script is used for booting the API server within gunicorn
from tussle.application import create_and_initialization_application_container
from tussle.general.api_server.dev_api_server import DevAPIServer


def main():
    container = create_and_initialization_application_container()

    """ This is called for local dev servers, but this script also initializes the live server that
        is run in gunicorn. Gunicorn simply grabs the 'app' object from this script and does its own
        thing with it. """

    dev_api_server = DevAPIServer()
    dev_api_server.run()

    container.shutdown_resources()


if __name__ == "__main__":
    main()
