# Flask-Oxide: Requirements & Development Specifications

## Project Purpose
Provide a Flask extension that enables seamless integration and development of Rust modules with a developer experience equivalent to native Python during Flask application development.

## Key Features (in order of priority)

### 1. Hot Reload for Rust Files (Highest Priority)
- Detect changes in Rust files under `rust/` just like Flask's auto-reload for Python files.
- Automatically compile Rust files on change and reload the Flask app to reflect updates immediately.
- Emphasize consistency in the development experience.

### 2. Pythonic Import of Rust Modules
- Allow importing Rust sources in the `rust/` directory as if they were regular Python modules, e.g., `from .rust import xxx`.
- Make calling Rust code intuitive and seamless.

### 3. Automatic Initialization of Rust Projects
- Initialize a Rust project/directory in a specified location with a single Flask command.
- No manual setup required.

### 4. One-liner Production Rust Build
- Enable one-liner production Rust builds from a Flask command (build_crate/build_all_crates API).
- Minimize deployment effort.

---

## Additional Notes & Development Policy
- Features are prioritized from top to bottom.
- Consistency and intuitiveness of the development experience are top priorities.
- Detailed design and command specifications will be discussed and implemented in the future.

---

> This file is intended for GitHub Copilot and other AI agents, as well as developers, to quickly understand the project's goals, priorities, and features.
