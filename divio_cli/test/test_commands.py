import os

import pytest
from click.testing import CliRunner

from divio_cli import cli


TEST_COMMANDS_CLICK = (
    "doctor",
    ("doctor", "-m"),
    ("doctor", "-c", "login"),
    ("login", "--check"),
    "project",
    ("project", "dashboard"),
    ("project", "deploy-log"),
    ("project", "env-vars"),
    ("project", "list"),
    ("project", "pull"),
    ("project", "push"),
    ("project", "status"),
    "version",
    ("version", "-s"),  # don't check PyPI for newer version
    ("version", "-m"),  # Show this message and exit.
)


@pytest.mark.integration
@pytest.mark.parametrize("command", TEST_COMMANDS_CLICK)
def test_call_click_commands(divio_project, command):
    current_dir = os.getcwd()
    os.chdir(os.path.join(current_dir, divio_project))
    runner = CliRunner()
    result = runner.invoke(cli.cli, command)
    os.chdir(current_dir)
    assert result.exit_code == 0
