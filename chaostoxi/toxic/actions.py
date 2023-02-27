# -*- coding: utf-8 -*-
from typing import Any, Dict

from chaoslib.types import Configuration
from logzero import logger

import chaostoxi.toxiproxyapi as toxiproxyapi

__all__ = [
    "delete_toxic",
    "create_toxic",
    "create_latency_toxic",
    "create_bandwith_degradation_toxic",
    "create_slow_connection_close_toxic",
    "create_timeout_toxic",
    "create_slicer_toxic",
    "create_limiter_toxic",
]


def delete_toxic(for_proxy: str, toxic_name: str, configuration: Configuration = None):
    """
    Deletes the a given toxic.
    """
    return toxiproxyapi.delete_toxic(
        proxy_name=for_proxy, toxic_name=toxic_name, configuration=configuration
    )


def create_toxic(
    for_proxy: str,
    toxic_name: str,
    toxic_type: str,
    stream: str = "downstream",
    toxicity: float = 1.0,
    attributes: Dict[str, Any] = None,  # noqa: E251
    configuration: Configuration = None,  # noqa: E251
) -> bool:
    """
    Allows you to create any of the supported types of toxics
    with their attributes.
    """
    logger.info(
        "Creating toxy {} for proxy {} with type: {} as a {} with toxicity {} "
        "and attributes {}".format(
            toxic_name, for_proxy, toxic_type, stream, str(toxicity), str(attributes)
        )
    )
    json = {
        "name": toxic_name,
        "type": toxic_type,
        "stream": stream,
        "toxicity": toxicity,
        "attributes": attributes,
    }
    logger.debug("json format for toxy creation: {}".format(json))
    toxic = toxiproxyapi.create_toxic(
        proxy_name=for_proxy, toxic_json=json, configuration=configuration
    )
    return toxic["name"] == toxic_name


def create_latency_toxic(
    for_proxy: str,
    toxic_name: str,
    latency: int,
    jitter: int = 0,
    configuration: Configuration = None,
) -> Dict[str, Any]:
    """
    Add a delay to all data going through the proxy using a downstream
    with a toxicity of 100%.
    """
    attributes = {"latency": latency, "jitter": jitter}
    return create_toxic(
        for_proxy=for_proxy,
        toxic_name=toxic_name,
        toxic_type="latency",
        attributes=attributes,
        configuration=configuration,
    )


def create_bandwith_degradation_toxic(
    for_proxy: str, toxic_name: str, rate: int, configuration: Configuration = None
) -> Dict[str, Any]:
    """
    Limit the bandwith of a  downstream connection with a toxicity of 100%.
    """
    attributes = {"rate": rate}
    return create_toxic(
        for_proxy=for_proxy,
        toxic_name=toxic_name,
        toxic_type="bandwidth",
        attributes=attributes,
        configuration=configuration,
    )


def create_slow_connection_close_toxic(
    for_proxy: str, toxic_name: str, delay: int, configuration: Configuration = None
) -> Dict[str, Any]:
    """
    Limit the bandwith of a  downstream connection with a toxicity of 100%.
    """
    attributes = {"delay": delay}
    return create_toxic(
        for_proxy=for_proxy,
        toxic_name=toxic_name,
        toxic_type="slow_close",
        attributes=attributes,
        configuration=configuration,
    )


def create_timeout_toxic(
    for_proxy: str, toxic_name: str, timeout: int, configuration: Configuration = None
) -> Dict[str, Any]:
    """
    Generate as downstream delayed TCP close with a toxicity of 100%.
    """
    attributes = {"timeout": timeout}
    return create_toxic(
        for_proxy=for_proxy,
        toxic_name=toxic_name,
        toxic_type="timeout",
        attributes=attributes,
        configuration=configuration,
    )


def create_slicer_toxic(
    for_proxy: str,
    toxic_name: str,
    average_size: int,
    size_variation: int,
    delay: int,
    configuration: Configuration = None,
) -> Dict[str, Any]:
    """
    Slices TCP data up into small bits, optionally adding a delay between
    each sliced "packet" with a toxicity of 100%.
    """
    attributes = {
        "average_size": average_size,
        "size_variation": size_variation,
        "delay": delay,
    }
    return create_toxic(
        for_proxy=for_proxy,
        toxic_name=toxic_name,
        toxic_type="slicer",
        attributes=attributes,
        configuration=configuration,
    )


def create_limiter_toxic(
    for_proxy: str,
    toxic_name: str,
    bytes_limit: int,
    configuration: Configuration = None,
) -> Dict[str, Any]:
    """
    Closes connections when transmitted data after the limit,
    sets it up as a dowsntream, 100% toxicity.
    """
    attributes = {"bytes": bytes_limit}
    return create_toxic(
        for_proxy=for_proxy,
        toxic_name=toxic_name,
        toxic_type="limit_data",
        attributes=attributes,
        configuration=configuration,
    )
