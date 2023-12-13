import logging
from colors import italic, yellow, white

global_root_logger = None
global_default_log_level = logging.INFO


def create_global_logger(default_log_level=logging.INFO):
    """
    This is used to initialize the global logger object.
    :return:
    """
    global global_root_logger
    global global_default_log_level
    global_default_log_level = default_log_level

    time_format = italic(white('%(asctime)s'))
    process_thread_format = italic(white('[%(process)s.%(threadName)s]'))
    filename_line_func_format = italic(yellow('%(filename)s:%(lineno)d:%(funcName)s'))
    message_format = '%(message)s'

    logging.basicConfig(
        format=f'{time_format} {process_thread_format} {filename_line_func_format}: {message_format}',
        datefmt='%H:%M:%S'
    )
    global_root_logger = logging.getLogger("tussle")
    global_root_logger.setLevel(global_default_log_level)

    # Ensure the werkzeug module gets the same log level
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(global_default_log_level)

    # Ensure the celery module gets the same log level
    celery_logger = logging.getLogger("celery")
    celery_logger.setLevel(global_default_log_level)

    global_root_logger.info(f"Initialized global logger with default log level {global_default_log_level}")

    return global_root_logger

def get_global_default_log_level():
    """
    This is used to return the current default global log level
    :return:
    """
    global global_default_log_level
    return global_default_log_level


def get_logger(component_name):
    """
    This is used to get a logger object for a specific component.
    :param component_name:
    :return:
    """
    global global_root_logger
    if not global_root_logger:
        create_global_logger()

    subLogger = global_root_logger.getChild(component_name)
    subLogger.setLevel(global_default_log_level)
    return subLogger
