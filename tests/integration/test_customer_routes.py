from uuid import UUID

from fastapi.testclient import TestClient

from server_kit.main import create_app
from server_kit.settings import get_settings
from tests.support.database import run_alembic_upgrade, temporary_database_sync


def test_customer_crud_endpoints(monkeypatch):
    with temporary_database_sync("server_kit_customer_routes") as database_url:
        run_alembic_upgrade(database_url)
        monkeypatch.setenv("DATABASE_URL", database_url)
        get_settings.cache_clear()
        app = create_app()

        with TestClient(app) as client:
            create_response = client.post(
                "/api/v1/customers",
                json={"name": "Jane Doe", "city": "Boston", "state": "MA"},
            )

            assert create_response.status_code == 201
            created_customer = create_response.json()
            customer_id = created_customer["id"]
            assert create_response.headers["Location"] == f"/api/v1/customers/{customer_id}"

            get_response = client.get(f"/api/v1/customers/{customer_id}")
            assert get_response.status_code == 200
            assert get_response.json()["name"] == "Jane Doe"

            list_response = client.get("/api/v1/customers?limit=10&offset=0")
            assert list_response.status_code == 200
            assert len(list_response.json()["data"]) == 1
            assert list_response.json()["data"][0]["id"] == customer_id

            patch_response = client.patch(
                f"/api/v1/customers/{customer_id}",
                json={"city": "Providence"},
            )
            assert patch_response.status_code == 200
            assert patch_response.json()["city"] == "Providence"
            assert patch_response.json()["state"] == "MA"

            delete_response = client.delete(f"/api/v1/customers/{customer_id}")
            assert delete_response.status_code == 204

            missing_response = client.get(f"/api/v1/customers/{customer_id}")
            assert missing_response.status_code == 404


def test_customer_routes_return_404_for_missing_customer(monkeypatch):
    with temporary_database_sync("server_kit_customer_missing") as database_url:
        run_alembic_upgrade(database_url)
        monkeypatch.setenv("DATABASE_URL", database_url)
        get_settings.cache_clear()
        app = create_app()
        missing_customer_id = UUID("00000000-0000-0000-0000-000000000001")

        with TestClient(app) as client:
            get_response = client.get(f"/api/v1/customers/{missing_customer_id}")
            patch_response = client.patch(
                f"/api/v1/customers/{missing_customer_id}",
                json={"city": "Providence"},
            )
            delete_response = client.delete(f"/api/v1/customers/{missing_customer_id}")

            assert get_response.status_code == 404
            assert patch_response.status_code == 404
            assert delete_response.status_code == 404
