import utils
import logging
import devault
import argparse

COMMAND_NAME = "dev"
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(
        format='[{levelname}]: {message}',
        style='{',
        level=logging.INFO
    )

    parser = argparse.ArgumentParser(
        prog="devault",
        description="A minimal tool to manage your repositories",
        epilog=f"Run '{COMMAND_NAME} <command> --help' for more information about a command."
    )

    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="Show the current version"
    )

    parser.add_argument(
        "-V",
        type=int,
        default=0,
        choices=[0, 1, 2, 3],
        help="increase output verbosity"
    )

    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Initialize a dev vault")
    init_parser.set_defaults(func=lambda args: devault.init())

    ls_parser = subparsers.add_parser("ls", help="List entities in a vault")
    ls_parser.add_argument("paths", nargs="*", help="Paths to list")
    ls_parser.set_defaults(func=lambda args: devault.list(*args.paths or [""]))

    rm_parser = subparsers.add_parser("rm", help="Remove entity(ies) from dev vault")
    rm_parser.add_argument("paths", nargs="+", help="Paths to remove")
    rm_parser.set_defaults(func=lambda args: devault.remove(*args.paths))

    find_parser = subparsers.add_parser("find", help="Find a repository (supports regex)")
    find_parser.add_argument("queries", nargs="+", help="Queries to search for")
    find_parser.set_defaults(func=lambda args: devault.find(*args.queries))

    new_parser = subparsers.add_parser("new", help="Create and initialize a local git repository")
    new_parser.set_defaults(func=lambda args: devault.mkrepo())

    clone_parser = subparsers.add_parser("clone", help="Clone a repository to a vault")
    clone_parser.add_argument("url", help="Repository URL to clone")
    clone_parser.add_argument("collections", nargs="*", help="Collections to add the repository to")
    clone_parser.set_defaults(func=lambda args: devault.clone(args.url, args.collections))

    update_parser = subparsers.add_parser("update", help="Pull the latest changes from upstream")
    update_parser.add_argument("paths", nargs="*", help="Paths to update")
    update_parser.set_defaults(func=lambda args: devault.update(*args.paths))

    group_parser = subparsers.add_parser("group", help="Group repositories into collections")
    group_parser.add_argument("repositories", nargs="+", help="Repositories to group")
    group_parser.add_argument("collection", help="Collection name")
    group_parser.set_defaults(func=lambda args: devault.group(*args.repositories, args.collection))

    args = parser.parse_args()

    if args.V >= 3:     logging.basicConfig(level=logging.ERROR)
    elif args.V >= 2:   logging.basicConfig(level=logging.WARNING)
    elif args.V >= 1:   logging.basicConfig(level=logging.INFO)
    elif args.V >= 0:   logging.basicConfig(level=logging.DEBUG)

    if args.version:                utils.version()
    elif hasattr(args, "func"):     args.func(args)
    else:                           parser.print_help()
