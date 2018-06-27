# -*- coding: utf-8 -*-
import toxiproxy.proxy.actions as actions
import unittest
from unittest import mock
from os import environ


class TestActionMethods (unittest.TestCase):

    @mock.patch('chaoslib.types.Configuration', spec_set=dict)
    @mock.patch('toxiproxy.toxiproxyapi.create_proxy')
    def test_create_proxy_success(self, toxiproxyapi_mock, mockconfig):
        toxiproxyapi_mock.return_value = {
                "name": "aproxy",
                "listen": "0.0.0.0:6660",
                "upstream": "10.28.188.118:6040"
        }
        self.assertTrue(actions.create_proxy(proxy_name="proxyone", listen_port=0, upstream_host="127.0.0.1",
                                             upstream_port="8080", configuration=mockconfig))
        # the action has the side effect of adding the proxy port into the config with the key proxyname_PORT
        mockconfig.__setitem__.assert_called_once_with('proxyone_PORT', '6660')
        self.assertTrue(environ['proxyone_PORT'], '6660')

    @mock.patch('chaoslib.types.Configuration', spec_set=dict)
    @mock.patch('toxiproxy.toxiproxyapi.create_proxy')
    def test_create_proxy_from_env_success(self, toxiproxyapi_mock, mockconfig):
        toxiproxyapi_mock.return_value = {
                "name": "aproxy",
                "listen": "0.0.0.0:8900",
                "upstream": "10.28.188.118:6040"
        }
        environ['RANDOM_HOST_KEY'] = '10.28.188.118'
        environ['RANDOM_PORT_KEY'] = '6040'

        self.assertTrue(actions.create_proxy(proxy_name="createproxy", listen_port=0, upstream_host="env:RANDOM_HOST_KEY",
                                             upstream_port="env:RANDOM_PORT_KEY", configuration=mockconfig))
        # the action has the side effect of adding the proxy port into the config with the key proxyname_PORT
        mockconfig.__setitem__.assert_called_once_with('createproxy_PORT', '8900')
        self.assertTrue(environ['createproxy_PORT'], '8900')

    @mock.patch('chaoslib.types.Configuration', spec_set=dict)
    @mock.patch('toxiproxy.toxiproxyapi.create_proxy')
    def test_create_proxy_from_env_failure(self, toxiproxyapi_mock, mockconfig):
        toxiproxyapi_mock.return_value = {
                "name": "aproxy",
                "listen": "0.0.0.0:6660",
                "upstream": "10.28.188.118:6040"
        }
        with self.assertRaises(KeyError):
            actions.create_proxy(proxy_name="aproxy", listen_port=0, upstream_host="env:DONT_EXISTS",
                                 upstream_port="env:DONT_EXISTS", configuration=mockconfig)

    @mock.patch('chaoslib.types.Configuration', spec_set=dict)
    @mock.patch('toxiproxy.toxiproxyapi.create_proxy')
    def test_create_proxy_http_error(self, toxiproxyapi_mock, mockconfig):
        toxiproxyapi_mock.return_value = None
        with self.assertRaises(AssertionError):
            actions.create_proxy(proxy_name="failproxy", listen_port=0, upstream_host="127.0.0.1",
                                 upstream_port="8080", configuration=mockconfig)

    @mock.patch('chaoslib.types.Configuration', spec_set=dict)
    @mock.patch('toxiproxy.toxiproxyapi.create_proxy')
    def test_create_proxy_bad_data(self, toxiproxyapi_mock, mockconfig):
        toxiproxyapi_mock.return_value = {
                "name": "baddataproxy",
                "listen": "baddadahere",
                "upstream": "10.28.188.118:6040"
        }
        with self.assertRaises(AssertionError):
            actions.create_proxy(proxy_name="baddataproxy", listen_port=0, upstream_host="127.0.0.1",
                                 upstream_port="8080", configuration=mockconfig)

    @mock.patch('chaoslib.types.Configuration', spec_set=dict)
    @mock.patch('toxiproxy.toxiproxyapi.delete_proxy', autospec=True)
    def test_delete_proxy(self, toxiproxyapi_mock, mockconfig):
        toxiproxyapi_mock.return_value = True
        self.assertTrue(actions.delete_proxy("some_proxy", mockconfig))

    @mock.patch('chaoslib.types.Configuration', spec_set=dict)
    @mock.patch('toxiproxy.toxiproxyapi.delete_proxy', autospec=True)
    def test_delete_proxy_fail(self, toxiproxyapi_mock, mockconfig):
        toxiproxyapi_mock.return_value = False
        self.assertFalse(actions.delete_proxy("some_proxy", mockconfig))

    @mock.patch('chaoslib.types.Configuration', spec_set=dict)
    @mock.patch('toxiproxy.toxiproxyapi.modify_proxy')
    def test_modify_proxy_everything(self, toxiproxyapi_mock, mockconfig):
        modify_json = {
            "listen": "127.0.0.1:6666",
            "upstream": "10.10.10.10:1234",
            "enabled": True
        }
        toxiproxyapi_mock.return_value = {
                "name": "change_all",
                "listen": "127.0.0.1:6666",
                "upstream": "10.28.188.118:6040"
        }
        self.assertTrue(actions.modify_proxy(proxy_name="change_all", listen_address="127.0.0.1:6666", upstream_address="10.10.10.10:1234",
                                             enabled=True, configuration=mockconfig))
        toxiproxyapi_mock.assert_called_once_with(proxy_name="change_all", proxy_json=modify_json, configuration=mockconfig)
        # the action has the side effect of adding the proxy port into the config with the key proxyname_PORT
        mockconfig.__setitem__.assert_called_once_with('change_all_PORT', '6666')

    @mock.patch('chaoslib.types.Configuration', spec_set=dict)
    @mock.patch('toxiproxy.toxiproxyapi.modify_proxy')
    def test_modify_proxy_listen(self, toxiproxyapi_mock, mockconfig):
        modify_json = {
            "listen": "0.0.0.0:43409",
        }
        toxiproxyapi_mock.return_value = {
            "name": "change_one",
            "listen": "[::]:43409",
            "upstream": "10.28.188.118:6040",
            "enabled": True,
            "toxics": []
        }
        self.assertTrue(actions.modify_proxy(proxy_name="change_one", listen_address="0.0.0.0:43409", configuration=mockconfig))
        toxiproxyapi_mock.assert_called_once_with(proxy_name="change_one", proxy_json=modify_json, configuration=mockconfig)
        # the action has the side effect of adding the proxy port into the config with the key proxyname_PORT
        mockconfig.__setitem__.assert_called_once_with('change_one_PORT', '43409')

    @mock.patch('chaoslib.types.Configuration', spec_set=dict)
    @mock.patch('toxiproxy.toxiproxyapi.modify_proxy')
    def test_modify_proxy_upstream(self, toxiproxyapi_mock, mockconfig):
        modify_json = {
            "upstream": "10.10.10.10:1234",
        }
        toxiproxyapi_mock.return_value = {
                "name": "change_two",
                "listen": "127.0.0.1:6666",
                "upstream": "10.28.188.118:6040"
        }
        self.assertTrue(actions.modify_proxy(proxy_name="change_two", upstream_address="10.10.10.10:1234", configuration=mockconfig))
        toxiproxyapi_mock.assert_called_once_with(proxy_name="change_two", proxy_json=modify_json, configuration=mockconfig)
        # the action has the side effect of adding the proxy port into the config with the key proxyname_PORT
        mockconfig.__setitem__.assert_called_once_with('change_two_PORT', '6666')

    @mock.patch('chaoslib.types.Configuration', spec_set=dict)
    @mock.patch('toxiproxy.toxiproxyapi.modify_proxy')
    def test_enable_proxy(self, toxiproxyapi_mock, mockconfig):
        modify_json = {
            "enabled": True
        }
        toxiproxyapi_mock.return_value = {
                "name": "enableproxy",
                "listen": "127.0.0.1:6666",
                "upstream": "10.28.188.118:6040"
        }
        self.assertTrue(actions.enable_proxy(proxy_name="enableproxy", configuration=mockconfig))
        toxiproxyapi_mock.assert_called_once_with(proxy_name="enableproxy", proxy_json=modify_json, configuration=mockconfig)
        # the action has the side effect of adding the proxy port into the config with the key proxyname_PORT
        mockconfig.__setitem__.assert_called_once_with('enableproxy_PORT', '6666')

    @mock.patch('chaoslib.types.Configuration', spec_set=dict)
    @mock.patch('toxiproxy.toxiproxyapi.modify_proxy')
    def test_disable_proxy(self, toxiproxyapi_mock, mockconfig):
        modify_json = {
            "enabled": False
        }
        toxiproxyapi_mock.return_value = {
                "name": "disable_proxy",
                "listen": "127.0.0.1:6666",
                "upstream": "10.28.188.118:6040"
        }
        self.assertTrue(actions.disable_proxy(proxy_name="disable_proxy", configuration=mockconfig))
        toxiproxyapi_mock.assert_called_once_with(proxy_name="disable_proxy", proxy_json=modify_json, configuration=mockconfig)
        # the action has the side effect of adding the proxy port into the config with the key proxyname_PORT
        mockconfig.__setitem__.assert_called_once_with('disable_proxy_PORT', '6666')
