"""Entrypoint for `ee`.
Functions not decorated with @app are actions to affect state"""
import readline  # noqa: F401
from typing import List

import pyperclip
import typer
from click import clear

from ee_cli import __version__
from ee_cli.constants import HOTWORDS_HELP
from ee_cli.content import dispatch, visible_content
from ee_cli.ui import EchoList

app = typer.Typer(name="ee", help="A salve for timesmiths 🧴🕰️")


@app.command(
    help=f"""
In an infinite prompt, give an epoch, get a datetime, and vice versa.

Can be controlled with various redundant hotwords:

{HOTWORDS_HELP} """
)
def repl(tz: str = "America/Chicago"):
    """Give an epoch, get a datetime. And vice versa."""
    colored_prompt = typer.style("\n\n >  ", fg=typer.colors.BRIGHT_RED)
    clear()  # create a full-screen view

    while True:
        try:
            input_ = typer.prompt(
                "",
                prompt_suffix=colored_prompt,  # suffix lookin like a prefix
                default=visible_content(),
                show_default=True,
            )
        except typer.Abort:
            # see the quit function for why this is happening
            quit()

        dispatch(input_)
        clear()


@app.command()
def flip(dates: List[str], copy: bool = False, plain: bool = False):
    """`repl` without the prompt.
    Takes a list of dates/timestamps (mixing them works fine)"""
    output = EchoList(*dates)
    if copy:
        pyperclip.copy(output.plain_str())
        typer.echo(
            f"Converted date{'s' if len(dates) > 1 else ''} copied to clipboard."
        )
        return

    typer.echo(output.plain_str() if plain else output)


def _version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


# pylint: disable=unused-argument
@app.callback()
def _(
    version: bool = typer.Option(
        None, "--version", "-v", callback=_version_callback, is_eager=True
    )
):
    """Print the version and exit.."""
