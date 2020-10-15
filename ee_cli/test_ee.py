"""Test the UI.
For repl tests, the input will always include an exit hotword so the tests can
actually finish."""
import pytest
from click.testing import Result
from ee_cli import utils
from ee_cli.constants import COULD_NOT_PARSE_ERROR_MESSAGE
from ee_cli.settings import Settings
from main import app
from typer.testing import CliRunner


def repl_input_factory(*strings):
    """Return the strings joined by newlines.
    Last element is always 'done' at the end so repl can exit"""
    return "\n".join([*strings, "done\n"])


def repl_frames(command_result: Result):
    """Think of each time you press enter at the repl as a 're-render'.
    The screen gets cleared, but the output doesn't go away, so we can look at it
    if we really want to.

    This gets you a list of each 'frame'"""
    return command_result.output.split("\n\n")


def last_frame(command_result: Result):
    """Technically the second to last.
    Return the last frame shown before exiting."""
    return repl_frames(command_result)[-2]


@pytest.fixture
def runner():
    return CliRunner()


def test_repl_smoke(runner):
    result = runner.invoke(app, "repl", input=repl_input_factory())
    assert result.exit_code == 0, "App starts and exits on exit hotword"


def test_repl_failed_conversion(runner):
    invalid_date = "hahahaahaha"
    result = runner.invoke(app, "repl", input=repl_input_factory(invalid_date))
    last = last_frame(result)
    assert (
        COULD_NOT_PARSE_ERROR_MESSAGE.format(date=invalid_date) in last
    ), "Error message displayed faithfully"


def test_repl_conversions(runner):
    result = runner.invoke(
        app, "repl", input=repl_input_factory("now", "tomorrow", "today")
    )
    last = last_frame(result)
    assert all(s in last for s in ["now", "tomorrow", "today"]), "No inputs get lost"
    assert "Couldn't" not in last


def test_output_format_env(runner, monkeypatch):
    monkeypatch.setattr(
        utils, "settings", Settings(custom_datetime_output_format="[Q]Q YYYY")
    )
    result = runner.invoke(app, ["flip", "0"])

    assert (
        "Q4 1969" == result.output
    ), "Respects custom output formats. (It was still 1969 in Chicago at epoch start)"
