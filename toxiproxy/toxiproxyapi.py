# -*- coding: utf-8 -*-
import requests

from chaoslib.types import Configuration
from logzero import logger
from typing import Dict


def create_proxy(proxy_json: Dict[str, str], configuration: Configuration):
    url = build_baseUrl(configuration)
    response = requests.post(url, json=proxy_json)
    if not response.ok:
        logger.debug("Unable to create proxy, response code {} with {}".format(response.status_code, response.text))
        return None
    return response.json()


def modify_proxy(proxy_name: str, proxy_json: Dict[str, any], configuration: Configuration):
    base_url = build_baseUrl(configuration)
    url = "{}/{}".format(base_url, proxy_name)
    logger.debug("Toxiproxy server API located at {}".format(url))
    response = requests.post(url, json=proxy_json)
    if response.ok:
        logger.debug("Unable to create proxy, response code {} with {}".format(response.status_code, response.text))
        return None
    return response.json()


def delete_proxy(proxy_name: str, configuration: Configuration):
    base_url = build_baseUrl(configuration)
    url = "{}/{}".format(base_url, proxy_name)
    try:
        response = requests.delete(url)
        if not response.ok:
            logger.warning("Unable to remove proxy from chaostoolkit with: {} received: {}".format(url, response.status_code))
    except Exception:
        logger.warning("Unable to remove proxy from chaostoolkit with: {}".format(url))


def read_proxy(proxy_name: str, configuration: Configuration):
    base_url = build_baseUrl(configuration)
    url = "{}/{}".format(base_url, proxy_name)
    response = requests.get(url)
    if not response.ok:
        return None
    return response.json()


def create_toxic(proxy_name: str, toxic_json: Dict[str, any], configuration: Configuration):
    base_url = build_baseUrl(configuration)
    url = "{}/{}/toxics".format(base_url, proxy_name)
    response = requests.post(url, json=toxic_json)
    if not response.ok:
        logger.error("Unable to create toxic for proxy: {}".format(proxy_name))
        return None
    return response.json()


def delete_toxic(proxy_name: str, toxic_name, configuration: Configuration):
    base_url = build_baseUrl(configuration)
    url = "{}/{}/toxics/{}".format(base_url, proxy_name, toxic_name)
    response = requests.delete(url)
    return response.ok


def build_baseUrl(configuration: Configuration):
    toxiproxy_host = configuration.get("toxiproxy_host")
    toxiproxy_port = configuration.get("toxiproxy_port")
    if not toxiproxy_port:
        toxiproxy_port = 8474
    url = "http://{}:{}/proxies".format(toxiproxy_host, toxiproxy_port)
    logger.debug("Calculated toxiproxy URL is: {}".format(url))
    return url
