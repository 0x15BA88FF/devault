import os
import re
import utils

DEVDIR = os.getenv("DEVDIR") or os.path.expanduser("~/Dev")

def parse_uri(uri: str):
    URL_PATTERNS = [
        r'^https?://(?P<provider>[^/]+)(?:/(?P<directory>.*?))?/(?P<repository>[^/]+)\.git$',
        r'^git@(ssh\.)?(?P<provider>[^:]+)(?::(?P<directory>.*?))?/(?P<repository>[^/]+)\.git$',
    ]

    for pattern in URL_PATTERNS:
        match = re.search(pattern, uri)
        if match:
            provider = match.group("provider").lower()
            directory = match.group("directory").lower() or ""
            repository = match.group("repository").lower()

            return provider, directory, repository

    raise ValueError("Invalid URL.")


def init() -> None:
    utils.mkdir(DEVDIR)
    print(f"{ DEVDIR } has been initialized.")


def ls(*paths: str) -> None:
    if len(paths) < 1: paths = [""]
    [ utils.ls(f"{ DEVDIR }/{ path }") for path in paths ]


def rm(*paths: str) -> None:
    arguments = [f"{ DEVDIR }/{ path }" for path in paths]
    utils.rm(arguments)


def find(query: str) -> None:
    regex = re.compile(query)
    [
        print(repository) for repository in utils.get_repos(DEVDIR)
        if regex.search(repository)
    ]


def clone(*args: str) -> None:
    uri = args[0]
    collections = args[1:] if len(args) > 1 else []
    collections = [f"{ DEVDIR }/{ collection }" for collection in collections ]

    provider, directory, repository = parse_uri(uri)
    destination = f"{ DEVDIR }/hosts/{ provider }/{ directory }/{ repository }/"
    utils.clone(uri, destination)

    for collection in collections:
        utils.mkdir(collection)
        utils.ln(destination, f"{ collection }/{ repository }")


def update(*repositories: str) -> None:
    if "." in repositories: repositories = [""]
    repositories = [f"{ DEVDIR }/hosts/{ repository }" for repository in repositories]

    for repository in repositories:
        [utils.update(repository) for repository in utils.get_repos(repository)]


def group(*args: str) -> None:
    if len(args) < 2: utils.exit(1, print("At least two arguments required."))
    collection = f"{ DEVDIR }/{ args[-1] }"
    utils.mkdir(collection)
    for repository in args[:-1]:
        repository_name = repository.strip("/").split("/")[-1]
        utils.ln(repository, f"{ collection }/{ repository_name }")


def mkrepo() -> None:
    name = input("Repositories Name: ") or utils.exit(1, print("Repository name required."))
    starters = input("Starter content (README.md): ") or "README.md"
    collections = input("Add to collection(s): ")

    repository = f"{ DEVDIR }/hosts/local/{ name }"
    starters = [ f"{ repository }/{ item }" for item in starters.split(" ") ]

    utils.mkdir(repository)
    utils.git_init(repository)
    if collections: group(repository, *collections.split(" "))

    for item in starters:
        item = os.path.realpath(item)

        if len(repository) > len(item) or repository == item[0:len(repository) - 1]:
            print(f"Starter item { item } is located outside the repository")
            continue

        if item[-1] == "/":
            utils.mkdir(item)
        else:
            utils.mkdir("/".join(item.split("/")[:-1]))
            utils.touch([item])
