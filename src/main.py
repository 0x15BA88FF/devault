import os
import re
import utils
import argparse


COMMAND_NAME = "dev"
DEVAULT_DIR = os.getenv("DEVAULT_DIR") or os.path.expanduser("~/Dev")


def parse_uri(uri: str):
    URL_PATTERNS = [
        r'^https?://(?P<provider>[^/]+)(?:/(?P<directory>.*?))?/(?P<repository>[^/]+)\.git$',
        r'^git@(ssh\.)?(?P<provider>[^:]+)(?::(?P<directory>.*?))?/(?P<repository>[^/]+)\.git$',
    ]

    for pattern in URL_PATTERNS:
        match = re.search(pattern, uri)
        if match:
            provider = match.group("provider")
            directory = match.group("directory") or ""
            repository = match.group("repository")

            return provider, directory, repository

    raise ValueError("Invalid URL.")


def init() -> None:
    utils.mkdir([DEVAULT_DIR])
    print(f"{ DEVAULT_DIR } has been initialized.")


def ls(*paths: str) -> None:
    if len(paths) < 1: paths = [""]
    arguments = [f"{ DEVAULT_DIR }/{ path }" for path in paths]
    utils.ls(arguments)


def rm(*paths: str) -> None:
    arguments = [f"{ DEVAULT_DIR }/{ path }" for path in paths]
    utils.rm(arguments)


def find(query: str) -> None:
    regex = re.compile(query)
    [
        print(repository) for repository in utils.get_repos(DEVAULT_DIR)
        if regex.search(repository)
    ]


def clone(*args: str) -> None:
    uri = args[0]
    collections = args[1:] if len(args) > 1 else []
    collections = [f"{ DEVAULT_DIR }/{ collection }" for collection in collections ]

    provider, directory, repository = parse_uri(uri)
    destination = f"{ DEVAULT_DIR }/clones/{ provider }/{ directory }/{ repository }/"
    utils.clone(uri, destination)

    for collection in collections:
        utils.mkdir([collection])
        utils.ln(destination, f"{ collection }/{ repository }")


def update(*repositories: str) -> None:
    if "." in repositories: repositories = [""]
    repositories = [f"{ DEVAULT_DIR }/clones/{ repository }" for repository in repositories]

    for repository in repositories:
        [utils.update(repository) for repository in utils.get_repos(repository)]


def group(*args: str) -> None:
    if len(args) < 2: utils.exit(1, print("At least two arguments required for grouping."))
    repositories = args[:-1]
    collection = args[-1]

    for repository in repositories:
        utils.ln(repository, collection)


def mkrepo() -> None:
    name = input("Repositories Name: ") or utils.exit(1, print("Repository name required."))
    directory = input("Repositories directory: ")
    starters = input("Starter content (README.md): ") or "README.md"
    collections = input("Add to collection(s): ")

    repository = f"{ DEVAULT_DIR }/clones/local/{ directory }/{ name }"
    starters = [ f"{ repository }/{ item }" for item in starters.split(" ") ]

    utils.mkdir([repository])
    utils.git_init(repository)
    [ group(repository, collection) for collection in collections ]

    for item in starters:
        if item[-1] == "/":
            utils.mkdir([item])
        else:
            utils.mkdir(["/".join(item.split("/")[:-1])])
            utils.touch([item])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A minimal tool to manage your repositories",
        epilog="Examples:"
               f"\n\t{ COMMAND_NAME } init                       # initialize a vault"
               f"\n\t{ COMMAND_NAME } clone <repo-url>           # Clone a repository",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("command",
        choices=["help", "version", "init", "ls", "rm", "find", "clone", "update", "group", "mkrepo"],
        help=(
            "\nhelp                 show list of command-line options"
            "\nversion              show the current version"
            "\ninit                 initialize a dev vault"
            "\nls                   list entities in a vault"
            "\nrm                   remove entitie"
            "\nfind                 find a repository (supports regex)"
            "\nclone                clone a repository to a vault"
            "\nupdate               pull latest changes from upstream"
            "\ngroup                group repositories into collections"
            "\nmkrepo               Create and initialize a local git repository"
        )
    )

    parser.add_argument("arg", nargs="*", help="Argument for the command.")

    args = parser.parse_args()
    command = args.command
    arguments = args.arg

    if   command == "version":                   utils.version()
    elif command == "init":                      init()
    elif command == "ls":                        ls(*arguments)
    elif command == "rm" and arguments:          rm(*arguments)
    elif command == "find" and arguments:        find(arguments[0])
    elif command == "clone" and arguments:       clone(*arguments)
    elif command == "update" and arguments:      update(*arguments)
    elif command == "group" and arguments:       group(*arguments)
    elif command == "mkrepo":                    mkrepo()
    else:                                        parser.print_help()
