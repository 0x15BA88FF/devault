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

### Added

- Add an install / uninstall shell script
- Add unit test data
- Template URL parser test case.
- Repository name validation.
- Quick prompt helper function.
- Python logging functionality.
- Python build test workflow.
- Python pylint workflow.

### Changed

- User logger setLever method for verbosity argument 
- User more descriptive variable names
- Restructured codebase.
- Adhered to pylint guidelines.
- Improved `argparse` input parsing and output.
- Renamed helper functions to more descriptive names.
- Modified helper functions (`touch`, `mkdir`, `ln`, `ls`) to accept a single path parameter.
- Converted all URL groups to lowercase during parsing.
- Renamed `DEVAULT_DIR` environment variable to `DEVDIR`.

### Removed

- Replaced exit utility with `sys.exit()`.

### Fixed

- prevent invalid method .lower() on NoneType in url parser
- Prevented devault actions from escaping the `DEVDIR` sandbox.
- Fixed collection creation from splitting characters.
- Prevented collections from duplicating.
- Prevented repositories from creating collections of themselves.
- Prevented invalid regex query injection.
- Prevented starter content from being created outside the repository.
- Added a maximum recursion depth to prevent unnecessary and infinite recursion.

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
[0.0.1]: https://github.com/0x15ba88ff/devault/releases/tag/v0.0.1-alpha
