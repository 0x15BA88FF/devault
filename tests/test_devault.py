from devault import parse_uri

def test_http_uri():
    uri = "https://github.com/0x15BA88FF/devault.git"
    provider, directory, repository = parse_uri(uri)

    assert (provider, directory, repository) == ("github.com", "0x15ba88ff", "devault")
