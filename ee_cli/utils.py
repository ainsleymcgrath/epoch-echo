from typing import Callable, List

import pendulum


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


def flip_time_format(date: str, tz: str = "America/Chicago") -> str:
    """If it's an epoch get back a friendly date[time].
    If it's anything else, get an epoch"""

    try:
        timestamp = int(date)
        return pendulum.from_timestamp(timestamp, tz=tz).format(
            "ddd[,] MMM D YYYY HH:mm:ss"
        )
    except ValueError:
        try:
            return str(pendulum.parse(date).timestamp()).split(".")[0]
        except pendulum.parsing.exceptions.ParserError:
            return f"Couldn't parse: {date}"