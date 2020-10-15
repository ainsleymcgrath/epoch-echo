"""Test the UI.
For repl tests, the input will always include an exit hotword so the tests can
actually finish."""
import pytest
from click.testing import Result
from main import app
from typer.testing import CliRunner


@pytest.fixture
def repl_input_factory():
    """Return the strings joined by newlines.
    Last element is always 'done' at the end so repl can exit"""

    def _repl_input_factory(*strings):
        return "\n".join([*strings, "done"])

    return _repl_input_factory


@pytest.fixture
def repl_frames():
    """Think of each time you press enter at the repl as a 're-render'.
    The screen gets cleared, but the output doesn't go away, so we can look at it
    if we really want to.

    This gets you a list of each 'frame'"""

    def _repl_frames(command_result: Result):
        return command_result.output.split("\n\n")

    return _repl_frames


@pytest.fixture
def last_frame(repl_frames):
    """Technically the second to last.
    Return the last frame shown before exiting."""

    def _last_frame(command_result: Result):
        return repl_frames(command_result)[-2]

    return _last_frame


@pytest.fixture
def runner():
    return CliRunner()


def test_repl_smoke(runner, repl_input_factory):
    result = runner.invoke(app, ["repl"], input=repl_input_factory())
    assert result.exit_code == 0, "App starts and exits an exit hotword"


def test_repl_conversions(runner, repl_input_factory, last_frame):
    result = runner.invoke(
        app, ["repl"], input=repl_input_factory("now", "tomorrow", "today")
    )
    last = last_frame(result)
    assert all(s in last for s in ["now", "tomorrow", "today"])
