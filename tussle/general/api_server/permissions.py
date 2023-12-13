from tussle.general.api_server.auth import authenticate
from flask_restful import abort
from dependency_injector.wiring import Provide, inject

def authenticate_user(require_logged_in=True):
    def wrapper(api_func):
        @inject
        def wrapped(*args, config=Provide['config'], **kwargs):
            if kwargs is None:
                kwargs = {}

            if config['api']['force_auth_test_user'] is True:
                kwargs['user'] = 'test-user'
                return api_func(*args, **kwargs)

            user = authenticate()
            if user is None and require_logged_in:
                return abort(401)

            kwargs['user'] = user

            return api_func(*args, **kwargs)

        return wrapped
    return wrapper
