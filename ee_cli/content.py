"""Dispatch actions that determine the user-facing content.

`dispatch` and `visible_content` are the major players here.
All other functions are in service of affecting state."""
from textwrap import indent
from typing import Callable

import pyperclip
import typer

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
from ee_cli.ui import EchoList, OptionallyLatentString, make_dispatcher

# UI state data is stored in these variables
user_inputs = EchoList()
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
    """Drop the value at the specifed indexes."""
    if not indexes:
        user_inputs.pop()

    for index in indexes:
        user_inputs.pop(index)


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
    pyperclip.copy(user_inputs.plain_str())
    typer.echo(
        f"Converted date{'s' if len(user_inputs) > 1 else ''} copied to clipboard."
    )
    quit()


dispatch: Callable[[str], None] = make_dispatcher(
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


def visible_content():
    """Return the first string-ish state object that is not falsey at the moment."""
    return next(x for x in [help_, config, user_inputs, NO_TIMES_YET_MESSAGE] if len(x))
