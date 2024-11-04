import os
import shutil
import subprocess
from typing import Optional, Callable

def exit(code: int = 0, callback: Optional[Callable[[], None]] = None) -> None:
    if callback:
        callback()
    os._exit(code)


def version() -> None:
    print("v0.0.1")


def ls(paths: list) -> None:
    for path in paths:
        for item in os.listdir(path):
            print(item)


def touch(paths: list) -> None:
    for path in paths:
        with open(path, 'w') as file:
            file.write("")


def mkdir(paths: list) -> None:
    for path in paths:
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as err:
            raise OSError(f"Failed to create directory { path }.")


def rm(paths: list) -> None:
    for path in paths:
        response = input(f"Are you sure you want to remove '{ path }'? [Y/n]: ")
        if response not in ["Y", "y"]:
            return None

        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except FileNotFoundError:
            print(f"Path '{ path }' not found.")
        except OSError as err:
            print(f"Error removing path '{ path }': { err }")


def ln(target: str, destination: str) -> None:
    try:
        os.symlink(target, destination)
    except FileExistsError:
        print(f"Error: The symlink '{ destination }' already exists.")
    except Exception as err:
        print(f"Error creating symlink: { err }")


def clone(uri: str, destination: str) -> None:
    try:
        os.makedirs(destination, exist_ok=True)
        subprocess.run([ "git", "clone", uri, destination ], check=True)
    except Exception as err:
        print(f"Failed to clone '{ uri }' to { destination }: { err }")


def git_init(path: str) -> None:
    try:
        os.chdir(path)
        subprocess.run([ "git", "init" ], check=True)
    except Exception as err:
        print(f"Failed to initialize repository { path }: { err }")


def update(repository: str) -> None:
    try:
        os.chdir(repository)
        subprocess.run([ "git", "pull" ], check=True)
    except Exception as err:
        print(f"Failed to pull '{ repository }': { err }")


def get_repos(path: str) -> list[str, ...]:
    if os.path.isdir(os.path.join(path, ".git")):
        return [path]

    repos = []
    exceptions = [".git", "node_modules"]
    [
        repos.extend(get_repos(os.path.join(path, dir))) for dir in os.listdir(path)
        if os.path.isdir(os.path.join(path, dir)) and dir not in exceptions
    ]
        
    return repos
