#!/usr/bin/env python3
"""Test module for utils"""

import unittest
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json
from fixtures import TEST_PAYLOAD


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map function"""

    def test_access_nested_map(self):
        """Test access_nested_map returns the expected result"""
        test_cases = [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
        
        for nested_map, path, expected in test_cases:
            with self.subTest(nested_map=nested_map, path=path):
                self.assertEqual(access_nested_map(nested_map, path), expected)

    def test_access_nested_map_exception(self):
        """Test access_nested_map raises KeyError for invalid paths"""
        test_cases = [
            ({}, ("a",)),
            ({"a": 1}, ("a", "b")),
        ]
        
        for nested_map, path in test_cases:
            with self.subTest(nested_map=nested_map, path=path):
                with self.assertRaises(KeyError):
                    access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test class for get_json function"""

    def test_get_json(self):
        """Test get_json returns the expected result without making actual HTTP calls"""
        test_cases = [
            ("http://example.com", TEST_PAYLOAD[0]),
            ("http://holberton.io", TEST_PAYLOAD[1]),
        ]
        
        for test_url, test_payload in test_cases:
            with self.subTest(test_url=test_url):
                mock_response = Mock()
                mock_response.json.return_value = test_payload
                
                # Use this exact patch target - it should work
                with patch('requests.get', return_value=mock_response) as mock_get:
                    result = get_json(test_url)
                    mock_get.assert_called_once_with(test_url)
                    self.assertEqual(result, test_payload)


if __name__ == '__main__':
    unittest.main()