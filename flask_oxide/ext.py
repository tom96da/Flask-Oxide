# Copyright (c) 2026 tom96da

"""Flask-Oxide extension core implementation."""

import os
import pathlib

from flask import Flask, current_app

from . import config
from .builder import build_all_crates, build_crate
from .observer import RustObserver


class FlaskOxide:
    """Flask-Oxide extension for Rust integration."""

    def __init__(self, app: Flask | None = None) -> None:
        """Initialize the FlaskOxide extension and optionally register with a Flask app.

        This sets up the extension and optionally registers it with a Flask app.
        """
        self._observer = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Register the extension with the Flask app and set default config."""
        self.init_config(app)
        app.extensions["oxide"] = self
        # Start watcher only in debug mode and if enabled
        if app.debug and app.config["OXIDE_RUST_WATCH"]:
            self._start_rust_watcher(app)

        @app.teardown_appcontext
        def _oxide_teardown(_exc: BaseException | None = None) -> None:
            self._stop_rust_watcher()

    def _start_rust_watcher(self, app: Flask) -> None:
        """Start the Rust source file watcher using RustWatcherManager."""
        if self._observer is None:
            self._observer = RustObserver(self)
        self._observer.start(app)

    def _stop_rust_watcher(self) -> None:
        """Stop the Rust source file watcher if running."""
        if self._observer:
            self._observer.stop()

    @staticmethod
    def init_config(app: Flask) -> None:
        """Set default configuration values for Flask-Oxide from config.py."""
        for key in dir(config):
            if key.startswith("OXIDE_"):
                value = getattr(config, key)
                app.config.setdefault(key, value)

    def list_crates(self) -> list[str]:
        """List all Rust crates (Cargo.toml) in the rust source directory.

        Returns:
            list[str]: List of crate names.
        """
        crates: list[str] = []
        rust_dir = self._get_rust_dir()
        rust_path = pathlib.Path(rust_dir)
        if not rust_path.is_dir():
            return crates
        for entry in rust_path.iterdir():
            crate_path = entry
            if crate_path.is_dir() and (crate_path / "Cargo.toml").is_file():
                crates.append(entry.name)
        # Also support single crate in rust_dir (Cargo.toml directly under rust/)
        if (rust_path / "Cargo.toml").is_file():
            crates.append(rust_path.name)
        return crates

    def build_crate(self, crate: str, *, release: bool = False) -> bool:
        """Build a single specified Rust crate using cargo build.

        (Delegates to builder.py.)

        Args:
            crate (str): The crate to build (directory name).
            release (bool, optional): Build in release mode. Defaults to False.

        Returns:
            bool: True if build succeeded, False otherwise.
        """
        rust_dir = self._get_rust_dir()
        return build_crate(rust_dir, crate, release=release)

    def build_all_crates(self, *, release: bool = False) -> bool:
        """Build all Rust crates using build_crate (delegates to builder.py).

        Args:
            release (bool, optional): Build in release mode. Defaults to False.

        Returns:
            bool: True if all builds succeeded, False otherwise.
        """
        rust_dir = self._get_rust_dir()
        crate_list = self.list_crates()
        return build_all_crates(rust_dir, crate_list, release=release)

    @staticmethod
    def reload() -> None:
        """Trigger Flask app reload."""
        main_file: str | None = current_app.config.get("FLASK_APP")
        if main_file and pathlib.Path(main_file).is_file():
            os.utime(main_file)

    @staticmethod
    def _get_rust_dir() -> str:
        return current_app.config["OXIDE_RUST_SOURCE_DIR"]
