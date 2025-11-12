
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")  # Mock get_json so it does not make HTTP calls
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""

        # Setup the mock to return a specific dictionary
        expected_result = {"login": org_name}
        mock_get_json.return_value = expected_result

        # Instantiate the client with the org_name
        client = GithubOrgClient(org_name)

        # Call the org method
        result = client.org()

        # Assert that the result is what we mocked
        self.assertEqual(result, expected_result)

        # Assert get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    if __name__ == "__main__":
