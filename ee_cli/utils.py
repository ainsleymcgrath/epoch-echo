"""Utility functions. Lots of work with strings."""
from typing import Union

import pendulum

from ee_cli.constants import COULD_NOT_PARSE_ERROR_MESSAGE, PENDULUM_SEMANTIC_ATTRS
from ee_cli.settings import Settings

settings = Settings()


def _epoch_int_no_millis(epoch: Union[str, int, float]) -> int:
    """We reject milliseconds."""
    return int(str(epoch).split(".")[0])


def flip_time_format(date: str, tz: str = settings.default_timezone) -> str:
    """If it's an epoch get back a friendly date[time].
    If it's anything else, get an epoch."""
    try:  # passing an epoch feels like primary use case--or at lest it's mine
        timestamp = _epoch_int_no_millis(date)
        return (
            pendulum.from_timestamp(timestamp, tz=tz).to_datetime_string()
            if not settings.custom_datetime_output_format
            else pendulum.from_timestamp(timestamp, tz=tz).format(
                settings.custom_datetime_output_format
            )
        )
    # it's not an epoch if we make it here
    except ValueError:
        if date in PENDULUM_SEMANTIC_ATTRS:
            # pendulum can't parse the strings in that constant (even though it should)
            # but they do exist as methods!
            value: pendulum.DateTime = getattr(pendulum, date)(tz=tz)
            return str(_epoch_int_no_millis(value.timestamp()))
        try:
            maybe_epoch = try_parse_formats(
                date, *settings.extra_datetime_input_formats
            )
            return (
                maybe_epoch
                or str(pendulum.parse(date, tz=tz).timestamp()).split(".")[0]
            )
        except pendulum.parsing.exceptions.ParserError:
            return COULD_NOT_PARSE_ERROR_MESSAGE.format(date=date)


def try_parse_formats(date: str, *formats: str, tz: str = settings.default_timezone):
    """Try calling pendulum.parse with each of the supplied formats."""
    for format in formats:
        try:
            timestamp = pendulum.from_format(date, format, tz=tz).timestamp()
            return str(_epoch_int_no_millis(timestamp))
        except ValueError:
            continue
