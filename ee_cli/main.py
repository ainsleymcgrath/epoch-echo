"""Entrypoint for the `ee` executable."""
from typing import List

import typer
from click import clear
from ee_cli.constants import (
    DROP_HOTWORDS,
    EXIT_HOTWORDS,
    NO_TIMES_YET_MESSAGE,
    RESET_HOTWORDS,
    TOGGLE_INDEX_HOTWORDS,
)
from ee_cli.ui import TransformedUserInputStore, make_dispatcher

app = typer.Typer(name="ee", help="A salve for timesmiths 🧴🕰️")

user_inputs = TransformedUserInputStore()


def toggle_index():
    user_inputs.show_index = not user_inputs.show_index


def clear_list():
    user_inputs.clear()


def drop_list_item(*indexes):
    if not indexes:
        user_inputs.pop()
        return

    user_inputs._working_list = [
        item
        for idx, item in enumerate(user_inputs._working_list)
        if str(idx) not in indexes
    ]


def append_to_list(item):
    user_inputs.append(item)


def quit():
    raise typer.Exit


def show_help():
    ...


dispatch = make_dispatcher(
    [RESET_HOTWORDS, clear_list],
    [DROP_HOTWORDS, drop_list_item],
    [TOGGLE_INDEX_HOTWORDS, toggle_index],
    [EXIT_HOTWORDS, quit],
    default=append_to_list,
)


@app.command(
    help=f"""In an infinite prompt, give an epoch, get a datetime. And vice versa.

    Can be controlled with various redundant hotwords:

        To exit the repl use: {EXIT_HOTWORDS}
        [ctrl + d] and [ctrl + c] also work.

        To remove the last item from the list use: {DROP_HOTWORDS}
        To remove arbitrary items, include the 0-based index of the item.
        i.e. `drop 3` will drop the 4th item shown on screen.

        To clear the list use: {RESET_HOTWORDS}"""
)
def repl(tz: str = "America/Chicago"):
    """Give an epoch, get a datetime. And vice versa."""
    colored_prompt = typer.style("\n\n >  ", fg=typer.colors.BRIGHT_RED)
    clear()  # create a full-screen view

    while True:
        input_ = typer.prompt(
            "",
            # suffix lookin like a prefix
            prompt_suffix=colored_prompt,
            # the 'default' is being used as the main UI element for the user
            # by passing multiline strings in, it can be used to display lists and
            # blocks of text
            default=user_inputs or NO_TIMES_YET_MESSAGE,
            show_default=True,
        )

        dispatch(input_)
        clear()


@app.command()
def flip(dates: List[str]):
    """`repl` without the prompt.
    Takes a list of dates/timestamps (mixing them works fine)"""
    store = TransformedUserInputStore(*dates)
    typer.echo(store)
