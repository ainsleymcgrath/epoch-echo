"""Entrypoint for `ee`.
Functions not decorated with @app are actions to affect state"""
import readline  # noqa: F401
from textwrap import indent
from typing import List

import pyperclip
import typer
from click import clear

from ee_cli import __version__
from ee_cli.constants import (
    CONFIGURATION_INFO,
    COPY_HOTWORDS,
    DROP_HOTWORDS,
    EXIT_HOTWORDS,
    GO_BACK_HOTWORDS,
    HELP_HEADER,
    HELP_HOTWORDS,
    HOTWORDS_HELP,
    NO_TIMES_YET_MESSAGE,
    RESET_HOTWORDS,
    SHOW_CONFIG_HOTWORDS,
    TOGGLE_INDEX_HOTWORDS,
)
from ee_cli.ui import OptionallyLatentString, TransformedUserInputStore, make_dispatcher
from ee_cli.utils import flip_time_format

app = typer.Typer(name="ee", help="A salve for timesmiths 🧴🕰️")


# UI state data is stored in these variables
user_inputs = TransformedUserInputStore()
help_ = OptionallyLatentString(HELP_HEADER + indent(HOTWORDS_HELP, "   "))
config = OptionallyLatentString(HELP_HEADER + indent(CONFIGURATION_INFO, "   "))


# the following functions affect state
def toggle_index():
    """Show/hide the index of transformed items in the repl."""
    user_inputs.show_index = not user_inputs.show_index


def clear_list():
    """Clear all transformations from the repl."""
    user_inputs.clear()


def drop_list_item(*indexes):
    """Drop the value at any of the specifed indexes.
    Drop [-1] if no index provided."""
    if not indexes:
        user_inputs.pop()
        return

    user_inputs._working_list = [
        item
        for idx, item in enumerate(user_inputs._working_list)
        if str(idx) not in indexes
    ]


def append_to_list(item):
    """Add an item to the store for transformation."""
    user_inputs.append(item)


def quit():
    """Leave the repl.

    As of this moment, state needs to be cleaned up on exit in service of testing.
    During the lifecycle of test invocation, the state variables stick around across
    runs for some reason."""
    user_inputs.clear()
    help_.latent = True
    config.latent = True
    raise typer.Exit


def show_help():
    """Make help visible by toggling the latent property of `help_`."""
    help_.latent = not help_.latent


def show_config():
    """Make your configuration visible by toggling the latent property on `config`."""
    config.latent = not config.latent


def go_back():
    """Make all latent strings latent again so they do not show on screen."""
    for string in [config, help_]:
        string.latent = True


def copy_to_clipboard():
    """Copy all visible conversion results to the clipboard."""
    values = "\n".join(map(flip_time_format, user_inputs._working_list))
    pyperclip.copy(values)
    typer.echo(
        f"Converted date{'s' if len(user_inputs) > 1 else ''} copied to clipboard."
    )
    quit()


dispatch = make_dispatcher(
    [RESET_HOTWORDS, clear_list],
    [DROP_HOTWORDS, drop_list_item],
    [TOGGLE_INDEX_HOTWORDS, toggle_index],
    [EXIT_HOTWORDS, quit],
    [HELP_HOTWORDS, show_help],
    [SHOW_CONFIG_HOTWORDS, show_config],
    [GO_BACK_HOTWORDS, go_back],
    [COPY_HOTWORDS, copy_to_clipboard],
    default=append_to_list,
)


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
        visible_content = next(
            (x for x in [help_, config, user_inputs] if len(x)), NO_TIMES_YET_MESSAGE
        )
        try:
            input_ = typer.prompt(
                "",
                prompt_suffix=colored_prompt,  # suffix lookin like a prefix
                default=visible_content,
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
    if copy:
        text = "\n".join(map(flip_time_format, dates))
        pyperclip.copy(text)
        typer.echo(
            f"Converted date{'s' if len(dates) > 1 else ''} copied to clipboard."
        )
        return

    output = (
        "\n".join(map(flip_time_format, dates))
        if plain
        else TransformedUserInputStore(*dates)  # __str__ on this makes a pretty list
    )
    typer.echo(output)


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
