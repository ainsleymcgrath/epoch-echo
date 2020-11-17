"""Entrypoint for `ee`.
Functions not decorated with @app are actions to affect state"""
import readline  # noqa: F401
from typing import List

import pyperclip
import typer
from click import clear

from ee_cli import __doc__, __version__
from ee_cli.constants import HOTWORDS_HELP
from ee_cli.content import dispatch, visible_content
from ee_cli.ui import EchoList

app = typer.Typer(name="ee", help="A salve for timesmiths 🧴🕰️")


def _repl():
    """Run the interface for interactively transforming dates."""
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


def _version_callback(value: bool, ctx: typer.Context):
    """For --version."""
    if value:
        if len(ctx.args) or any(v for v in ctx.params.values()):
            raise typer.Abort("--version must be called alone.")

        typer.echo(__version__)
        raise typer.Exit()

    return value


def _exclusivity_check(ctx: typer.Context):
    """Make sure arguments don't get called in combination that don't make sense.
    It's not `app.callback` decorated b/c that's only for apps w multiple commands"""
    if ctx.params["repl"] is True:
        ctx.params.pop("repl")
        # everything gotta be falsey
        if any(v for v in ctx.params.values()) or len(ctx.args):
            raise typer.Abort("--repl must be called alone.")

    return ctx


@app.command(help=__doc__, no_args_is_help=True)
def main(
    ctx: typer.Context,
    dates: List[str] = typer.Argument(
        None,
        help="Dates/datetimes separated by spaces.\n"
        "Can be in the style of an epoch timestamp (milliseconds will be ignored) or\n"
        "in any of the formats specified in EXTRA_DATETIME_INPUT_FORMATS",
    ),
    copy: bool = typer.Option(
        False,
        "--copy",
        "-c",
        is_flag=True,
        show_default=False,
        help="Send output to the clipboard.",
    ),
    plain: bool = typer.Option(
        False,
        "--plain",
        "-p",
        is_flag=True,
        show_default=False,
        help="Don't show pretty output, just transformations.",
    ),
    repl: bool = typer.Option(
        False,
        "--repl",
        "-r",
        is_flag=True,
        show_default=False,
        help="In an infinite prompt, give an epoch, get a datetime, and vice versa.\n"
        "Can be controlled with various redundant hotwords:\n"
        f"{HOTWORDS_HELP}",
    ),
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=_version_callback,
        help="Print the version and exit",
    ),
):
    """Acts as the entrypoint for `ee`."""
    _exclusivity_check(ctx)

    if repl:
        _repl()
        return

    output = EchoList(*dates)
    if copy:
        pyperclip.copy(output.plain_str())
        typer.echo(
            f"Converted date{'s' if len(dates) > 1 else ''} copied to clipboard."
        )
        return

    typer.echo(output.plain_str() if plain else output)
