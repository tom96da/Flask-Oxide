# Copyright (c) 2026 tom96da

"""Flask-Oxide CLI integration."""

import click

from flask.cli import with_appcontext

from .utils import build_all_crates, build_crate, list_crates


@click.group()
def oxide() -> None:
    """Flask-Oxide CLI commands."""


@oxide.command()
@click.argument("crate", required=False)
@click.option("--release", is_flag=True, help="Build in release mode.")
@with_appcontext
def build(crate: str | None = None, *, release: bool = False) -> None:
    """Build Rust extension(s). If no crate is specified, build all.

    Raises:
        click.ClickException: If the Rust build fails.
    """
    if crate:
        success = build_crate(crate, release=release)
    else:
        success = build_all_crates(release=release)
    if not success:
        msg = "Rust build failed."
        raise click.ClickException(msg)


@oxide.command(name="list")
@with_appcontext
def list() -> None:  # noqa: A001
    """List detected Rust crates."""
    crates = list_crates()
    for c in crates:
        click.echo(c)
