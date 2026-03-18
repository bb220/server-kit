import pytest
from tests.support.database import run_alembic_upgrade, table_exists, temporary_database


@pytest.mark.anyio
async def test_alembic_upgrade_creates_customers_table():
    async with temporary_database("server_kit_migration") as test_database_url:
        run_alembic_upgrade(test_database_url)
        assert await table_exists(test_database_url, "customers")
