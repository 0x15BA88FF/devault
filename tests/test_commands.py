"""Test Cases for commands script"""

# type: ignore # pylint: disable=import-error

import commands

def test_http_uri():
    """Test Regex URL Parsing"""

    url = "https://github.com/0x15BA88FF/devault.git"
    provider, directory, repository = commands.parse_url(url)

    assert (provider, directory, repository) == ("github.com", "0x15ba88ff", "devault")
