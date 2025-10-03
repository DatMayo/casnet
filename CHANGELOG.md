# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-03

### Added
- **Persistent Database**: Migrated from an in-memory data model to a persistent SQLite database using SQLAlchemy 2.0.
- **SQLAlchemy Models**: Introduced a new `src/models/` directory for all database models.
- **Pydantic Schemas**: Created a `src/schemas/` directory for all data validation and serialization schemas.
- **Password Hashing**: Centralized password hashing logic in a new `src/hashing.py` file to resolve circular imports.
- **`.gitkeep`**: Added a `.gitkeep` file to the `data/` directory to ensure it is tracked by Git.
- **`CONTRIBUTING.md`**: Added a guide for contributors.
- **`CHANGELOG.md`**: This file, to track project changes.

### Changed
- **Project Architecture**: Refactored the entire application to be database-driven.
- **Routers**: Updated all API routers to use SQLAlchemy sessions for data operations instead of in-memory lists.
- **Configuration**: Updated `src/config.py` to use `pydantic-settings`.
- **`README.md`**: Overhauled the documentation to reflect the new architecture, removing all mentions of the in-memory database and updating project structure and setup instructions.
- **`.gitignore`**: Updated to correctly ignore the SQLite database file while tracking the `data/` directory.

### Removed
- **In-Memory Database**: Removed all logic related to the old in-memory data store from `src/database.py` and `src/util.py`.
- **`src/model/` Directory**: Deleted the obsolete `src/model/` directory, which has been replaced by `src/schemas/`.

### Fixed
- **`sqlalchemy.exc.InvalidRequestError`**: Resolved the "Table is already defined" error by removing duplicate model definitions.
- **Circular Imports**: Fixed multiple circular import errors by refactoring the security and database modules.
- **`SyntaxError`**: Corrected invalid parameter ordering in all `update` functions across the API routers.
- **`NameError` & `ModuleNotFoundError`**: Fixed all remaining import errors to allow the server to start successfully.
