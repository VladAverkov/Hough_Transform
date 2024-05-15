"""Testing the console module."""

from click import testing
import pytest
from src.hough_transform_project import console


@pytest.fixture
def runner() -> testing.CliRunner:
    """Fixture for creating a Click CLI runner."""
    return testing.CliRunner()


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner):
    """e2e testing."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_succeeds(runner: testing.CliRunner) -> None:
    """Test that the main function exits with a status code of zero."""
    result: testing.Result = runner.invoke(console.main)
    assert result.exit_code == 0
