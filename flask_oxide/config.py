# Copyright (c) 2026 tom96da

"""Flask-Oxide configuration constants."""

from typing import Final, Literal


OXIDE_RUST_SOURCE_DIR: Final = "rust"
"""The root directory where Rust crates are located."""

OXIDE_RUST_WATCH: Final = True
"""Enable or disable Rust source file watching."""

OXIDE_RUST_WATCH_EXTENSIONS: Final = [".rs"]
"""File extensions to watch for Rust source changes."""

OXIDE_RUST_WATCH_IGNORE: Final = ["target", ".git"]
"""Directories to ignore when watching for changes."""

OXIDE_RUST_RELOAD_ENABLED: Final = True
"""Enable or disable Flask app reload on Rust changes."""

OXIDE_RUST_RELOAD_DEBOUNCE: Final = 0.5
"""Debounce time (seconds) for reload events after Rust changes."""

OXIDE_RUST_BUILD_ON_CHANGE: Final = True
"""Automatically build Rust crates when changes are detected."""

OXIDE_RUST_BUILD_COMMAND: Final = "cargo build"
"""The shell command used to build Rust crates."""

OXIDE_RUST_MATURIN_ARGS: Final = []
"""Extra arguments to pass to maturin when building Rust crates."""

OXIDE_RUST_BUILD_ERROR_MODE: Final[Literal["log", "raise"]] = "log"
"""How to handle Rust build errors: 'log' to log errors, 'raise' to raise exceptions."""

OXIDE_RUST_WATCH_MODE: Final[Literal["thread", "process"]] = "thread"
"""File watch mode: 'thread' for in-process, 'process' for subprocess-based watching."""

OXIDE_LOG_LEVEL: Final[Literal["DEBUG", "INFO", "WARNING", "ERROR"]] = "INFO"
"""Log level for Flask-Oxide extension logging."""
