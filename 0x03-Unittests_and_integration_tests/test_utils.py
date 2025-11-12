#!/usr/bin/env python3
"""Test module for utils"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json
from fixtures import TEST_PAYLOAD
from client import GithubOrgClient


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns expected result"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test KeyError is raised for invalid paths"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test class for get_json"""

    @parameterized.expand([
        ("http://example.com", TEST_PAYLOAD[0]),
        ("http://holberton.io", TEST_PAYLOAD[1]),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test get_json returns expected payload"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        with patch('requests.get', return_value=mock_response) as mock_get:
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @patch('client.get_json')
    def test_org(self, mock_get_json):
        """Test org property returns correct value"""
        test_payload = {"key": "val"}
        mock_get_json.return_value = test_payload
        client = GithubOrgClient("test_org")

        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/test_org")

        # Cached call
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
