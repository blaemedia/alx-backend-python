#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import get_json
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

    def test_get_json_example_com(self):
        """Test get_json with http://example.com"""
        test_url = "http://example.com"
        test_payload = {"payload": True}
        
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        
        with patch('requests.get', return_value=mock_response) as mock_get:
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)

    def test_get_json_holberton_io(self):
        """Test get_json with http://holberton.io"""
        test_url = "http://holberton.io"
        test_payload = {"payload": False}
        
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        
        with patch('requests.get', return_value=mock_response) as mock_get:
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)
            
if __name__ == '__main__':
    unittest.main()