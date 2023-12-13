from jwcrypto.jws import JWK, InvalidJWSSignature, InvalidJWSObject, InvalidJWSOperation
from jwcrypto.jwt import JWT
from jwcrypto.common import json_decode
from tussle.general.config.config import load_cloud_configuration
import json
import pkg_resources
import flask
import functools

@functools.cache
def load_auth0_key():
    config_data = load_cloud_configuration()
    auth_key = json.loads(pkg_resources.resource_string("tussle", config_data['auth0']['key_file']))
    return auth_key

def authenticate(return_all_claims=False):
    config_data = load_cloud_configuration()

    if 'WWW-Authenticate' in flask.request.headers:
        token = flask.request.headers['WWW-Authenticate']
    elif 'token' in flask.request.args:
        token = flask.request.args['token']
    else:
        return None

    api_url = config_data['auth0']['api_url']
    auth_domain = config_data['auth0']['domain']
    auth_key = load_auth0_key()

    try:
        key = JWK(**auth_key)

        token = JWT(jwt=token,
                    key=key,
                    check_claims={
                        'iss': f"https://{auth_domain}/",
                        'aud': api_url
                    },
                    algs=['RS256'])

        claims = json_decode(token.claims)

        if return_all_claims:
            return claims['sub'], claims
        else:
            return claims['sub']
    except ValueError as e:
        print(e)
        return None
    except InvalidJWSSignature as e:
        print(e)
        return None
    except InvalidJWSObject as e:
        print(e)
        return None
    except InvalidJWSOperation as e:
        print(e)
        return None

def is_admin():
    user, claims = authenticate(return_all_claims=True)
    return claims['https://app.tussle.com/admin']

