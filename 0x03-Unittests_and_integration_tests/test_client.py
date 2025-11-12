#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        expected_result = {"login": org_name}
        mock_get_json.return_value = expected_result

        client = GithubOrgClient(org_name)

        # Call the org method
        result = client.org()

        self.assertEqual(result, expected_result)

        # Assert get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        # Optional: call again to check memoization
        result2 = client.org()
        self.assertEqual(result2, expected_result)
        mock_get_json.assert_called_once()  # should still be called once due to memoization

if __name__ == "__main__":
    unittest.main()