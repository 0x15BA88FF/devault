import argparse
from main import *


COMMAND_NAME = "dev"


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
