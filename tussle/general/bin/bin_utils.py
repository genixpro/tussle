import pkgutil
import requests
import json
import pkg_resources


def import_everything_tussle():
    """
    This ensures that all the tussle packages have been imported,
    so that if there are functions getting registered into global registries,
    they will get registered.

    :return:
    """
    __all__ = []
    for loader, module_name, is_pkg in pkgutil.walk_packages(["tussle"]):
        __all__.append(module_name)
        _module = loader.find_module(module_name).load_module(module_name)
        globals()[module_name] = _module


