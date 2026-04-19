# Flask-Oxide: Detailed Design

This document describes the detailed design of the Flask-Oxide extension, based on the requirements in FEATURES.md and additional specifications provided.

## 1. Extension Architecture

### 1.1 Overview
Flask-Oxide is a Flask extension that enables seamless integration of Rust modules into Flask applications, providing a native Python developer experience. The extension is designed to be discoverable, configurable, and extensible, following Flask's best practices.


### 1.2 Modularization and Core Modules

Flask-Oxide is organized into the following core modules to ensure strict separation of concerns and maintainability:

- **ext.py**: Main Flask extension entrypoint. Defines the `FlaskOxide` class, coordinates watcher and build logic, and exposes the public API.
- **observer.py**: Implements all Rust source file watching logic. Contains `RustObserver` (watcher lifecycle management) and `RustEventHandler` (event handling). Delegates build actions to `builder.py`.
- **builder.py**: Implements all Rust build logic. Contains only build-related functions such as `build_crate` and `build_all_crates`. Dedicated to build operations; does not include any watcher logic.
- **utils.py**: Provides wrapper functions for the public API, calling into the extension instance via `current_app`.

This modularization ensures:
- All watcher logic is in `observer.py` (no build logic here)
- All build logic is in `builder.py` (no watcher logic here)
- `ext.py` (FlaskOxide) only coordinates and delegates, keeping the extension entrypoint simple and maintainable
- All public API is exposed via `FlaskOxide` and `utils.py`.


### 1.3 FlaskOxide Class and Public API
The core extension class is `FlaskOxide` (in ext.py):
  - `__init__(self, app: Flask = None)`: Optionally takes a Flask app instance. If provided, calls `init_app(app)`.
  - `init_app(self, app: Flask)`: Registers the extension with the Flask app, sets up configuration, attaches the extension instance to `app.extensions['flask-oxide']` and automatically registers CLI commands.
  - `init_config(self, app: Flask)`: Sets default configuration values using `app.config.setdefault` for all extension-specific settings. Default values are defined in `config.py`.
  - Rust source monitoring and build are triggered automatically when Rust source files are updated. Manual invocation of these processes is not required in typical usage.
  - Error handling and all operational behaviors are consistently controlled via configuration values (see 1.6 Configuration Management for details).
  - CLI commands are registered automatically at `init_app` and cover all necessary operations for development and production, including:
    - Rust project (subdirectory) initialization
    - Development build
    - Production build
    - (Other CLI operations as required)
    - Other operations required from development to production
  - Additional methods and properties are added as needed to fulfill the requirements in FEATURES.md (e.g., import hooks, advanced configuration, etc).

### 1.3.1 RustObserver and RustEventHandler
The core watcher logic is implemented in `observer.py` and consists of the following classes:

- **RustObserver**: Manages the lifecycle of the Rust source file watcher.
  - `__init__(self, oxide)`: Stores a reference to the FlaskOxide extension instance.
  - `start(self, app: Flask)`: Starts the file watcher (thread or process backend, depending on configuration). Sets up the observer and event handler.
  - `stop(self)`: Stops the file watcher and cleans up resources.
  - Maintains internal state for observer and thread management.
  - Responsible for clean startup/shutdown and delegating event handling to RustEventHandler.

- **RustEventHandler**: Handles file system events for Rust source files.
  - `__init__(self, oxide)`: Stores a reference to the FlaskOxide extension instance.
  - `on_any_event(self, event)`: Called on any file system event. Applies debounce, filtering, and triggers build/reload as appropriate.
  - `_should_ignore_event(event)`: Determines if the event should be ignored (e.g., by extension or ignored directory).
  - `_safe_build()`: Triggers a safe build via builder.py, handling errors per configuration.
  - Responsible for enforcing debounce, filtering, and correct build/reload flow.

#### Public API
The public API of Flask-Oxide is defined as public methods of the `FlaskOxide` class.
Additionally, wrapper functions that call these methods via `current_app` are implemented in `utils.py`, and these are imported and exposed in `__init__.py` as the package's public API.

Main public API examples:
- `build_crate(self, crate: str, release: bool = False) -> bool`: Build a single Rust crate.
- `build_all_crates(self, release: bool = False) -> bool`: Build all Rust crates.
- `list_crates(self) -> list[str]`: Get a list of Rust crate names.
- `reload(self)`: Reload the Flask application.

Users can import these via `from flask_oxide import build_crate, build_all_crates, list_crates, reload`.


### 1.4 Exception Classes
The following exception classes are defined in exc.py:

- `FlaskOxideError`: Base exception for Flask-Oxide errors.
- `UnsafeBuildCommandError`: Raised when an unsafe build command is detected.
- `BuildError`: Raised when a Rust build process fails.


### 1.5 Extension Registration
- The extension instance is registered in `app.extensions['flask-oxide']` so it can be accessed from the Flask app context or via `current_app.extensions['flask-oxide']`.


### 1.6 Configuration Management
- Default configuration values are defined in `flask_oxide/config.py` as constants with type hints (`Final`).
- All required configuration values must be defined as constants in `config.py` and use the `OXIDE_` prefix.
- When setting these values to `app.config`, import the config module and use a loop to set all constants starting with `OXIDE_`.

**Example:**
```python
# config.py
from typing import Final

OXIDE_RUST_SOURCE_DIR: Final[str] = "rust"
OXIDE_RUST_WATCH: Final[bool] = True
# ... other config values ...

# app initialization
import config
for key in dir(config):
    if key.startswith('OXIDE_'):
        app.config[key] = getattr(config, key)
```

#### Core Configuration Options
| Key                           | Default              | Description                                                                        |
| ----------------------------- | -------------------- | ---------------------------------------------------------------------------------- |
| `OXIDE_RUST_SOURCE_DIR`       | `"rust"`             | Directory for Rust source and built modules (Python package).                      |
| `OXIDE_RUST_WATCH`            | `True`               | Monitor Rust source files for changes.                                             |
| `OXIDE_RUST_WATCH_EXTENSIONS` | `[".rs"]`            | File extensions to watch for changes.                                              |
| `OXIDE_RUST_WATCH_IGNORE`     | `["target", ".git"]` | Subdirectories to ignore when watching.                                            |
| `OXIDE_RUST_RELOAD_ENABLED`   | `True`               | Reload Flask app on Rust source changes.                                           |
| `OXIDE_RUST_RELOAD_DEBOUNCE`  | `0.5`                | Debounce time (seconds) for reload events.                                         |
| `OXIDE_RUST_BUILD_ON_CHANGE`  | `True`               | Build Rust code automatically on changes.                                          |
| `OXIDE_RUST_BUILD_COMMAND`    | `"cargo build"`      | Command to build Rust code.                                                        |
| `OXIDE_RUST_MATURIN_ARGS`     | `[]`                 | Extra arguments for maturin build.                                                 |
| `OXIDE_RUST_BUILD_ERROR_MODE` | `"log"`              | Rust build error handling: `"log"` or `"raise"`.                                   |
| `OXIDE_RUST_WATCH_MODE`       | `"thread"`           | Backend for Rust source watcher: `"thread"` (default, recommended) or `"process"`. |
| `OXIDE_LOG_LEVEL`             | `"INFO"`             | Log level for extension output: "DEBUG", "INFO", "WARNING", "ERROR".             |

All configuration keys are prefixed with `OXIDE_` to avoid conflicts.


---
## 2. Rust Source Change Detection & Hot Reload

### 2.1 Purpose
Automatically detect changes in Rust source files during development and, as needed, trigger a Rust build and reload the Flask application.

**Implementation Note:**
All watcher logic is implemented in `observer.py` (see 1.2), and all build logic is implemented in `builder.py`. The watcher delegates build actions to the builder module, ensuring strict separation of concerns.


### 2.2 Components and Specifications
 - Watch target directory: `OXIDE_RUST_SOURCE_DIR` (default: "rust")
 - Watched file extensions: `OXIDE_RUST_WATCH_EXTENSIONS` (e.g., [".rs"])
 - Excluded directories: `OXIDE_RUST_WATCH_IGNORE` (e.g., ["target", ".git"])
 - Build on change: `OXIDE_RUST_BUILD_ON_CHANGE` (True to enable build)
 - Build command: `OXIDE_RUST_BUILD_COMMAND` (e.g., "cargo build")
 - Reload on change: `OXIDE_RUST_RELOAD_ENABLED` (True to enable Flask reload)
 - Debounce interval: `OXIDE_RUST_RELOAD_DEBOUNCE` (seconds to suppress rapid events)
 - Watcher is only active in development mode (`app.debug` is True)
 - **Watcher backend (thread/process):** The watcher can run either as a sub-thread (default, recommended) or sub-process. This is controlled by the configuration value `OXIDE_RUST_WATCH_MODE` ("thread" or "process"). The default is chosen for best compatibility and performance, but can be changed by the user if needed.
  - **Error handling mode:** Rust build error handling is controlled by `OXIDE_RUST_BUILD_ERROR_MODE`. This determines whether errors are logged and the process continues (`"log"`), or a dedicated exception is raised (`"raise"`).


### 2.3 Detailed Flow
1. On Flask app initialization, if `app.debug` is True, start the Rust source watcher.
2. Use `watchdog.Observer` to recursively watch under `OXIDE_RUST_SOURCE_DIR`.
3. The event handler only processes file changes matching `OXIDE_RUST_WATCH_EXTENSIONS` and ignores paths under `OXIDE_RUST_WATCH_IGNORE`.
4. On event, if it occurs within `OXIDE_RUST_RELOAD_DEBOUNCE` seconds of the last event, ignore it (debounce); otherwise, proceed.
5. If `OXIDE_RUST_BUILD_ON_CHANGE` is True, execute `OXIDE_RUST_BUILD_COMMAND` as a subprocess. **If the build fails, suppress Flask reload, output only a log, and continue monitoring.**
6. If the build fails, handle the error according to `OXIDE_RUST_BUILD_ERROR_MODE`:
  - If set to `"log"`, log the error and continue monitoring (suppress Flask reload).
  - If set to `"raise"`, raise `OxideRustBuildError` and halt further processing.
7. If `OXIDE_RUST_RELOAD_ENABLED` is True and the build succeeded, trigger Flask reload (see below for method).
7. Ensure the watcher thread/process is cleanly stopped when the Flask app shuts down.


### 2.4 Design Notes
- Clearly handle subprocess errors and log output.
 - Flask reload methods should provide a development experience equivalent to Python source reload (e.g., Werkzeug reloader). Prefer the same mechanism as Flask's built-in reloader (such as touching the main app file or using the reloader API). The method should be abstracted for future extension.
 - Implement clean shutdown for watcher threads/processes.
 - All configuration values must be retrieved from `app.config`; avoid hardcoding.


### 2.5 Extensibility
Make the watch targets, build command, and reload method flexible via configuration for future extension.
Design to allow for future features such as notification hooks or custom build scripts.

The watcher backend (thread/process) is selectable via the `OXIDE_RUST_WATCH_MODE` configuration value. By default, `"thread"` is used for best compatibility and performance, but users can set `"process"` if their environment requires it. On build failure, Flask reload is suppressed and only a log is output; monitoring continues. The reload method should match Flask's standard development experience (e.g., Werkzeug reloader behavior).


---
## 3. Rust-Python Interoperability

### 3.1 Purpose
Enable seamless import and usage of Rust modules in Python code within Flask applications, providing a native Python experience.


### 3.2 Components and Specifications
- Rust modules are built as Python extension modules using PyO3 and maturin.
- The Rust source directory (`OXIDE_RUST_SOURCE_DIR`) may contain one or more Rust crates (e.g., `rust/foo`, `rust/bar`), each with a `Cargo.toml` configured for PyO3/maturin. Each crate is built as a separate Python extension module, and the directory structure supports flexible import patterns such as `from rust.foo import func`.
- Build process is triggered on source change (in dev mode) or via CLI, using maturin with optional extra arguments (`OXIDE_RUST_MATURIN_ARGS`).
- Built extension modules are placed directly within the Rust source directory (`OXIDE_RUST_SOURCE_DIR`), which must be structured as a valid Python package (i.e., must contain an `__init__.py`). This allows the Rust source directory itself to be imported as a Python module or package (e.g., `import rust.my_rust`). The project root is never used for extension placement.
- Python code can import the Rust module as a native module.
- All configuration is managed via `app.config`.


### 3.3 Detailed Flow
1. Developer writes Rust code with PyO3 annotations in the configured source directory.
2. On source change or CLI invocation, maturin builds the Rust crate as a Python extension module (`.so`/`.pyd`).
3. Each built extension is copied/moved into its corresponding crate directory under `OXIDE_RUST_SOURCE_DIR` (e.g., `rust/foo/foo.so`). Each crate directory must be a valid Python package (must contain `__init__.py`). This enables flexible import patterns such as `from rust.foo import func`.
4. The built extension module is automatically renamed (if necessary) to ensure it can be imported as `from rust.<crate> import ...` (e.g., `foo.so`), regardless of maturin's default output name.
4. Python code imports the Rust module directly (e.g., `import my_rust`).
5. All build and import paths are configurable for flexibility.


### 3.4 Design Notes
- Ensure maturin and PyO3 are required dependencies and properly documented.
- Support for multiple Rust crates/modules in the source directory.
- Handle build errors gracefully and provide clear logs.
- Allow for future extension (e.g., custom build steps, post-processing).


### 3.5 Extensibility
- Support for additional build arguments, custom output directories, and multiple module management.
- Design for future integration with other build tools or workflows.


### 3.6 Dependencies
- **PyO3**: Rust crate for creating Python bindings and native extension modules.
- **maturin**: Tool for building and publishing Rust-based Python packages.
- **watchdog**: Python package for file system monitoring (already required for reload logic).


### 3.7 Example Rust Project (PyO3)
```toml
[package]
name = "my_rust"
version = "0.1.0"

[lib]
name = "my_rust"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "*", features = ["extension-module"] }

[package.metadata.maturin]
python-source = false
```

```rust
use pyo3::prelude::*;

#[pyfunction]
fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[pymodule]
fn my_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add, m)?)?;
    Ok(())
}
```


### 3.8 Python Import Example
```python
# Flexible import patterns are supported:
import rust.foo
from rust.foo import add
from rust.bar import some_func
# Build API usage:
from flask_oxide import build_crate, build_all_crates
build_crate(crate="foo", release=True)
build_all_crates(release=True)
```


### 3.9 Development Workflow Summary
1. Developer writes Rust code with PyO3 annotations in the configured source directory.
2. On save (in dev mode) or via CLI, FlaskOxide triggers maturin to build the extension.
3. The built extension is placed in the Rust source directory, which is a valid Python package and thus importable.
4. Python code can import the Rust module directly.


---
## 4. File Structure

The directory structure and its rationale are described in detail in [STRUCTURE.md](../STRUCTURE.md). Please refer to that file for the latest and authoritative information.


---
## 5. Design Considerations
- The design must support all features and priorities described in FEATURES.md, including hot reload, import hooks, CLI, and build integration.
- The extension should be discoverable and usable in a standard Flask way, with clear configuration and context access patterns.


---
## 6. CLI Commands

Flask-Oxide provides a set of CLI commands for managing Rust integration and development lifecycle. All commands are registered under the Flask CLI (`flask oxide ...`).

### 6.1 Command List and Specifications

| Command | Arguments/Options              | Description                                                                         |
| ------- | ------------------------------ | ----------------------------------------------------------------------------------- |
| `init`  | `[crate_name]`                 | Initialize a new Rust crate under `OXIDE_RUST_SOURCE_DIR` with PyO3/maturin config. |
| `build` | `[--release] [--crate <name>]` | Build all or a specific Rust crate(s) as Python extension modules.                  |
| `watch` |                                | Start file watcher for Rust source changes and auto-build/reload in dev mode.       |
| `list`  |                                | List all detected Rust crates under `OXIDE_RUST_SOURCE_DIR`.                        |

#### 6.2 Command Details

- `init [crate_name]`: Creates a new subdirectory under `OXIDE_RUST_SOURCE_DIR` with a minimal `Cargo.toml` and PyO3/maturin configuration. Also creates `__init__.py` for Python package import.
- `build [--release] [--crate <name>]`: Builds all crates or a specified crate. Uses maturin with appropriate arguments. On error, handles per `OXIDE_RUST_BUILD_ERROR_MODE`.
- `watch`: Starts the file watcher for Rust source changes. Only active in development mode.
- `list`: Lists all detected crates (subdirectories with `Cargo.toml`) under `OXIDE_RUST_SOURCE_DIR`.

All commands output status and errors to the Flask CLI. Error handling follows the configuration (log or raise). Command help and usage are available via `flask oxide --help`.

### 6.3 Error Handling Policy
- Flask-Oxide only handles errors directly related to Rust integration (Rust build failures, watcher errors, extension module placement errors). These are controlled by configuration values such as `OXIDE_RUST_BUILD_ERROR_MODE`.
- Errors outside the scope of Rust integration (e.g., Flask app bugs, Python standard exceptions, CLI argument errors, unrelated external tool failures) are not handled by Flask-Oxide and will propagate normally (causing CLI abnormal exit or standard exception behavior).


---
## 7. Crate Detection Rule

Under `OXIDE_RUST_SOURCE_DIR`, any immediate subdirectory that contains a `Cargo.toml` file is treated as a Rust crate. Each such crate is built as a separate Python extension module. Individual Rust source files are not treated as crates; only directories with `Cargo.toml` are considered crates.


---

> This document is intended for developers and AI agents to guide implementation and ensure consistency with project requirements.
