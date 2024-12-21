import os
import re
import utils
import logging

logger = logging.getLogger(__name__)
DEVDIR = os.getenv("DEVDIR") or os.path.expanduser("~/Dev")

def parse_url(url: str):
    URL_PATTERNS = [
        r'^https?://(?P<provider>[^/]+)(?:/(?P<directory>.*?))?/(?P<repository>[^/]+)\.git$',
        r'^git@(ssh\.)?(?P<provider>[^:]+)(?::(?P<directory>.*?))?/(?P<repository>[^/]+)\.git$',
    ]

    for pattern in URL_PATTERNS:
        match = re.search(pattern, url)
        if match:
            provider = match.group("provider").lower()
            directory = match.group("directory").lower() or ""
            repository = match.group("repository").lower()

            return provider, directory, repository

    logger.error(f"Invalid URL '{url}' could not be parsed")
    utils.exit(1)


def init() -> None:
    utils.create_directory(DEVDIR)
    logger.info(f"{DEVDIR} has been initialized.")


def list(*paths: str) -> None:
    for path in paths:
        full_path = os.path.join(DEVDIR, path)
        if not full_path.startswith(DEVDIR):
            logger.warning(f"The path '{full_path}' is outside the dev sandbox.")
            continue
        utils.list(os.path.join(full_path))


def remove(*paths: str) -> None:
    for path in paths:
        full_path = os.path.join(DEVDIR, path)
        if not full_path.startswith(DEVDIR):
            logger.warning(f"The path '{full_path}' is outside the dev sandbox.")
            continue
        utils.remove(os.path.join(full_path))


def find(*queries: str) -> None:
    try:
        regex = re.compile("|".join(queries))
        repositories = utils.find_repositories(DEVDIR)
        matching_repositories = [repo for repo in repositories if regex.search(repo)]
        for repo in matching_repositories:
            print(repo)
    except re.error as err:
        logger.error(f"Invalid search expression {err}")
        return


def clone(url: str, collections: [str, ...]) -> None:
    provider, directory, repository = parse_url(url)
    destination = os.path.join(DEVDIR, "hosts", provider, directory, repository)
    utils.clone(url, destination)

    for collection in collections:
        collection_path = os.path.join(DEVDIR, collection)
        utils.create_directory(collection_path)
        utils.create_symlink(destination, os.path.join(DEVDIR, collection, repository))


def update(*paths: str) -> None:
    # [TODO] feature: update repos by group / user / provider using /*
    if "*" in paths:
        paths = [""]

    for path in paths:
        path = os.path.join(DEVDIR, path)
        for repo in utils.find_repositories(path):
            utils.update_repository(repo)


def group(*args: str) -> None:
    if len(args) < 2:
        logger.error("At least two arguments are required.")
        utils.exit(1)

    collection_path = os.path.join(DEVDIR, args[-1])
    utils.create_directory(collection_path)

    for repository in args[:-1]:
        repository_name = os.path.basename(repository.rstrip("/"))
        utils.create_symlink(repository, os.path.join(collection_path, repository_name))


def mkrepo() -> None:
    # [TODO] preview
    # [TODO] feature: using repositories as templates
    name = input("Repositories name: ").split()
    repository_path = os.path.join(DEVDIR, "hosts", "local", name)

    if not utils.is_valid_repo_name(name):
        logger.error(f"{name} is an invalid repository name.")
        utils.exit(1)
    if os.path.isdir(repository_path):
        if not utils.yesno(f"{repository_path} already exists, do you want to overwrite it? [Y/n]: "):
            utils.exit(1)

    starters = input("Starter content (README.md): ").split() or ["README.md"]
    starter_paths = [os.path.join(repository_path, starter) for starter in starters]

    collections = input("Add to collection(s): ").split() or []

    utils.create_directory(repository)
    utils.initialize_repository(repository)

    if collections:
        group(repository, *collections)

    for starter_path in starter_paths:
        starter_abs_path = os.path.realpath(starter_path)
        if not starter_abs_path.startswith(repository_path):
            logger.warning(f"Starter item {starter} is outside the repository path.")
            continue

        if starter.endswith("/"):
            utils.create_directory(starter)
        else:
            utils.create_directory(os.path.dirname(starter))
            utils.create_file(starter)
