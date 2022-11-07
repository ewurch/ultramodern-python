import pytest
import requests
from typer.testing import CliRunner

from ultramodern_python.main import app


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker):
    return mocker.patch("ultramodern_python.wikipedia.random_page")


def test_main(runner, mock_requests_get):
    result = runner.invoke(app, ["fact"])
    assert result.exit_code == 0
    assert "title-test" in result.stdout
    assert "extract-test" in result.stdout


def test_main_invokes_requests_get(runner, mock_requests_get):
    runner.invoke(app, ["fact"])
    mock_requests_get.assert_called()


def test_main_uses_en_wikipedia_org(runner, mock_requests_get):
    runner.invoke(app, ["fact"])
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(app, ["fact"])
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = requests.exceptions.Timeout()
    result = runner.invoke(app, ["fact"])
    assert result.exit_code == 1
    assert "Error" in result.stdout


def test_main_uses_specified_language(runner, mock_wikipedia_random_page):
    runner.invoke(app, ["fact", "--language", "es"])
    mock_wikipedia_random_page.assert_called_with(language="es")


@pytest.mark.e2e
def test_main_scceeds_in_production_env(runner):
    result = runner.invoke(app, ["fact"])
    assert result.exit_code == 0
