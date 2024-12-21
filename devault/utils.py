"""
This script defines all utility / helper functions that handle micro funtionality.
"""

# pylint: disable=broad-exception-caught

import os
import re
import sys
import shutil
import logging
import subprocess

logger = logging.getLogger(__name__)

def version() -> None:
    """Output version"""

    print("v1.2.2 - beta")


def yesno(prompt: str) -> bool:
    """Return true / false response from frompt"""

    response = input(prompt).strip().lower()
    return response == "y"


def list_items(path: str) -> None:
    """Output items in a path"""

    try:
        for item in os.listdir(path):
            print(item)
    except FileNotFoundError:
        logger.error("Directory %s was not found.", path)
        sys.exit(1)
    except Exception as err:
        logger.error("Failed to list items in '%s': %s", path, err)
        sys.exit(1)


def create_file(path: str) -> None:
    """Create an empty file"""

    try:
        with open(path, 'w', encoding="UTF-8") as file:
            file.write("")
    except Exception as err:
        logger.error("creating file '%s': %s", path, err)
        sys.exit(1)


def create_directory(path: str) -> None:
    """Create a directory"""

    try:
        os.makedirs(path, exist_ok=True)
    except Exception as err:
        logger.error("Failed to create directory '%s': %s", path, err)
        sys.exit(1)


def remove(path: str) -> None:
    """Remove a directory or file"""

    if not yesno(f"Are you sure you want to remove '{path}'? [Y/n]: "):
        return

    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
    except FileNotFoundError:
        logger.error("Path '%s' not found.", path)
        sys.exit(1)
    except Exception as err:
        logger.error("Failed to remove path '%s': %s", path, err)
        sys.exit(1)


def create_symlink(target: str, destination: str) -> None:
    """Create symlink to a directory or file"""

    try:
        os.symlink(target, destination)
    except FileExistsError:
        logger.info("The symlink '%s' already exists.", destination)
        sys.exit(1)
    except Exception as err:
        logger.error("Failed to create symlink '%s' to '%s': %s", target, destination, err)
        sys.exit(1)


def clone(url: str, destination: str) -> None:
    """Clone a repository with git"""

    try:
        os.makedirs(destination, exist_ok=True)
        subprocess.run(["git", "clone", url, destination], check=True)
    except Exception as err:
        logger.error("Failed to clone '%s' to '%s': %s", url, destination, err)
        sys.exit(1)


def initialize_repository(path: str) -> None:
    """Initialize an empty repository"""

    try:
        subprocess.run(["git", "init", path], check=True)
    except Exception as err:
        logger.error("Failed to initialize repository %s: %s", path, err)
        sys.exit(1)


def update_repository(repository: str) -> None:
    """Pull remote changes"""

    try:
        os.chdir(repository)
        subprocess.run(["git", "pull"], check=True)
    except Exception as err:
        logger.error("Failed to pull updates for '%s': %s", repository, err)
        sys.exit(1)


def find_repositories(path: str, max_depth: int = 5) -> list:
    """Find all git repositories in path"""

    if max_depth <= 0:
        return []

    if os.path.isdir(os.path.join(path, ".git")):
        return [path]

    repositories = []
    exceptions = {".git", "node_modules"}

    for directory in os.listdir(path):
        full_path = os.path.join(path, directory)
        if os.path.isdir(full_path) and directory not in exceptions:
            repositories.extend(find_repositories(full_path, max_depth - 1))

    return repositories


def is_valid_repo_name(repository: str) -> bool:
    """Validate repository name"""

    invalid_characters = re.compile(r"[^a-zA-Z0-9_-]")
    return not bool(invalid_characters.search(repository.strip()))
