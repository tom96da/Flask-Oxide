# Copyright (c) 2026 tom96da
"""Flask-Oxide exceptions."""


class FlaskOxideError(Exception):
    """Base exception for Flask-Oxide errors."""


class UnsafeBuildCommandError(FlaskOxideError, RuntimeError):
    """Raised when an unsafe build command is detected."""


class BuildError(FlaskOxideError, RuntimeError):
    """Raised when a Rust build process fails."""
