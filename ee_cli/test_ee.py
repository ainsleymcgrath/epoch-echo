"""Test the UI.
For repl tests, the input will always include an exit hotword so the tests can
actually finish."""
import pyperclip
import pytest
from click.testing import Result
from typer.testing import CliRunner

from ee_cli import ui, utils
from ee_cli.constants import COULD_NOT_PARSE_ERROR_MESSAGE, NO_TIMES_YET_MESSAGE
from ee_cli.main import app
from ee_cli.settings import Settings


@pytest.fixture(autouse=True)
def turn_off_tz_heads_up(monkeypatch):
    monkeypatch.setattr("ee_cli.main.MAYBE_TZ_HEADS_UP", "")
    monkeypatch.setattr("ee_cli.constants.MAYBE_TZ_HEADS_UP", "")


def repl_input_factory(*strings):
    """Return the strings joined by newlines.
    Last element is always 'done' at the end so repl can exit"""
    return "\n".join([*strings, "done\n"])


def repl_frames(command_result: Result):
    """Think of each time you press enter at the repl as a 're-render'.
    The screen gets cleared, but the output doesn't go away, so we can look at it
    if we really want to.

    This gets you a list of each 'frame'"""
    return command_result.output.split("\n\n >  ")


def last_frame(command_result: Result):
    """Technically the second to last.
    Return the last frame shown before exiting."""
    return repl_frames(command_result)[-2]


@pytest.fixture
def runner():
    return CliRunner()


def test_repl_smoke(runner):
    result = runner.invoke(app, "--repl", input=repl_input_factory())
    assert result.exit_code == 0, "App starts and exits on exit hotword"


def test_repl_failed_conversion(runner):
    invalid_date = "hahahaahaha"
    result = runner.invoke(app, "--repl", input=repl_input_factory(invalid_date))
    last = last_frame(result)
    assert (
        COULD_NOT_PARSE_ERROR_MESSAGE.format(date=invalid_date) in last
    ), "Error message displayed faithfully"


def test_repl_conversions(runner):
    INPUTS = "now", "tomorrow", "today", "Feb 1 2021", "Jan 02 2021", "01-01-22"
    result = runner.invoke(app, "--repl", input=repl_input_factory(*INPUTS))

    last = last_frame(result)
    assert all(s in last for s in INPUTS), "No inputs get lost"
    assert "Couldn't" not in last


def test_repl_with_index_always_env(runner, monkeypatch):
    monkeypatch.setattr(
        # overriding settings has the same effect as using an env var
        ui,
        "settings",
        Settings(show_indexes_always=True),
    )

    result = runner.invoke(app, "--repl", input=repl_input_factory("now"))
    last = last_frame(result)
    # there are pretty brackets and whitespace around the conversion
    _, _, conversion, _ = last.split("\n")
    assert conversion.lstrip().startswith("0"), "The index of the conversion is visible"


def test_repl_with_extra_input_formats_env(runner, monkeypatch):
    monkeypatch.setattr(
        # overriding settings has the same effect as using an env var
        utils,
        "settings",
        Settings(extra_datetime_input_formats=["MMM D YYYY"]),
    )
    result = runner.invoke(app, ["Jan 30 2018"])

    assert "1517292000" in result.output, "Respects custom input formats."


def test_repl_copy_hotword(runner):
    runner.invoke(app, "--repl", input=repl_input_factory("now", "copy"))
    assert pyperclip.paste() == "790495200"


def test_repl_reset(runner):
    result = runner.invoke(
        app, "--repl", input=repl_input_factory("now", "now", "clear")
    )
    last = last_frame(result)
    assert NO_TIMES_YET_MESSAGE in last


def test_repl_config(runner):
    result = runner.invoke(app, "--repl", input=repl_input_factory("config"))
    last = last_frame(result)
    assert all(name.upper() in last for name in Settings().dict().keys())


def test_repl_config_and_back(runner):
    result = runner.invoke(app, "--repl", input=repl_input_factory("config", "back"))
    last = last_frame(result)
    assert not any(name.upper() in last for name in Settings().dict().keys())


def test_repl_help(runner):
    result = runner.invoke(app, "--repl", input=repl_input_factory("help"))
    last = last_frame(result)
    assert "help" in last


def test_repl_help_and_back(runner):
    result = runner.invoke(app, "--repl", input=repl_input_factory("help", "back"))
    last = last_frame(result)
    assert "help" not in last


def test_repl_drop(runner):
    result = runner.invoke(
        app,
        "--repl",
        # first, drop the conversion for "2"
        # then drop it for "poop"
        input=repl_input_factory("yesterday", "poop", "0", "2", "drop", "drop 1"),
    )
    last = last_frame(result)
    assert "poop" not in last
    assert "2 =>" not in last


@pytest.mark.parametrize("blank_input", [("\n"), (""), ("\n", "5", "")])
def test_repl_repeat_enter_key(blank_input, runner):
    """I encountered a bug during usage where pressing <enter> without having typed
    anything into the prompt caused the app to break."""
    result = runner.invoke(app, "--repl", input=repl_input_factory(*blank_input))
    assert result.exit_code == 0, "Pressing enter without having typed anything is ok."


def test_flip_with_output_format_env(runner, monkeypatch):
    monkeypatch.setattr(
        # overriding settings has the same effect as using an env var
        utils,
        "settings",
        Settings(custom_datetime_output_format="[Q]Q YYYY"),
    )
    result = runner.invoke(app, ["0"])

    assert (
        "Q4 1969" in result.output
    ), "Respects custom output formats. (It was still 1969 in Chicago at epoch start)"


def test_flip_with_copy_flag(runner):
    # no result needed bc testing against clipboard
    runner.invoke(app, ["2020-12-12", "--copy"])
    assert pyperclip.paste() == "1607752800", "Converted date is sent to clipboard"


def test_flip_plain(runner):
    result = runner.invoke(app, ["2020-12-12", "--plain"])
    assert (
        "=>" not in result.output and " " not in result.output
    ), "Characters that show up in formatting are not shown"


@pytest.mark.parametrize(
    "args, exit_code, message",
    [
        ("--plain", 0, "--plain can be used alone."),
        ("--repl 1 2 3", 1, "--repl can't be used with args passed"),
        ("--repl --copy --plain", 1, "--repl can't be used with other options"),
    ],
)
def test_arg_exclusivity(args, exit_code, message, runner):
    result = runner.invoke(app, args.split(" "))
    assert result.exit_code == exit_code, message
