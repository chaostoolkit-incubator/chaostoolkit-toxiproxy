# -*- coding: utf-8 -*-
from chaoslib.types import Configuration

from logzero import logger
import chaostoxi.toxiproxyapi as toxiproxyapi

__all__ = ["proxy_exist", "get_proxy_attribute"]


def proxy_exist(proxy_name: str, configuration: Configuration = None):
    """
    Returns True of False if a given proxy exists.
    """
    proxy = toxiproxyapi.read_proxy(proxy_name=proxy_name,
                                    configuration=configuration)
    if proxy:
        name = proxy["name"]
        logger.debug("Received a proxy with name: {} and expecting {}".format(
            name, proxy_name))
        return name == proxy_name
    logger.debug("Proxy with name {} does not seem to exist".format(proxy_name))
    return False


def get_proxy_attribute(proxy_name: str, attribute: str,
                        configuration: Configuration = None):
    """
    Returns an attribute of a specified proxy.
    """
    proxy = toxiproxyapi.read_proxy(proxy_name=proxy_name,
                                    configuration=configuration)
    if proxy:
        attribute = proxy[attribute]
        logger.debug(
            "Found proxy object for {} and attribute resolved to {}".format(
                proxy_name, attribute))
        return attribute
    return None
