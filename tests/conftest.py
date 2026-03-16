import pytest
from fastapi.testclient import TestClient

from server_kit.main import create_app
from server_kit.settings import get_settings


@pytest.fixture
def app():
    return create_app()


@pytest.fixture(autouse=True)
def reset_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def client(app) -> TestClient:
    with TestClient(app) as test_client:
        yield test_client
