import os
import re
import argparse
import subprocess

COMMAND_NAME = "dv"
DEVAULT_DIR = os.getenv("DEVAULT_DIR") or os.path.expanduser("~/DEVAULT")


def print_version() -> None:
    print("v0.0.0")


def parse_repo_url(url: str):
    URL_PATTERNS = [
        r"https?://(?P<provider>[^/]+)/(?P<username>[^/]+)/(?P<repository>[^/]+)(?:\.git)?",
        r"git@(?P<provider>[^:]+):(?P<username>[^/]+)/(?P<repository>[^/]+)(?:\.git)?"
    ]

    for pattern in URL_PATTERNS:
        match = re.search(pattern, url)
        if match:
            provider = match.group("provider")
            repository = match.group("repository")
            username = match.group("username") or provider.split(".")[-2]

            return provider, username, repository

    raise ValueError("Invalid URL.")


def clone_repo(url: str) -> None:
    provider, username, repository = parse_repo_url(url)
    destination = f"{ DEVAULT_DIR }/{ provider }/{ username }/{ repository }"

    os.makedirs(destination, exist_ok=True)
    subprocess.run([ "git", "clone", url, destination ], check=True)


def list_entities(entity: str) -> None:
    path = os.path.join(DEVAULT_DIR, entity or "")
    if not os.path.exists(path): raise ValueError("Invalid path.")
    if "cmd.exe" in os.getenv("COMSPEC", ""):
        return print(subprocess.run(["cmd", "/c", "dir", path], capture_output=True, text=True).stdout)

    return print(subprocess.run(["ls", "-la", path], capture_output=True, text=True).stdout)


def list_tree() -> None:
    if not os.path.exists(DEVAULT_DIR): return
    if "cmd.exe" in os.getenv("COMSPEC", ""):
        return print(subprocess.run(['cmd', '/c', f'tree /F /A /N /L 3 {DEVAULT_DIR}'], capture_output=True, text=True).stdout)

    return print(subprocess.run(['tree', '-L', '3', DEVAULT_DIR], capture_output=True, text=True).stdout)


def remove_entity(entity: str) -> None:
    path = os.path.join(DEVAULT_DIR, entity or "")
    if not os.path.exists(path): raise ValueError("Invalid path.")

    answer = input(f"Are you sure you want to remove '{ entity }' (Y/n) ")
    if answer not in ["Y", "y"]: return

    if "cmd.exe" in os.getenv("COMSPEC", ""):
        return print(subprocess.run(['cmd', '/c', f'rmdir /s /q {path}'], capture_output=True, text=True).stdout)

    return print(subprocess.run(['rm', '-rf', path], capture_output=True, text=True).stdout)


def make_repo() -> None:
    provider = input(f"Enter a provider e.g. (github.com): ")
    if not provider: return print(f"Invalid provider { provider }")
    username = input(f"Enter your username: ")
    if not username: return print(f"Invalid username { username }")
    repository = input(f"Enter a repository name: ")
    if not repository: return print(f"Invalid username { repository }")

    path = os.path.join(DEVAULT_DIR, provider, username, repository)

    os.makedirs(path, exist_ok=True)
    print(subprocess.run([ "git", "init", path ], check=True).stdout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A minimal tool to manage your repositories and git clones.",
        epilog="Examples:"
               f"\n\t{ COMMAND_NAME } clone <repo-url>           # Clone a repository"
               f"\n\t{ COMMAND_NAME } ls github.com              # List entities in /github.com"
               f"\n\t{ COMMAND_NAME } tree                       # Tree list entities",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "command",
        choices=["version", "clone", "ls", "tree", "mkrepo", "rm", "open"],
        help=(
            "version              : Print the current version"
            "\nclone <repo-url>     : Clone a repository into your DEVault"
            "\nls [entity]          : List entities in your DEVault"
            "\ntree                 : Display a tree view of entities"
            "\nmkrepo <repo-name>   : Create a new repository"
            "\nrm <entity>          : Remove an entity from your DEVault"
            "\nopen <entity>        : Open an entity in the default editor"
        )
    )

    parser.add_argument("arg", nargs="?", help="Argument for the command, e.g. [<repo-url>, <entity>].")

    args = parser.parse_args()
    command = args.command
    arg = args.arg

    if   command == "version":                     print_version()
    elif command == "clone" and arg:               clone_repo(arg)
    elif command in ["ls", "list", "dir"]:         list_entities(arg)
    elif command == "tree":                        list_tree()
    elif command == "mkrepo":                      make_repo()
    elif command in ["remove", "rm"] and arg:      remove_entity(arg)
    else:                                          parser.print_help()
