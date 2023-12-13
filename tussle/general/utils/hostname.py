import os
import socket


def get_host_name():
    """
    This will return the hostname of the machine that is running this code.

    :return:
    """
    host_name = os.environ.get('HOSTNAME')
    if host_name is None:
        host_name = os.environ.get('COMPUTERNAME')
    if host_name is None:
        host_name = os.environ.get('HOST')

    if host_name is None:
        return socket.gethostname()
    else:
        return host_name
