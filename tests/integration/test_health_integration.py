from fastapi.testclient import TestClient

from server_kit.main import create_app
from server_kit.settings import get_settings
from tests.support.database import temporary_database_sync


def test_health_endpoint_returns_200_and_expected_payload(monkeypatch):
    with temporary_database_sync("server_kit_health") as database_url:
        monkeypatch.setenv("DATABASE_URL", database_url)
        get_settings.cache_clear()
        app = create_app()

        with TestClient(app) as client:
            response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["X-Request-ID"]
    assert response.json() == {
        "message": "ok",
        "data": {"service": "api", "status": "alive", "database": "ready"},
    }


def test_health_endpoint_returns_503_when_database_is_unavailable(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/server_kit_missing",
    )
    get_settings.cache_clear()
    app = create_app()

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 503
    assert response.json() == {
        "message": "degraded",
        "data": {"service": "api", "status": "alive", "database": "unavailable"},
    }
