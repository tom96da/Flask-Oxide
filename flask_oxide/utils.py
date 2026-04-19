# Copyright (c) 2026 tom96da

"""Flask-Oxide public API utility functions."""

from typing import TYPE_CHECKING

from flask import current_app


if TYPE_CHECKING:
    from .ext import FlaskOxide


def build_crate(crate: str, *, release: bool = False) -> bool:
    """Build a single Rust crate via the FlaskOxide extension instance.

    Args:
        crate (str): The crate to build (directory name).
        release (bool, optional): Build in release mode. Defaults to False.

    Returns:
        bool: True if build succeeded, False otherwise.
    """
    oxide: FlaskOxide = current_app.extensions["oxide"]
    return oxide.build_crate(crate=crate, release=release)


def build_all_crates(*, release: bool = False) -> bool:
    """Build all Rust crates via the FlaskOxide extension instance.

    Args:
        release (bool, optional): Build in release mode. Defaults to False.

    Returns:
        bool: True if all builds succeeded, False otherwise.
    """
    oxide: FlaskOxide = current_app.extensions["oxide"]
    return oxide.build_all_crates(release=release)


def list_crates() -> list[str]:
    """List detected Rust crate names via the FlaskOxide extension instance.

    Returns:
        list[str]: List of crate names.
    """
    oxide: FlaskOxide = current_app.extensions["oxide"]
    return oxide.list_crates()


def reload() -> None:
    """Trigger Flask app reload via the FlaskOxide extension instance.

    Returns:
        None
    """
    oxide: FlaskOxide = current_app.extensions["oxide"]
    return oxide.reload()
