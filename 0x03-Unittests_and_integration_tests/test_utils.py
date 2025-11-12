#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import get_json
from fixture import TEST_PAYLOAD 
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns the expected result"""
        self.assertEqual(access_nested_map(nested_map, path), expected)



#!/usr/bin/env python3
"""Test module for utils"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns the expected result"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError for invalid paths"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{path[-1]}'")

class TestGetJson(unittest.TestCase):
    """Test class for get_json function"""

    def test_get_json(self):
        """Test get_json returns the expected result without making actual HTTP calls"""
        # Use the payloads from your fixture.py file
        test_cases = [
            ("http://example.com", TEST_PAYLOAD[0]),
            ("http://holberton.io", TEST_PAYLOAD[1]),
        ]
        
        for test_url, test_payload in test_cases:
            with self.subTest(test_url=test_url):
                mock_response = Mock()
                mock_response.json.return_value = test_payload
                
                with patch('requests.get', return_value=mock_response) as mock_get:
                    result = get_json(test_url)
                    mock_get.assert_called_once_with(test_url)
                    self.assertEqual(result, test_payload)



if __name__ == '__main__':
    unittest.main()