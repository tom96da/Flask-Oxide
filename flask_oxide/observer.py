# Copyright (c) 2026 tom96da

"""Flask-Oxide Rust source file observer and event handler."""

import pathlib
import threading
import time

from flask import Flask, current_app
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from .builder import build_crate


class RustObserver:
    """Manages the lifecycle of the Rust source file observer."""

    def __init__(self, oxide: object) -> None:
        """Initialize the RustObserver.

        Args:
            oxide: The FlaskOxide extension instance.
        """
        self.oxide = oxide
        self._observer = None
        self._observer_thread = None

    def start(self, app: Flask) -> None:
        """Start the Rust source file observer using watchdog."""
        if self._observer:
            return  # Already running
        rust_dir = app.config["OXIDE_RUST_SOURCE_DIR"]
        watch_mode = app.config["OXIDE_RUST_WATCH_MODE"]
        event_handler = RustEventHandler(self.oxide)
        observer = Observer()
        observer.schedule(event_handler, rust_dir, recursive=True)
        self._observer = observer
        if watch_mode == "thread":
            t = threading.Thread(target=observer.start, daemon=True)
            t.start()
            self._observer_thread = t
        else:
            observer.start()

    def stop(self) -> None:
        """Stop the Rust source file observer if running."""
        if self._observer:
            self._observer.stop()
            # Only join if the thread was started and is alive
            if self._observer_thread and self._observer_thread.is_alive():
                self._observer.join()
            self._observer = None
        self._observer_thread = None


class RustEventHandler(FileSystemEventHandler):
    """Watchdog event handler for Rust source changes in Flask-Oxide."""

    def __init__(self, oxide: object) -> None:
        """Initialize the RustEventHandler.

        Args:
            oxide: The FlaskOxide extension instance.
        """
        super().__init__()
        self.oxide = oxide
        self._last_event = 0.0

    def on_any_event(self, event: FileSystemEvent) -> None:
        """Handle any file system event for Rust source files."""
        if self._should_ignore_event(event):
            return
        src_path = str(event.src_path)
        now = time.monotonic()
        if now - self._last_event < float(
            current_app.config["OXIDE_RUST_RELOAD_DEBOUNCE"]
        ):
            return
        self._last_event = now
        current_app.logger.info("[oxide] Rust file change detected: %s", src_path)
        build_ok = True
        if current_app.config["OXIDE_RUST_BUILD_ON_CHANGE"]:
            build_ok = self._safe_build()
        if build_ok and current_app.config["OXIDE_RUST_RELOAD_ENABLED"]:
            reload_fn = getattr(self.oxide, "reload", None)
            if callable(reload_fn):
                reload_fn()

    @staticmethod
    def _should_ignore_event(event: FileSystemEvent) -> bool:
        src_path = str(event.src_path)
        rust_dir = current_app.config["OXIDE_RUST_SOURCE_DIR"]
        watch_exts = set(current_app.config["OXIDE_RUST_WATCH_EXTENSIONS"])
        ignore_dirs = set(current_app.config["OXIDE_RUST_WATCH_IGNORE"])
        return (
            event.is_directory
            or not any(src_path.endswith(ext) for ext in watch_exts)
            or any(
                part in pathlib.Path(src_path).relative_to(rust_dir).parts
                for part in ignore_dirs
            )
        )

    @staticmethod
    def _safe_build() -> bool:
        rust_dir = current_app.config["OXIDE_RUST_SOURCE_DIR"]
        # Use the root crate (".") for monorepo or single crate
        return build_crate(
            rust_dir,
            crate=".",
            release=current_app.config["OXIDE_RUST_BUILD_COMMAND"].endswith(
                "--release"
            ),
        )
