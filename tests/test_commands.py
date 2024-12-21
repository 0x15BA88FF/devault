"""Test Cases for commands script"""

# type: ignore # pylint: disable=import-error

import json
import commands

class TestUrlParser:
    """Test Regex URL Parsing"""

    def test_http(self):
        """Test http / https parsing"""

        test_data_file = "./tests/test_files/test_http_urls.json"

        with open(test_data_file, 'r', encoding="UTF-8") as file:
            json_data = json.load(file)

            for case in json_data:
                provider, directory, repository = commands.parse_url(case["url"])

                assert provider == case["provider"]
                assert directory == case["directory"]
                assert repository == case["repository"]

    def test_ssh(self):
        """Test ssh parsing"""

        test_data_file = "./tests/test_files/test_ssh_urls.json"

        with open(test_data_file, 'r', encoding="UTF-8") as file:
            json_data = json.load(file)

            for case in json_data:
                provider, directory, repository = commands.parse_url(case["url"])

                assert provider == case["provider"]
                assert directory == case["directory"]
                assert repository == case["repository"]
