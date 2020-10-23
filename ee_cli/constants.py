"""Some things never change."""
import typer

from ee_cli.settings import Settings

settings = Settings()

EXIT_HOTWORDS = {"end", "exit", "done", "quit", "q"}
RESET_HOTWORDS = {"clear", "restart", "c"}
DROP_HOTWORDS = {"drop", "remove", "rm", "d"}
TOGGLE_INDEX_HOTWORDS = {"index", "idx", "indexes", "i"}
HELP_HOTWORDS = {"help", "h", "?"}
SHOW_CONFIG_HOTWORDS = {"config", "settings", "variables", "vars", "env"}
GO_BACK_HOTWORDS = {"back"}
COPY_HOTWORDS = {"copy", "yy", "cp"}
SPECIAL_KEYS = {}

PENDULUM_SEMANTIC_ATTRS = {"tomorrow", "today", "yesterday"}

COULD_NOT_PARSE_ERROR_MESSAGE = "Couldn't parse: {date}. Try again?."
NO_TIMES_YET_MESSAGE = "Transformations added to the list as you type them"
HELP_HEADER = typer.style(
    "\n   Type the word 'back' to leave this screen\n\n", typer.colors.BRIGHT_MAGENTA
)

HOTWORDS_HELP = f"""
To exit the repl use: {typer.style(str(EXIT_HOTWORDS), typer.colors.RED)}.
[ctrl + d] and [ctrl + c] also work.

To remove the last item from the list use: {typer.style(str(DROP_HOTWORDS), typer.colors.RED)}.
To remove arbitrary items, include the 0-based index of the item.
i.e. `drop 3` will drop the 4th item shown on screen.

To send all your conversions to the clipboard, use {typer.style(str(COPY_HOTWORDS), typer.colors.RED)}.
This will exit the repl.

To clear the list use: {typer.style(str(RESET_HOTWORDS), typer.colors.RED)}.

To inspect your configuration (env vars) use: {typer.style(str(SHOW_CONFIG_HOTWORDS), typer.colors.RED)}.

To see this help in the repl use: {typer.style(str(HELP_HOTWORDS), typer.colors.RED)}.
 """  # the space is intentional

CONFIGURATION_INFO = (
    "\n".join(f"{k.upper()}: {v or '<unset>'}" for k, v in settings.dict().items())
    + "\n "
)
