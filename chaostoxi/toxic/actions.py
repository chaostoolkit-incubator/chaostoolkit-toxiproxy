# -*- coding: utf-8 -*-
from chaoslib.types import Configuration

from logzero import logger
import chaostoxi.toxiproxyapi as toxiproxyapi
from typing import Dict


def delete_toxic(for_proxy: str, toxic_name: str,
                 configuration: Configuration = None):
    return toxiproxyapi.delete_toxic(proxy_name=for_proxy,
                                     toxic_name=toxic_name,
                                     configuration=configuration)


def create_toxic(for_proxy: str, toxic_name: str, toxic_type: str,
                 stream: str = "downstream", toxicity: float = 1.0,
                 attributes: Dict[str, any] = None,
                 configuration: Configuration = None):
    logger.info("Creating toxy {} for proxy {} with type: {} as a {} with toxicity {} and attributes {}"
                .format(toxic_name, for_proxy, toxic_type, stream,
                        str(toxicity), str(attributes)))
    json = {"name": toxic_name,
            "type": toxic_type,
            "stream": stream,
            "toxicity": toxicity,
            "attributes": attributes
            }
    logger.debug("json format for toxy creation: {}".format(json))
    toxic = toxiproxyapi.create_toxic(proxy_name=for_proxy, toxic_json=json,
                                      configuration=configuration)
    return toxic['name'] == toxic_name


def create_latency_toxic(for_proxy: str, toxic_name: str, latency: int,
                         jitter: int = 0, configuration: Configuration = None):
    attributes = {
        "latency": latency,
        "jitter": jitter
    }
    return create_toxic(for_proxy=for_proxy, toxic_name=toxic_name,
                        toxic_type='latency', attributes=attributes,
                        configuration=configuration)


def create_bandwith_degradation_toxic(for_proxy: str, toxic_name: str,
                                      rate: int,
                                      configuration: Configuration = None):
    attributes = {
        "rate": rate
    }
    return create_toxic(for_proxy=for_proxy, toxic_name=toxic_name,
                        toxic_type='bandwidth', attributes=attributes,
                        configuration=configuration)


def create_slow_connection_close_toxic(for_proxy: str, toxic_name: str,
                                       delay: int,
                                       configuration: Configuration = None):
    attributes = {
        "delay": delay
    }
    return create_toxic(for_proxy=for_proxy, toxic_name=toxic_name,
                        toxic_type='slow_close', attributes=attributes,
                        configuration=configuration)


def create_timeout_toxic(for_proxy: str, toxic_name: str, timeout: int,
                         configuration: Configuration = None):
    attributes = {
        "timeout": timeout
    }
    return create_toxic(for_proxy=for_proxy, toxic_name=toxic_name,
                        toxic_type='timeout', attributes=attributes,
                        configuration=configuration)


def create_slicer_toxic(for_proxy: str, toxic_name: str, average_size: int,
                        size_variation: int, delay: int,
                        configuration: Configuration = None):
    attributes = {
        "average_size": average_size,
        "size_variation": size_variation,
        "delay": delay
    }
    return create_toxic(for_proxy=for_proxy, toxic_name=toxic_name,
                        toxic_type='slicer', attributes=attributes,
                        configuration=configuration)


def create_limiter_toxic(for_proxy: str, toxic_name: str, bytes_limit: int,
                         configuration: Configuration = None):
    attributes = {
        "bytes": bytes_limit
    }
    return create_toxic(for_proxy=for_proxy, toxic_name=toxic_name,
                        toxic_type='limit_data', attributes=attributes,
                        configuration=configuration)
