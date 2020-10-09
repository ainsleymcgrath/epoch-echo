from typing import Callable, List

import typer
from click import clear

app = typer.Typer(help="Endlessly grokking time back and forth")

NO_TIMES_YET_MESSAGE = "Transformations added to the list as you type them"


class _State:
    times = []

    def reset_times(self):
        clear()
        self.times = []

    def add_time(self, time):
        self.times.append(time)

    @property
    def no_times_set(self):
        return len(self.times) == 0


state = _State()


def _quit():
    raise typer.Exit


HOTWORD_ACTIONS = {
    "clear": state.reset_times,
    "restart": state.reset_times,
    "end": _quit,
    "exit": _quit,
    "quit": _quit,
}


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
            else arrange_for_pretty_defaults_abuse(state.times),
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
    """Fart!"""
    print('fart')


def arrange_for_pretty_defaults_abuse(
    items, should_format: Callable[[List[str]], bool] = len
) -> str:
    """Format a list of items so they'll look nice in the prompt, which we are abusing
    by showing output in it. Ultimately, in the CLI defaults, it'll look like this:

 [
   item
   item
   item
 ]

    The space prefixing the first bracket is automatically added by click.
    There's a suffix of a newline followed by a single space in the function output.
    That aligns the closing bracket with the first.
    The items within are indented 2 spaces relative to the position of the bracket"""

    THREE_SPACES = " " * 3
    indented_items = "\n".join(f"{THREE_SPACES}{i}" for i in items)
    return f"\n{indented_items}\n " if should_format(items) else ""


def flip_format(date: str) -> str:
    """If it's an epoch get back a friendly date[time].
    If it's anything else, get an epoch"""
