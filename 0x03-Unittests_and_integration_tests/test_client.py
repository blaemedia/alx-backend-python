#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
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

        # Test memoization - call again
        result2 = client.org()
        self.assertEqual(result2, expected_result)
        mock_get_json.assert_called_once()  # should still be called once due to memoization

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct value based on mocked org payload"""
        # Test payload with repos_url
        test_payload = {
            "repos_url": "https://api.github.com/orgs/test-org/repos",
            "login": "test-org",
            "id": 123456
        }
        
        # Use patch as a context manager to mock the org property
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            # Set the return value of the mocked property
            mock_org.return_value = test_payload
            
            # Create client instance
            client = GithubOrgClient("test-org")
            
            # Call the _public_repos_url property
            result = client._public_repos_url
            
            # Assert the result is the expected repos_url from the payload
            self.assertEqual(result, test_payload["repos_url"])
            
            # Verify the org property was accessed
            mock_org.assert_called_once()


if __name__ == "__main__":
    unittest.main()