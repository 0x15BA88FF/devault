# Dev Vault

## Overview

Dev Vault is a minimal command-line tool designed to manage your Git repositories.  
It provides functionality for initializing environments, organizing them into collections, and more.

## Features

- **Organize Repositories**: Clone and create repositories from various providers into your vault in a well-structured manner.
- **Find Repositories**: Search for repositories using regex patterns.
- **Group Repositories**: Organize repositories into collections for easier management.
- **Create Local Repositories**: Initialize a new local Git repository with starter content.

## Installation

### 1. UNIX Install Script

On UNIX operating systems, you can use the install script:

```bash
sh <(curl https://raw.githubusercontent.com/0x15BA88FF/devault/refs/heads/main/scripts/install.sh)
```

### 2. Build from Source

Alternatively, use a package builder like PyInstaller to build an executable from the source code:

```bash
git clone https://github.com/0x15BA88FF/devault.git
cd ./devault

pip install pyinstaller
pyinstaller --onefile --name devault --paths devault devault/__main__.py
```

## Uninstallation

### 1. UNIX Uninstall Script

On UNIX operating systems, you can use the uninstall script:

```bash
sh <(curl https://raw.githubusercontent.com/0x15BA88FF/devault/refs/heads/main/scripts/uninstall.sh)
```

### 2. Manual Removal

If installed via the UNIX install script, the binary will be in `/usr/bin`. Simply remove it:

```bash
sudo rm /usr/bin/devault
```

If you installed it elsewhere, remove it from the corresponding directory.

## Usage

### Command Line Interface

Interact with Dev Vault through the command line:

```bash
devault --help
devault <command> --help
```

## Configuration

The tool uses an environment variable `DEVDIR` to define the base directory for managing repositories.  
If this variable is not set, it defaults to `~/Dev`. Set it in your shell configuration file:

```bash
export DEVAULT_DIR="/path/to/your/dev/vault"
```

## TODO

> Feature: update repos by group / user provider using wildcard.

> Preview make repo output.

> Feature: using repositories as templates.


## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to enhance the functionality of Dev Vault.

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE. See the [LICENSE](LICENSE) file for more information.
