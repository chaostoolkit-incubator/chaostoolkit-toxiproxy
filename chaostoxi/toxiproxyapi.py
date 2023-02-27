# -*- coding: utf-8 -*-
from typing import Any, Dict

import requests
from chaoslib.types import Configuration
from logzero import logger


def create_proxy(
    proxy_json: Dict[str, str], configuration: Configuration
) -> Dict[str, Any]:
    url = build_proxies_baseUrl(configuration)
    response = requests.post(url, json=proxy_json)
    if not response.ok:
        logger.debug(
            "Unable to create proxy, response code {} with {}".format(
                response.status_code, response.text
            )
        )
        return None
    return response.json()


def modify_proxy(
    proxy_name: str, proxy_json: Dict[str, Any], configuration: Configuration
) -> Dict[str, Any]:
    base_url = build_proxies_baseUrl(configuration)
    url = "{}/{}".format(base_url, proxy_name)
    logger.debug("Toxiproxy server API located at {}".format(url))
    response = requests.post(url, json=proxy_json)
    if not response.ok:
        logger.debug(
            "Unable to modify proxy, response code {} with {}".format(
                response.status_code, response.text
            )
        )
        return None
    return response.json()


def delete_proxy(proxy_name: str, configuration: Configuration) -> None:
    base_url = build_proxies_baseUrl(configuration)
    url = "{}/{}".format(base_url, proxy_name)
    try:
        response = requests.delete(url)
        if not response.ok:
            logger.warning(
                "Unable to remove proxy from chaostoolkit with: {} received: "
                "{}".format(url, response.status_code)
            )
    except Exception:
        logger.warning("Unable to remove proxy from chaostoolkit with: {}".format(url))


def read_proxy(proxy_name: str, configuration: Configuration) -> Dict[str, Any]:
    base_url = build_proxies_baseUrl(configuration)
    url = "{}/{}".format(base_url, proxy_name)
    response = requests.get(url)
    if not response.ok:
        return None
    return response.json()


def create_toxic(
    proxy_name: str, toxic_json: Dict[str, Any], configuration: Configuration
) -> Dict[str, Any]:
    base_url = build_proxies_baseUrl(configuration)
    url = "{}/{}/toxics".format(base_url, proxy_name)
    response = requests.post(url, json=toxic_json)
    if not response.ok:
        logger.error("Unable to create toxic for proxy: {}".format(proxy_name))
        return None
    return response.json()


def delete_toxic(proxy_name: str, toxic_name, configuration: Configuration) -> int:
    base_url = build_proxies_baseUrl(configuration)
    url = "{}/{}/toxics/{}".format(base_url, proxy_name, toxic_name)
    response = requests.delete(url)
    return response.ok


def reset(configuration: Configuration) -> int:
    base_url = build_baseUrl(configuration)
    url = "{}/reset".format(base_url)
    response = requests.post(url)
    return response.ok


def build_baseUrl(configuration: Configuration) -> str:
    """
    Constructs toxiproxy baseURL using variables from configuration.
    """
    toxiproxy_host = configuration.get("toxiproxy_host")
    toxiproxy_port = configuration.get("toxiproxy_port")
    toxiproxy_url = configuration.get("toxiproxy_url")
    if not toxiproxy_url:
        if not toxiproxy_port:
            toxiproxy_port = 8474
        url = "http://{}:{}".format(toxiproxy_host, toxiproxy_port)
    else:
        url = toxiproxy_url
    logger.debug("Calculated toxiproxy URL is: {}".format(url))
    return url


def build_proxies_baseUrl(configuration: Configuration) -> str:
    return build_baseUrl(configuration) + "/proxies"
