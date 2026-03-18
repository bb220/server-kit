import os
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from server_kit.settings import get_settings

REPO_ROOT = Path(__file__).resolve().parents[2]


async def table_exists(database_url: str, table_name: str) -> bool:
    engine = create_async_engine(database_url)
    try:
        async with engine.connect() as connection:
            result = await connection.execute(
                text("select to_regclass(:table_name)"),
                {"table_name": table_name},
            )
            return result.scalar_one() == table_name
    finally:
        await engine.dispose()


@pytest.mark.anyio
async def test_alembic_upgrade_creates_customers_table():
    base_database_url = os.environ.get("DATABASE_URL", get_settings().database_url)
    test_database_name = f"server_kit_migration_{uuid4().hex}"
    admin_database_url = base_database_url.rsplit("/", maxsplit=1)[0] + "/postgres"
    test_database_url = base_database_url.rsplit("/", maxsplit=1)[0] + f"/{test_database_name}"

    admin_engine = create_async_engine(admin_database_url, isolation_level="AUTOCOMMIT")

    try:
        async with admin_engine.connect() as connection:
            await connection.execute(text(f'CREATE DATABASE "{test_database_name}"'))

        env = os.environ.copy()
        env["DATABASE_URL"] = test_database_url

        subprocess.run(
            [sys.executable, "-m", "alembic", "-c", "alembic.ini", "upgrade", "head"],
            check=True,
            cwd=REPO_ROOT,
            env=env,
        )

        assert await table_exists(test_database_url, "customers")
    finally:
        async with admin_engine.connect() as connection:
            await connection.execute(
                text(
                    "SELECT pg_terminate_backend(pid) "
                    "FROM pg_stat_activity "
                    "WHERE datname = :database_name AND pid <> pg_backend_pid()"
                ),
                {"database_name": test_database_name},
            )
            await connection.execute(text(f'DROP DATABASE IF EXISTS "{test_database_name}"'))

        await admin_engine.dispose()
