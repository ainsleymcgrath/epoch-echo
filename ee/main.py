import typer
from click import clear
from ee.constants import HOTWORD_ACTIONS, NO_TIMES_YET_MESSAGE
from ee.utils import arrange_for_pretty_defaults_abuse, flip_time_format

from state import state

app = typer.Typer(help="Endlessly grokking time back and forth")


@app.command()
def repl(tz: str = "America/Chicago"):
    """Open a never-ending prompt that echoes back whatever time you type as the
    opposite version of itself. Give an epoch, get a datetime and vice versa.

    The repl also can take a list of timestamps separated by spaces.

    Type 'done' to be done."""

    colored_prompt = typer.style("\n\n >  ", fg=typer.colors.BRIGHT_RED)
    clear()

    while True:
        input_ = typer.prompt(
            "",
            prompt_suffix=colored_prompt,  # suffix lookin like a prefix
            default=NO_TIMES_YET_MESSAGE
            if state.no_times_set
            else arrange_for_pretty_defaults_abuse(
                [f"{s} => {flip_time_format(s)}" for s in state.times]
            ),
            show_default=True,
        )

        if input_ in HOTWORD_ACTIONS:
            HOTWORD_ACTIONS[input_]()
            continue

        state.add_time(input_)
        typer.echo(input_)
        clear()


@app.command()
def flip():
    """Non-interactive. Take a date/timestamp (or list thereof) and print them to
    stdout"""
    print("fart")
