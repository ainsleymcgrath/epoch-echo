from typing import List

import typer
from click import clear
from ee_cli.constants import (
    DROP_HOTWORDS,
    NO_TIMES_YET_MESSAGE,
    RESET_HOTWORDS,
    EXIT_HOTWORDS,
)
from ee_cli.ui import make_dispatcher, UserInputTransformationStore

app = typer.Typer(help="Endlessly grokking time back and forth")


@app.command()
def repl(tz: str = "America/Chicago"):
    """Open a never-ending prompt that echoes back whatever time you type as the
    opposite version of itself. Give an epoch, get a datetime and vice versa.

    The repl also can take a list of timestamps separated by spaces.

    Type 'done' to be done."""

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
    """Non-interactive. Take a date/timestamp (or list thereof) and print them to
    stdout"""
    store = UserInputTransformationStore(*dates)
    typer.echo(store)
