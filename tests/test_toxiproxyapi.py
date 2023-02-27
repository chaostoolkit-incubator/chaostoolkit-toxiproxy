import unittest

import chaostoxi.toxiproxyapi as toxiproxyapi


class TestActionMethods(unittest.TestCase):
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

    def test_build_baseUrl_from_env(self):
        configuration = {"toxiproxy_url": "http://mydomain:8080/path-to-toxiproxy-api"}
        expected_baseUrl = "http://mydomain:8080/path-to-toxiproxy-api"
        actual_baseUrl = toxiproxyapi.build_baseUrl(configuration)
        self.assertEqual(expected_baseUrl, actual_baseUrl)
