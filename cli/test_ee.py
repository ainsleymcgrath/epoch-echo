import pytest
from typer.testing import CliRunner

from main import app


@pytest.fixture
def runner():
    return CliRunner()


def test_repl(runner):
    result = runner.invoke(app, ["repl"], input="ok\nsure\nexit")
    assert result.exit_code == 0
