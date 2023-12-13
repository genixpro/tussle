# This script is used for booting the API server within gunicorn
import cProfile
import pstats


def internal_main():
    from tussle.application import create_and_initialization_application_container
    from tussle.general.api_server.gunicorn_api_server import GunicornApiServer

    container = create_and_initialization_application_container()

    # Create the gunicorn app to serve the flask app.
    app = GunicornApiServer()

    # app.run()

    # container.shutdown_resources()


def main():
    cProfile.run('import tussle.general.bin.profile_startup_time; tussle.general.bin.profile_startup_time.internal_main()', 'restats')

    p = pstats.Stats('restats')
    p.strip_dirs().sort_stats('cumtime').print_stats(0.05)


if __name__ == "__main__":
    main()
