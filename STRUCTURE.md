# Directory Structure Plan (Flask-Oxide)


This file describes the recommended directory structure for this repository and the role of each directory/file. All entries use the format:

`<path>`: <role/description>


## Root Level (Flask-Oxide repository)

```
Flask-Oxide/
├── README.md
├── FEATURES.md
├── pyproject.toml
├── .github/
├── .devcontainer/
├── flask_oxide/
├── tests/
├── examples/
└── ...
```

- `README.md`: Project overview and basic information
- `FEATURES.md`: Requirements and development specifications
- `pyproject.toml`: Python project settings and dependency management
- `.github/`: Workflows and AI agent instructions
- `.devcontainer/`: Development container configuration
- `flask_oxide/`: Main extension package (see below)
- `tests/`: Unit tests (using pytest)
- `examples/`: Concrete usage examples and sample code



## Flask Extension Package

```
flask_oxide/
├── __init__.py
├── ext.py
├── config.py
├── cli.py
├── utils.py
└── ...
```

- `__init__.py`: Package initialization
- `ext.py`: Main class implementation for the Flask extension
- `config.py`: Default configuration values (constants with OXIDE_ prefix)
- `cli.py`: Command-line interface functionality
- `utils.py`: Utility and wrapper functions
- ... (other extension modules as needed)


## Tests

```
tests/
└── ...
```
- Unit tests (using pytest)


## Examples

```
examples/
└── ...
```
- Concrete usage examples and sample code

---


## User Application Structure (with Rust integration)

```
user-app-root/
├── app.py
├── rust/
│   ├── __init__.py
│   ├── <crate>/
│   │   ├── Cargo.toml
│   │   ├── <crate>.so  # or .pyd on Windows
│   │   └── ... (Rust source files)
│   └── ...
└── ...
```

- `app.py`: Main Flask application
- `rust/`: Rust source and built modules (must contain `__init__.py`)
- `rust/<crate>/`: Rust crate directory (must contain `Cargo.toml`)
- `rust/<crate>/Cargo.toml`: Rust crate definition (PyO3/maturin config)
- `rust/<crate>/<crate>.so` or `.pyd`: Built extension module
- ... (Rust source files)


## Crate Detection Rule

- Under `OXIDE_RUST_SOURCE_DIR` (default: `rust/`), any immediate subdirectory containing a `Cargo.toml` file is treated as a Rust crate.
- Each crate is built as a separate Python extension module and placed in its crate directory.
- Individual Rust source files are not treated as crates; only directories with `Cargo.toml` are considered crates.

---

> This file serves as a guideline for directory structure, crate detection, and integration patterns, for both developers and AI agents. For design rationale, see DESIGN.md.
