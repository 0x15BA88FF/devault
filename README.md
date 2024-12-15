# Dev Vault Dx100 - BETA

## Overview

Dev Vault is a minimal command-line tool designed to manage your Git repositories efficiently. It provides functionality for initializing a development environment, cloning repositories, organizing them into collections, and more.

## Features

- **Clone Repositories**: Clone Git repositories from various providers (e.g., GitHub, GitLab) into your vault.
- **Find Repositories**: Search for repositories using regex patterns.
- **Group Repositories**: Organize repositories into collections for easier management.
- **Create Local Repositories**: Initialize a new local Git repository with starter content.

## Installation

### Git Clone

1. **Clone the Repository**:
   ```bash
   git clone https://https://github.com/0x15BA88FF/devault.git
   cd ./devault
   ```

## Usage

### Command Line Interface

You can interact with Dev Vault through the command line. Here are the available commands:

```bash
dev <command> [args]
```

- **help**: Show a list of command-line options.
- **version**: Show the current version of the tool.
- **init**: Initialize a dev vault.
- **ls**: List entities in the vault.
- **rm**: Remove an entity from the vault.
- **find <query>**: Find a repository (supports regex).
- **clone <repo-url> [collections]**: Clone a repository to the vault and optionally add it to collections.
- **update [repositories]**: Pull the latest changes from upstream for specified repositories.
- **group <repositories> <collection>**: Group repositories into a specified collection.
- **mkrepo**: Create and initialize a local Git repository.

### Examples

- **Initialize a Vault**:
  ```bash
  dev init
  ```

- **Clone a Repository**:
  ```bash
  dev clone https://https://github.com/0x15BA88FF/devault.git
  ```

- **List Repositories**:
  ```bash
  dev ls learning/bash
  ```

- **Find a Repository**:
  ```bash
  dev find rust$
  ```

- **Group Repositories**:
  ```bash
  dev group repo1 repo2 my_collection
  ```

## Configuration

The tool uses an environment variable `DEVAULT_DIR` to define the base directory for managing repositories. If this variable is not set, it defaults to `~/Dev`. You can set it in your shell configuration file:

```bash
export DEVAULT_DIR="/path/to/your/dev/vault"
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to enhance the functionality of Dev Vault.

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE. See the [LICENSE](LICENSE) file for more information.