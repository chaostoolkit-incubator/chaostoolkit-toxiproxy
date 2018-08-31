# -*- coding: utf-8 -*-
from chaoslib.types import Configuration

from os import environ
from logzero import logger
import chaostoxi.toxiproxyapi as toxiproxyapi


__all__ = ["create_proxy", "disable_proxy", "enable_proxy", "modify_proxy",
           "delete_proxy"]


def create_proxy(proxy_name: str, upstream_host: str, upstream_port: int,
                 listen_host: str = '0.0.0.0', listen_port: int = 0,
                 enabled: bool = True, configuration: Configuration = None):
    """
    Creates a proxy to which toxics can be added.
    """
    listen_address = "{}:{}".format(listen_host, str(listen_port))
    upstream_host = value_from_environment_if_exists(upstream_host)
    upstream_port = value_from_environment_if_exists(upstream_port)
    upstream_address = "{}:{}".format(upstream_host, str(upstream_port))

    json = {
        "name": proxy_name,
        "listen": listen_address,
        "upstream": upstream_address,
        "enabled": enabled
    }
    logger.debug("Creating proxy with the following configuration: {}".format(
        str(json)))
    proxy = toxiproxyapi.create_proxy(proxy_json=json,
                                      configuration=configuration)
    if not proxy:
        raise AssertionError
    return_port = proxy["listen"].split(":")[-1]
    if not return_port.isdigit():
        logger.error("Unable to parse port from proxy reponse {}".format(proxy))
        raise AssertionError
    logger.debug("toxyproxy ready listening on port: {}".format(return_port))
    config_key = "{}_PORT".format(proxy_name)
    entry = return_port
    configuration[config_key] = entry
    environ[config_key] = entry
    logger.debug("toxyproxy port added to configuration object: {}".format(
        return_port))
    return True


def disable_proxy(proxy_name: str, configuration: Configuration = None):
    """
    Disables the proxy, this is useful to simulate a proxied service being down.
    """
    return modify_proxy(proxy_name=proxy_name, enabled=False,
                        configuration=configuration)


def enable_proxy(proxy_name: str, configuration: Configuration = None):
    """
    Enables a disabled proxy.
    """
    return modify_proxy(proxy_name=proxy_name, enabled=True,
                        configuration=configuration)


def modify_proxy(proxy_name: str, listen_address: str = None,
                 upstream_address: str = None, enabled: bool = None,
                 configuration: Configuration = None):
    """
    Modify the configuration of a given proxy.
    Useful to change the upstream configiuration.
    Only arguments supplied result in modification of the proxy.
    """
    json = {}
    if listen_address is not None:
        json['listen'] = listen_address
    if upstream_address is not None:
        json['upstream'] = upstream_address
    if enabled is not None:
        json['enabled'] = enabled
    logger.debug("Modifying proxy with the following data: {}".format(str(json)))
    proxy = toxiproxyapi.modify_proxy(proxy_name=proxy_name, proxy_json=json,
                                      configuration=configuration)
    if not proxy:
        logger.error("Unable to modify proxy {}".format(proxy_name))
        raise AssertionError
    return_port = proxy["listen"].split(":")[-1]
    config_key = "{}_PORT".format(proxy_name)
    entry = return_port
    configuration[config_key] = entry
    environ[config_key] = entry
    return True


def delete_proxy(proxy_name: str, configuration: Configuration = None):
    """
    Removes the proxy from the system.
    """
    return toxiproxyapi.delete_proxy(proxy_name=proxy_name,
                                     configuration=configuration)


def value_from_environment_if_exists(key: str):
    if key.startswith("env:"):
        env_key = key[4:]
        logger.debug("Resolving from environment variable: {}".format(env_key))
        return environ[env_key]
    return key
