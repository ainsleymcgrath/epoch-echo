from typing import Callable, List, Union

import pendulum
from ee_cli.constants import COULD_NOT_PARSE_ERROR_MESSAGE, PENDULUM_SEMANTIC_ATTRS
from ee_cli.settings import Settings

settings = Settings()


def mangled_prompt_default(
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


def _epoch_int_no_millis(epoch: Union[str, int, float]) -> int:
    """We reject milliseconds."""
    return int(str(epoch).split(".")[0])


def flip_time_format(date: str, tz: str = settings.default_timezone) -> str:
    """If it's an epoch get back a friendly date[time].
    If it's anything else, get an epoch."""
    # TODO: try user-defined input formats
    try:  # passing an epoch feels like primary use case--or at lest it's mine
        timestamp = _epoch_int_no_millis(date)
        return pendulum.from_timestamp(timestamp, tz=tz).to_datetime_string()
    except ValueError:
        if date in PENDULUM_SEMANTIC_ATTRS:
            # pendulum can't parse the strings in that constant (even though it should)
            # but they do exist as methods!
            value: pendulum.DateTime = getattr(pendulum, date)()
            return str(_epoch_int_no_millis(value.timestamp()))
        try:
            # here, check for custom format rules
            return str(pendulum.parse(date).timestamp()).split(".")[0]
        except pendulum.parsing.exceptions.ParserError:
            return COULD_NOT_PARSE_ERROR_MESSAGE.format(date=date)
