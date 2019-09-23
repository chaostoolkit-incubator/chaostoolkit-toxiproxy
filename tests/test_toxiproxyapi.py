import chaostoxi.toxiproxyapi as toxiproxyapi
import unittest


class TestActionMethods (unittest.TestCase):

    def test_build_baseUrl(self):
        configuration = {"toxiproxy_host": "localhost", "toxiproxy_port": "8888"}
        expected_baseUrl = "http://localhost:8888"
        actual_baseUrl = toxiproxyapi.build_baseUrl(configuration)
        self.assertEqual(expected_baseUrl, actual_baseUrl)

    def test_build_proxy_baseUrl(self):
        configuration = {"toxiproxy_host": "localhost", "toxiproxy_port": "8888"}
        expected_baseUrl = "http://localhost:8888/proxies"
        actual_baseUrl = toxiproxyapi.build_proxies_baseUrl(configuration)
        self.assertEqual(expected_baseUrl, actual_baseUrl)
