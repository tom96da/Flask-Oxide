# Copyright (c) 2026 tom96da

"""Flask-Oxide Rust build logic and integration."""

import pathlib
import re
import subprocess  # noqa: S404

from flask import current_app


def build_crate(rust_dir: str, crate: str, *, release: bool = False) -> bool:
    """Build a single specified Rust crate using cargo build.

    Args:
        rust_dir (str): The root directory containing Rust crates.
        crate (str): The crate to build (directory name).
        release (bool, optional): Build in release mode. Defaults to False.

    Returns:
        bool: True if build succeeded, False otherwise.
    """
    rust_path = pathlib.Path(rust_dir)
    # Validate crate name: only allow alphanumeric, underscore, hyphen
    if not re.match(r"^[\w-]+$", crate):
        current_app.logger.error("Invalid crate name: %s", crate)
        return False
    crate_path = (rust_path / crate).resolve()
    # Ensure crate_path is under rust_path
    try:
        crate_path.relative_to(rust_path.resolve())
    except ValueError:
        current_app.logger.error("Crate path escapes rust directory: %s", crate_path)
        return False
    if not crate_path.is_dir():
        return False
    cargo_toml = crate_path / "Cargo.toml"
    if not cargo_toml.is_file():
        return False
    cmd = ["cargo", "build"]
    if release:
        cmd.append("--release")
    try:
        current_app.logger.debug("Running cargo build: %r in %s", cmd, crate_path)
        subprocess.run(  # noqa: S603
            cmd,
            cwd=crate_path,
            check=True,
            shell=False,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        current_app.logger.error(
            "Rust build failed in %s: %s\n%s", crate_path, exc, exc.stderr
        )
        return False
    return True


def build_all_crates(
    rust_dir: str, crate_list: list[str], *, release: bool = False
) -> bool:
    """Build all Rust crates using build_crate.

    Args:
        rust_dir (str): The root directory containing Rust crates.
        crate_list (list[str]): List of crate directory names.
        release (bool, optional): Build in release mode. Defaults to False.

    Returns:
        bool: True if all builds succeeded, False otherwise.
    """
    results = [build_crate(rust_dir, crate, release=release) for crate in crate_list]
    return all(results)
