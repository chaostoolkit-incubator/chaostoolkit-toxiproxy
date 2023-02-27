# -*- coding: utf-8 -*-
import unittest
from unittest import mock

import chaostoxi.toxic.actions as actions


class TestActionMethods(unittest.TestCase):
    @mock.patch("chaoslib.types.Configuration", spec_set=dict)
    @mock.patch("chaostoxi.toxiproxyapi.create_toxic")
    def test_create_latency_toxic(self, toxiproxyapi_mock, mockconfig):
        request_json = {
            "name": "toxic1",
            "type": "latency",
            "stream": "downstream",
            "toxicity": 1.0,
            "attributes": {"latency": 1000, "jitter": 0},
        }
        toxiproxyapi_mock.return_value = {
            "attributes": {"latency": 1000, "jitter": 0},
            "name": "toxic1",
            "type": "latency",
            "stream": "downstream",
            "toxicity": 1,
        }
        self.assertTrue(
            actions.create_latency_toxic(
                for_proxy="foobar",
                toxic_name="toxic1",
                latency=1000,
                configuration=mockconfig,
            )
        )
        toxiproxyapi_mock.assert_called_once_with(
            proxy_name="foobar", toxic_json=request_json, configuration=mockconfig
        )

    @mock.patch("chaoslib.types.Configuration", spec_set=dict)
    @mock.patch("chaostoxi.toxiproxyapi.create_toxic")
    def test_create_latency_toxic_with_jitter(self, toxiproxyapi_mock, mockconfig):
        request_json = {
            "name": "jittery",
            "type": "latency",
            "stream": "downstream",
            "toxicity": 1.0,
            "attributes": {"latency": 1000, "jitter": 300},
        }
        toxiproxyapi_mock.return_value = {"name": "jittery"}
        self.assertTrue(
            actions.create_latency_toxic(
                for_proxy="foobar",
                toxic_name="jittery",
                latency=1000,
                jitter=300,
                configuration=mockconfig,
            )
        )
        toxiproxyapi_mock.assert_called_once_with(
            proxy_name="foobar", toxic_json=request_json, configuration=mockconfig
        )

    @mock.patch("chaoslib.types.Configuration", spec_set=dict)
    @mock.patch("chaostoxi.toxiproxyapi.create_toxic")
    def test_create_bandwith_degradation_toxic(self, toxiproxyapi_mock, mockconfig):
        request_json = {
            "name": "bandwidth",
            "type": "bandwidth",
            "stream": "downstream",
            "toxicity": 1.0,
            "attributes": {"rate": 400},
        }
        toxiproxyapi_mock.return_value = {"name": "bandwidth"}
        self.assertTrue(
            actions.create_bandwith_degradation_toxic(
                for_proxy="foobar",
                toxic_name="bandwidth",
                rate=400,
                configuration=mockconfig,
            )
        )
        toxiproxyapi_mock.assert_called_once_with(
            proxy_name="foobar", toxic_json=request_json, configuration=mockconfig
        )

    @mock.patch("chaoslib.types.Configuration", spec_set=dict)
    @mock.patch("chaostoxi.toxiproxyapi.create_toxic")
    def test_create_slow_connection_close_toxic(self, toxiproxyapi_mock, mockconfig):
        request_json = {
            "name": "slowy",
            "type": "slow_close",
            "stream": "downstream",
            "toxicity": 1.0,
            "attributes": {"delay": 900},
        }
        toxiproxyapi_mock.return_value = {"name": "slowy"}
        self.assertTrue(
            actions.create_slow_connection_close_toxic(
                for_proxy="foobar",
                toxic_name="slowy",
                delay=900,
                configuration=mockconfig,
            )
        )
        toxiproxyapi_mock.assert_called_once_with(
            proxy_name="foobar", toxic_json=request_json, configuration=mockconfig
        )

    @mock.patch("chaoslib.types.Configuration", spec_set=dict)
    @mock.patch("chaostoxi.toxiproxyapi.create_toxic")
    def test_create_timeout_toxic(self, toxiproxyapi_mock, mockconfig):
        request_json = {
            "name": "timy",
            "type": "timeout",
            "stream": "downstream",
            "toxicity": 1.0,
            "attributes": {"timeout": 6900},
        }
        toxiproxyapi_mock.return_value = {"name": "timy"}
        self.assertTrue(
            actions.create_timeout_toxic(
                for_proxy="foobar",
                toxic_name="timy",
                timeout=6900,
                configuration=mockconfig,
            )
        )
        toxiproxyapi_mock.assert_called_once_with(
            proxy_name="foobar", toxic_json=request_json, configuration=mockconfig
        )

    @mock.patch("chaoslib.types.Configuration", spec_set=dict)
    @mock.patch("chaostoxi.toxiproxyapi.create_toxic")
    def test_create_slicer_toxic(self, toxiproxyapi_mock, mockconfig):
        request_json = {
            "name": "hamslice",
            "type": "slicer",
            "stream": "downstream",
            "toxicity": 1.0,
            "attributes": {"average_size": 6900, "size_variation": 20, "delay": 20},
        }
        toxiproxyapi_mock.return_value = {"name": "hamslice"}
        self.assertTrue(
            actions.create_slicer_toxic(
                for_proxy="foobar",
                toxic_name="hamslice",
                average_size=6900,
                size_variation=20,
                delay=20,
                configuration=mockconfig,
            )
        )
        toxiproxyapi_mock.assert_called_once_with(
            proxy_name="foobar", toxic_json=request_json, configuration=mockconfig
        )

    @mock.patch("chaoslib.types.Configuration", spec_set=dict)
    @mock.patch("chaostoxi.toxiproxyapi.create_toxic")
    def test_create_limiter_toxic(self, toxiproxyapi_mock, mockconfig):
        request_json = {
            "name": "limiteless",
            "type": "limit_data",
            "stream": "downstream",
            "toxicity": 1.0,
            "attributes": {"bytes": 100},
        }
        toxiproxyapi_mock.return_value = {"name": "limiteless"}
        self.assertTrue(
            actions.create_limiter_toxic(
                for_proxy="foobar",
                toxic_name="limiteless",
                bytes_limit=100,
                configuration=mockconfig,
            )
        )
        toxiproxyapi_mock.assert_called_once_with(
            proxy_name="foobar", toxic_json=request_json, configuration=mockconfig
        )

    @mock.patch("chaoslib.types.Configuration", spec_set=dict)
    @mock.patch("chaostoxi.toxiproxyapi.delete_toxic")
    def test_delete_toxic(self, toxiproxyapi_mock, mockconfig):
        toxiproxyapi_mock.return_value = True
        self.assertTrue(
            actions.delete_toxic(
                for_proxy="foobar", toxic_name="limiteless", configuration=mockconfig
            )
        )
