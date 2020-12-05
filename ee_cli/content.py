"""Define and control the state of what user sees during `ee --repl`."""
from textwrap import indent
from typing import Callable, Tuple, Union

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


def content_state() -> Tuple[
    Callable[[str], None], Callable[[], Union[EchoList, OptionallyLatentString, str]]
]:
    """Provide faculties for getting & setting state: the content in the user's repl.
    The `state` tuple specifies in priority order of what should appear in the repl
    based on the truthiness of its members.
    The first truthy value contains the content that should be presented.
    Functions scoped in here alter state based on messages passed from the user's input.
    """
    state = (
        EchoList(),
        OptionallyLatentString(HELP_HEADER + indent(HOTWORDS_HELP, "   ")),
        OptionallyLatentString(HELP_HEADER + indent(CONFIGURATION_INFO, "   ")),
        NO_TIMES_YET_MESSAGE,
    )
    user_inputs, help_, config, _ = state  # NO_TIMES_YET_MESSAGE never changes.

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
        """Add an item to the store for transformation.

        If the item is the inital message, don't add it to state. Why? Well...
        In `.main`, the `default` kwarg passed to `typer.prompt` is always whatever is
        "visible" according to the dispatcher. On an empty input for the user, the
        "visible" value is `NO_TIMES_YET_MESSAGE`. So, we keep the EchoList instance
        empty until something other than that is on the screen."""
        if item == NO_TIMES_YET_MESSAGE:
            return

        user_inputs.append(item)

    def quit():
        """Leave the repl."""
        raise typer.Exit

    def show_help():
        """Make help visible by toggling the latent property of `help_`."""
        help_.latent = not help_.latent

    def show_config():
        """Make configuration visible by toggling the latent property on `config`."""
        config.latent = not config.latent

    def go_back():
        """Make all latent strings latent again so they do not show on screen.
        Bump `user_inputs` the highest priority piece of state."""
        for string in [config, help_]:
            string.latent = True

    def copy_to_clipboard():
        """Copy all visible conversion results to the clipboard."""
        pyperclip.copy(user_inputs.plain_str())
        typer.echo(
            f"Converted date{'s' if len(user_inputs) > 1 else ''} copied to clipboard."
        )
        quit()

    dispatch_alter_visible_content: Callable[[str], None] = make_dispatcher(
        (RESET_HOTWORDS, clear_list),
        (DROP_HOTWORDS, drop_list_item),
        (TOGGLE_INDEX_HOTWORDS, toggle_index),
        (EXIT_HOTWORDS, quit),
        (HELP_HOTWORDS, show_help),
        (SHOW_CONFIG_HOTWORDS, show_config),
        (GO_BACK_HOTWORDS, go_back),
        (COPY_HOTWORDS, copy_to_clipboard),
        default=append_to_list,
    )

    def visible_content():
        """Return the first string-ish state object that is not falsey at the moment."""
        return next(x for x in state if len(x))

    return dispatch_alter_visible_content, visible_content
