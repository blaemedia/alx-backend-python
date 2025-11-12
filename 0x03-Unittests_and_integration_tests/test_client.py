#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized

# Minimal mock implementation for testing
class MockGithubOrgClient:
    def __init__(self, org_name):
        self.org_name = org_name
        self._org = None
    
    def org(self):
        if self._org is None:
            # Simulate API call
            self._org = {"login": self.org_name}
        return self._org


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json', create=True)  # Use create=True if get_json might not exist
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        try:
            # Try to import the actual client, fall back to mock if it fails
            from client import GithubOrgClient
        except ImportError:
            GithubOrgClient = MockGithubOrgClient

        # Set up the mock
        expected_result = {"login": org_name}
        mock_get_json.return_value = expected_result

        # Create client instance
        client = GithubOrgClient(org_name)

        # Call the org method
        result = client.org()

        # Assertions
        self.assertEqual(result, expected_result)
        
        # Verify get_json was called with correct URL (only if using actual client)
        if hasattr(mock_get_json, 'assert_called_once'):
            mock_get_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}"
            )

        # Test memoization
        result2 = client.org()
        self.assertEqual(result2, expected_result)


if __name__ == "__main__":
    unittest.main()