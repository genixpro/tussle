from tussle.completions.providers.lorem_ipsum_completion_provider import LoremIpsumCompletionProvider
from tussle.general.config.config import determine_environment, load_cloud_configuration
from tussle.general.logger import get_logger

logger = get_logger("test_initialization")
global_test_application_container = None

def initialize_container_for_tests():
    global global_test_application_container
    if global_test_application_container is not None:
        return global_test_application_container

    from tussle.application import Application

    global_test_application_container = Application()

    environment = determine_environment()

    logger.info(f"Initializing the DI container for tests with environment {environment}")

    # CICD environment uses a slightly different configuration then local environment.
    if environment == 'cicd':
        global_test_application_container.config.override(load_cloud_configuration('cicd'))
    elif environment == 'internal_only':
        global_test_application_container.config.override(load_cloud_configuration('internal_only'))
    else:
        # Ensure that the container has been loaded with the testing configuration,
        # no matter what environment we are running in.
        global_test_application_container.config.override(load_cloud_configuration('testing'))

    # Make sure the container has the correct overrides in place for testing.
    setup_test_overrides_if_needed(global_test_application_container)

    if environment != "internal_only":
        global_test_application_container.init_resources()
    global_test_application_container.wire(packages=['tussle'])

    return global_test_application_container


def setup_test_overrides_if_needed(container):
    if not container.config()['openai']['enabled']:
        # Make sure the default completion provider is replaced with the lorem ipsum.
        # This ensures that the tests don't result in a ton of OpenAI API calls being
        # made.
        container.completion_provider.override(
            LoremIpsumCompletionProvider()
        )
