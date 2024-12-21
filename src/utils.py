import os
import shutil
import logging
import subprocess

logger = logging.getLogger(__name__)

def exit(code: int = 0) -> None:
    os._exit(code)


def version() -> None:
    print("v1.0.0 - beta")

def yesno(prompt: str) -> bool:
    response = input(prompt).strip().lower()
    return response == "y"


def list(path: str) -> None:
    try:
        for item in os.listdir(path):
            print(item)
    except FileNotFoundError:
        logger.error(f"Directory '{path}' was not found.")
    except Exception as err:
        logger.error(err)
        exit(1)


def create_file(path: str) -> None:
    try:
        with open(path, 'w') as file:
            file.write("")
    except Exception as err:
        logger.error(f"creating file '{path}': {err}")
    except Exception as err:
        logger.error(err)
        exit(1)


def create_directory(path: str) -> None:
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as err:
        logger.error(f"Failed to create directory '{path}': {err}")
    except Exception as err:
        logger.error(err)
        exit(1)


def remove(path: str) -> None:
    if not yesno(f"Are you sure you want to remove '{path}'? [Y/n]: "):
        return

    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
    except FileNotFoundError:
        logger.error(f"Path '{path}' not found.")
    except OSError as err:
        logger.error(f"Failed to remove path '{path}': {err}")
    except Exception as err:
        logger.error(err)
        exit(1)


def create_symlink(target: str, destination: str) -> None:
    try:
        os.symlink(target, destination)
    except FileExistsError:
        logger.error(f"The symlink '{destination}' already exists.")
    except Exception as err:
        logger.error(f"Failed to create symlink: {err}")
    except Exception as err:
        logger.error(err)
        exit(1)


def clone(url: str, destination: str) -> None:
    try:
        os.makedirs(destination, exist_ok=True)
        subprocess.run(["git", "clone", url, destination], check=True)
    except subprocess.CalledProcessError:
        logger.error(f"Failed to clone repository from '{url}'.")
    except Exception as err:
        logger.error(f"Failed to clone '{url}' to '{destination}': {err}")
    except Exception as err:
        logger.error(err)
        exit(1)


def initialize_repository(path: str) -> None:
    try:
        subprocess.run(["git", "init", path], check=True)
    except Exception as err:
        logger.error(f"Failed to initialize repository {path}: {err}")
    except Exception as err:
        logger.error(err)
        exit(1)


def update_repository(repository: str) -> None:
    try:
        os.chdir(repository)
        subprocess.run(["git", "pull"], check=True)
    except Exception as err:
        logger.error(f"Failed to pull updates for '{repository}': {err}")
    except Exception as err:
        logger.error(err)
        exit(1)


def find_repositories(path: str, max_depth: int = 5) -> list:
    if max_depth <= 0:
        return []

    if os.path.isdir(os.path.join(path, ".git")):
        return [path]

    repositories = []
    exceptions = [".git", "node_modules"]

    for dir in os.listdir(path):
        full_path = os.path.join(path, dir)
        if os.path.isdir(full_path) and dir not in exceptions:
            repositories.extend(find_repositories(full_path, max_depth - 1))
        
    return repositories


def is_valid_repo_name(repository: str) -> bool:
    invalid_characters = re.compile(r"[^a-zA-Z0-9_-]")
    return not bool(invalid_characters.search(repository.strip()))
