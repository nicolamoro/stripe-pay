import pytest
from app import make_app


@pytest.fixture
def app():
    return make_app()
