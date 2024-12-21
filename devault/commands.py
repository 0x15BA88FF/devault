"""
This script defines all relivant commands and functions the tool directly runs.
"""

# pylint: disable=import-error

import os
import re
import sys
import logging
from typing import List, Tuple

import utils

logger = logging.getLogger(__name__)
DEVDIR = os.getenv("DEVDIR") or os.path.expanduser("~/Dev")

def parse_url(url: str) -> Tuple[str]:
    """split url into sections"""

    url_patterns = [
        r'^https?://(?P<provider>[^/]+)(?:/(?P<directory>.*?))?/(?P<repository>[^/]+)\.git$',
        r'^git@(ssh\.)?(?P<provider>[^:]+)(?::(?P<directory>.*?))?/(?P<repository>[^/]+)\.git$',
    ]

    for pattern in url_patterns:
        match = re.search(pattern, url)
        if match:
            provider = match.group("provider")
            directory = match.group("directory") or ""
            repository = match.group("repository")

            print(provider.lower(), directory.lower(), repository.lower())
            return provider.lower(), directory.lower(), repository.lower()

    logger.error("Invalid URL '%s' could not be parsed", url)
    sys.exit(1)


def init() -> None:
    """Initialize the DEVDIR"""

    utils.create_directory(DEVDIR)
    logger.info("%s has been initialized.", DEVDIR)


def list_items(*paths: str) -> None:
    """Handle listing entities within the DEVDIR"""

    for path in paths:
        full_path = os.path.realpath(os.path.join(DEVDIR, path))
        if not full_path.startswith(DEVDIR):
            logger.warning("The path '%s' is outside the dev sandbox.", full_path)
            continue
        utils.list_items(full_path)


def remove(*paths: str) -> None:
    """Handle removing entities inside the DEVDIR"""

    for path in paths:
        full_path = os.path.realpath(os.path.join(DEVDIR, path))
        if not full_path.startswith(DEVDIR):
            logger.warning("The path '%s' is outside the dev sandbox.", full_path)
            continue
        utils.remove(full_path)


def find(*queries: str) -> None:
    """Handle finding repositories in the DEVDIR"""

    try:
        regex = re.compile("|".join(queries))
        repositories = utils.find_repositories(DEVDIR)
        matching_repositories = [repo for repo in repositories if regex.search(repo)]
        for repo in matching_repositories:
            print(repo)
    except re.error as err:
        logger.error("Invalid search expression %s", err)
        sys.exit(1)


def clone(url: str, collections: List[str]) -> None:
    """Handle cloning remote repositories"""

    provider, directory, repository = parse_url(url)
    destination = os.path.join(DEVDIR, "hosts", provider, directory, repository)
    utils.clone(url, destination)

    for collection in collections:
        collection_path = os.path.join(DEVDIR, collection)
        utils.create_directory(collection_path)
        utils.create_symlink(destination, os.path.join(collection_path, repository))


def update(*paths: str) -> None:
    """Handle pulling remote changes from upstream repositories"""

    # [TODO] feature: update repos by group / user / provider using /*
    if "*" in paths:
        paths = [""]

    for path in paths:
        full_path = os.path.join(DEVDIR, path)
        for repo in utils.find_repositories(full_path):
            utils.update_repository(repo)


def group(*args: str) -> None:
    """Handle linking repositories into collections"""

    if len(args) < 2:
        logger.error("At least two arguments are required.")
        sys.exit(1)

    collection_path = os.path.join(DEVDIR, args[-1])
    utils.create_directory(collection_path)

    for repository in args[:-1]:
        repository_name = os.path.basename(repository.rstrip("/"))
        utils.create_symlink(repository, os.path.join(collection_path, repository_name))


def mkrepo() -> None:
    """Handle creating new local repositories"""

    # [TODO] preview
    # [TODO] feature: using repositories as templates
    name = input("Repositories name: ").split()
    repository_path = os.path.join(DEVDIR, "hosts", "local", name)

    if not utils.is_valid_repo_name(name):
        logger.error("%s is an invalid repository name.", name)
        sys.exit(1)
    if os.path.isdir(repository_path):
        if not utils.yesno(f"do you want to overwrite {repository_path}? [Y/n]: "):
            sys.exit(1)

    starters = input("Starter content (README.md): ").split() or ["README.md"]
    starter_paths = [os.path.join(repository_path, starter) for starter in starters]

    collections = input("Add to collection(s): ").split() or []

    utils.create_directory(repository_path)
    utils.initialize_repository(repository_path)

    if collections:
        group(repository_path, *collections)

    for starter_path in starter_paths:
        starter_abs_path = os.path.realpath(starter_path)
        if not starter_abs_path.startswith(repository_path):
            logger.warning("Starter item %s is outside the repository path.", starter_path)
            continue

        if starter_path.endswith("/"):
            utils.create_directory(starter_path)
        else:
            utils.create_directory(os.path.dirname(starter_path))
            utils.create_file(starter_path)
