import typer

EXIT_HOTWORDS = {"end", "exit", "done", "quit"}
RESET_HOTWORDS = {"clear", "restart"}
DROP_HOTWORDS = {"drop", "remove", "rm"}
HELP_HOTWORDS = {}
SPECIAL_KEYS = {}


def _quit():
    raise typer.Exit


HOTWORD_ACTIONS = {
    # hotword: _quit if hotword in EXIT_HOTWORDS else state.reset_times
    # for hotword in [*EXIT_HOTWORDS, *RESET_HOTWORDS]
}

NO_TIMES_YET_MESSAGE = "Transformations added to the list as you type them"
