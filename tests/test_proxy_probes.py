# -*- coding: utf-8 -*-
import toxiproxy.proxy.probes as probes
import unittest
from unittest import mock


class TestProbesMethods (unittest.TestCase):

    @mock.patch('chaoslib.types.Configuration', spec_set=dict)
    @mock.patch('toxiproxy.toxiproxyapi.read_proxy')
    def test_proxy_exist_success(self, toxiproxyapi_mock, mockconfig):
        toxiproxyapi_mock.return_value = {
                "name": "testproxy",
                "listen": "0.0.0.0:6660",
                "upstream": "10.28.188.118:6040"
        }
        self.assertTrue(probes.proxy_exist(proxy_name="testproxy", configuration=mockconfig))

    @mock.patch('chaoslib.types.Configuration', spec_set=dict)
    @mock.patch('toxiproxy.toxiproxyapi.read_proxy')
    def test_proxy_exist_weird_failure(self, toxiproxyapi_mock, mockconfig):
        # Why would we get a different name??
        toxiproxyapi_mock.return_value = {
                "name": "weird",
                "listen": "0.0.0.0:6660",
                "upstream": "10.28.188.118:6040"
        }
        self.assertFalse(probes.proxy_exist(proxy_name="testproxy", configuration=mockconfig))

    @mock.patch('chaoslib.types.Configuration', spec_set=dict)
    @mock.patch('toxiproxy.toxiproxyapi.read_proxy')
    def test_proxy_exist_failure(self, toxiproxyapi_mock, mockconfig):
        toxiproxyapi_mock.return_value = None
        self.assertFalse(probes.proxy_exist(proxy_name="testproxy", configuration=mockconfig))

    @mock.patch('chaoslib.types.Configuration', spec_set=dict)
    @mock.patch('toxiproxy.toxiproxyapi.read_proxy')
    def test_get_proxy_attribute(self, toxiproxyapi_mock, mockconfig):
        # Why would we get a different name??
        toxiproxyapi_mock.return_value = {
                "name": "someproxy",
                "listen": "0.0.0.0:6660",
                "upstream": "10.28.188.118:6040"
        }
        ret_attribute = probes.get_proxy_attribute(proxy_name="testproxy", attribute="listen", configuration=mockconfig)
        self.assertEquals(ret_attribute, "0.0.0.0:6660")
