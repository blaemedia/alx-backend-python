#!/usr/bin/env python3
"""
Test module for GithubOrgClient class
Contains unit tests for all methods of GithubOrgClient
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """Test that has_license returns the correct boolean value"""
        # Create a client instance (license_key doesn't matter for this test)
        client = GithubOrgClient("test-org")

        # Call the has_license method with the test parameters
        result = client.has_license(repo, license_key)

        # Assert the result matches the expected value
        self.assertEqual(result, expected_result)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient integration tests"""

    @classmethod
    def setUpClass(cls):
        """Set up class method to mock requests.get"""
        # Start a patcher for requests.get
        cls.get_patcher = patch('requests.get')

        # Start the mock
        cls.mock_get = cls.get_patcher.start()

        # Define side_effect function to return different payloads based on URL
        def side_effect(url):
            class MockResponse:
                @staticmethod
                def json():
                    if url.endswith('/orgs/test-org'):
                        return cls.org_payload
                    elif url.endswith('/repos'):
                        return cls.repos_payload
                    else:
                        return None

            return MockResponse()

        # Set the side_effect for the mock
        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class method to stop the patcher"""
        # Stop the patcher
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method in integration"""
        # Create client instance
        client = GithubOrgClient("test-org")

        # Call public_repos method
        result = client.public_repos()

        # Assert the result matches expected_repos
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method with license filter in integration"""
        # Create client instance
        client = GithubOrgClient("test-org")

        # Call public_repos method with license filter
        result = client.public_repos(license="apache-2.0")

        # Assert the result matches apache2_repos
        self.assertEqual(result, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
