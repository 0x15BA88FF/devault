# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

- ## Types of changes

  - **Added**: New features.
  - **Changed**: Modifications to existing functionality.
  - **Deprecated**: Features that will be removed in the future.
  - **Removed**: Features that have been removed.
  - **Fixed**: Bug fixes.
  - **Security**: Addressed vulnerabilities.

---

## [Unreleased]

### Changed

- Update changelog.
- Use absolute paths.
- Use `repository_name` instead of `name`.

### Fixed

- Fix group function linking to nonexistent directories.
- Prevent creating collections outside the dev directory.
- Prevent creating collections inside the hosts directory.

## [1.2.2] - 2024-12-21

### Added

- Add an install/uninstall shell script.
- Add unit test data.
- Template URL parser test case.
- Repository name validation.
- Quick prompt helper function.
- Python logging functionality.
- Python build test workflow.
- Python pylint workflow.

### Changed

- Use logger setLevel method for verbosity argument.
- Use more descriptive variable names.
- Restructure codebase.
- Adhere to pylint guidelines.
- Improve `argparse` input parsing and output.
- Rename helper functions to more descriptive names.
- Modify helper functions (`touch`, `mkdir`, `ln`, `ls`) to accept a single path parameter.
- Convert all URL groups to lowercase during parsing.
- Rename `DEVAULT_DIR` environment variable to `DEVDIR`.

### Removed

- Replace exit utility with `sys.exit()`.

### Fixed

- Prevent invalid method .lower() on NoneType in URL parser.
- Prevent devault actions from escaping the `DEVDIR` sandbox.
- Fix collection creation from splitting characters.
- Prevent collections from duplicating.
- Prevent repositories from creating collections of themselves.
- Prevent invalid regex query injection.
- Prevent starter content from being created outside the repository.
- Add a maximum recursion depth to prevent unnecessary and infinite recursion.

## [0.0.1] - 2024-12-15

### Added

- `init` command to initialize a dev vault for repository management.
- `ls` command to list entities within the vault.
- `rm` command to remove specified entities.
- `find` command to locate a repository using regex support.
- `clone` command to clone a repository into the vault.
- `update` command to pull the latest changes from the upstream repository.
- `group` command to organize repositories into collections.
- `mkrepo` command to create and initialize a local Git repository.

[unreleased]: https://github.com/0x15ba88ff/devault/compare/v1.1.1...HEAD
[1.2.2]: https://github.com/0x15ba88ff/devault/releases/tag/v1.2.2-beta
[0.0.1]: https://github.com/0x15ba88ff/devault/releases/tag/v0.0.1-alpha

