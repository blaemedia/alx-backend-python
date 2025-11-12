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
        # should still be called once due to memoization
        mock_get_json.assert_called_once()

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct value"""
        # Test payload with repos_url
        test_payload = {
            "repos_url": "https://api.github.com/orgs/test-org/repos",
            "login": "test-org",
            "id": 123456
        }

        # Use patch as a context manager to mock the org property
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            # Set the return value of the mocked property
            mock_org.return_value = test_payload

            # Create client instance
            client = GithubOrgClient("test-org")

            # Call the _public_repos_url property
            result = client._public_repos_url

            # Assert the result is the expected repos_url from payload
            self.assertEqual(result, test_payload["repos_url"])

            # Verify the org property was accessed
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the correct list of repositories"""
        # Mock payload for get_json (list of repos)
        mock_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]

        # Mock the _public_repos_url property value
        mock_repos_url = "https://api.github.com/orgs/test-org/repos"

        # Set up the mock for get_json
        mock_get_json.return_value = mock_repos_payload

        # Create client instance
        client = GithubOrgClient("test-org")

        # Use patch as context manager to mock _public_repos_url
        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value=mock_repos_url
        ) as mock_public_repos_url:

            # Call the public_repos method
            result = client.public_repos()

            # Expected result: list of repository names
            expected_repos = ["repo1", "repo2", "repo3"]

            # Assert the list of repos is what we expect
            self.assertEqual(result, expected_repos)

            # Verify that _public_repos_url was called once
            mock_public_repos_url.assert_called_once()

            # Verify that get_json was called once with correct URL
            mock_get_json.assert_called_once_with(mock_repos_url)

if __name__ == "__main__":
    unittest.main()