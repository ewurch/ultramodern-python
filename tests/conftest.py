import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "e2e: mark test as an end-to-end test.")


@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.json.return_value = {
        "title": "title-test",
        "extract": "extract-test",
    }
    return mock
