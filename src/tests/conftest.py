import pytest

from app import Application


@pytest.fixture
def app():
    return Application()
