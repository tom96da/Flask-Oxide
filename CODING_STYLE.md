# Coding Style Guide for Flask-Oxide

This document defines the coding conventions and best practices for the Flask-Oxide project. All contributors must follow these guidelines to ensure code quality and maintainability.

## 1. Linting and Formatting
- **Ruff** is used for linting and style checks. Configuration is managed in `pyproject.toml`.
- Code must pass all Ruff checks before submission.

## 2. Type Hints
- Use explicit type hints for all function and method signatures, including arguments and return types.
- Avoid using `Any` unless absolutely necessary.

## 3. Docstrings
- All public functions, methods, and classes must have docstrings in **Google style**.
- Docstrings should include:
  - **Title** (one-line summary)
  - **Description** (optional, for more details)
  - **Args**: List and describe all arguments with types
  - **Returns**: Describe the return value and its type
  - **Raises**: (if applicable) List exceptions raised

## 4. File and Directory Structure
- Follow the structure described in `STRUCTURE.md`.
- Place tests in the `tests/` directory, mirroring the source structure where possible.

## 5. Configuration
- All configuration should be managed via `pyproject.toml` where possible.
- Linting and formatting tools must be configured here.

## 6. Testing
- Use **pytest** for all tests.
- Place all test files in the `tests/` directory.
- Test files should be named `test_*.py`.
- Write tests for all public APIs and critical logic.

## 7. General Python Best Practices
- Use snake_case for functions, methods, and variables.
- Use PascalCase for class names.
- Avoid global variables.
- Keep functions and methods small and focused.
- Use list comprehensions and generator expressions where appropriate.

## 8. Rust Integration
- Follow the same style and documentation rigor for Rust code (when present).
- Document Rust modules and their Python bindings clearly.

---
For questions or clarifications, refer to the maintainers or open an issue.
