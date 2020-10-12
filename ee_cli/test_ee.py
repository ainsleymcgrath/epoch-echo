import pytest
from main import app
from typer.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


def test_repl(runner):
    result = runner.invoke(app, ["repl"], input="done")
    assert result.exit_code == 0, "App starts and exits on"
