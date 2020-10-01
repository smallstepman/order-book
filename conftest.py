import pytest

from src import app as _app


@pytest.fixture
def app():
    return _app
