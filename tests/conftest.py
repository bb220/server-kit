import pytest
from fastapi.testclient import TestClient

from server_kit.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
