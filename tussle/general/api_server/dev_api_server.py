from tussle.general.api_server.flask_app import create_flask_app

class DevAPIServer:
    """
        This class is used for booting your local dev API server. Not to be used in production.
    """
    default_port = 5496

    def __init__(self, port=default_port):
        self.app = create_flask_app()
        self.port = port

    def run(self, port=default_port):
        self.port = port
        self.app.run(host='0.0.0.0', port=port)

