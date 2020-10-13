"""Entrypoint for the `ee` executable."""
from typing import List

import typer
from click import clear
from ee_cli.constants import (
    DROP_HOTWORDS,
    EXIT_HOTWORDS,
    NO_TIMES_YET_MESSAGE,
    RESET_HOTWORDS,
)
from ee_cli.ui import UserInputTransformationStore, make_dispatcher

app = typer.Typer(name="ee", help="A salve for timesmiths 🧴🕰️")


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
def repl(tz: str = "America/Chicago"):  # noqa: D103
    colored_prompt = typer.style("\n\n >  ", fg=typer.colors.BRIGHT_RED)
    clear()  # create a sort of full-screen view
    user_input_transformations = UserInputTransformationStore()

    dispatch = make_dispatcher(
        [RESET_HOTWORDS, user_input_transformations.clear],
        [DROP_HOTWORDS, user_input_transformations.pop],
        [EXIT_HOTWORDS, exit],
        default=user_input_transformations.append,
    )

    while True:
        input_ = typer.prompt(
            "",
            prompt_suffix=colored_prompt,  # suffix lookin like a prefix
            default=user_input_transformations or NO_TIMES_YET_MESSAGE,
            show_default=True,
        )

        dispatch(input_)
        clear()


@app.command()
def flip(dates: List[str]):
    """`repl` without the prompt.
    Takes a list of dates/timestamps (mixing them works fine)"""
    store = UserInputTransformationStore(*dates)
    typer.echo(store)
