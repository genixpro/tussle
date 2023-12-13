import os
import json
import functools
import pkg_resources

def load_internal_only_configuration():
    internal_only_configuration_file_path = pkg_resources.resource_filename('tussle', 'general/config/configs/internal_only.json')
    with open(internal_only_configuration_file_path, 'rt') as f:
        data = json.load(f)
    return data

def determine_environment():
    environment = os.getenv("TUSSLE_ENV")

    if environment is None or environment == "":
        environment = "development"

    return environment

def configure_environment_variables():
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'notional-clover-408014'
    return os.environ


@functools.cache
def load_cloud_configuration(environment=None):
    if environment is None:
        environment = determine_environment()

    if environment == 'internal_only':
        config_data =  load_internal_only_configuration()
    else:
        config_data = get_environment_config_from_gcs_secrets(environment)

    return config_data


def get_environment_config_from_gcs_secrets(environment):
    from google.cloud import secretmanager

    client = secretmanager.SecretManagerServiceClient()
    # Build the resource name of the secret.
    name = client.secret_version_path("tussle", f"{environment}_environment_config", "latest")
    response = client.access_secret_version(request={"name": name})
    data = json.loads(response.payload.data.decode("UTF-8"))
    return data






