import asyncio
import os
import subprocess
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from server_kit.settings import get_settings

REPO_ROOT = Path(__file__).resolve().parents[2]


def get_base_database_url() -> str:
    return os.environ.get("DATABASE_URL", get_settings().database_url)


def build_database_url(base_database_url: str, database_name: str) -> str:
    return base_database_url.rsplit("/", maxsplit=1)[0] + f"/{database_name}"


@asynccontextmanager
async def temporary_database(prefix: str) -> AsyncIterator[str]:
    base_database_url = get_base_database_url()
    database_name = f"{prefix}_{uuid4().hex}"
    admin_database_url = build_database_url(base_database_url, "postgres")
    database_url = build_database_url(base_database_url, database_name)
    admin_engine = create_async_engine(admin_database_url, isolation_level="AUTOCOMMIT")

    try:
        async with admin_engine.connect() as connection:
            await connection.execute(text(f'CREATE DATABASE "{database_name}"'))

        yield database_url
    finally:
        async with admin_engine.connect() as connection:
            await connection.execute(
                text(
                    "SELECT pg_terminate_backend(pid) "
                    "FROM pg_stat_activity "
                    "WHERE datname = :database_name AND pid <> pg_backend_pid()"
                ),
                {"database_name": database_name},
            )
            await connection.execute(text(f'DROP DATABASE IF EXISTS "{database_name}"'))

        await admin_engine.dispose()


def run_alembic_upgrade(database_url: str) -> None:
    env = os.environ.copy()
    env["DATABASE_URL"] = database_url
    subprocess.run(
        [sys.executable, "-m", "alembic", "-c", "alembic.ini", "upgrade", "head"],
        check=True,
        cwd=REPO_ROOT,
        env=env,
    )


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


def create_test_engine(database_url: str) -> AsyncEngine:
    return create_async_engine(database_url)


async def _create_database(admin_database_url: str, database_name: str) -> None:
    admin_engine = create_async_engine(admin_database_url, isolation_level="AUTOCOMMIT")
    try:
        async with admin_engine.connect() as connection:
            await connection.execute(text(f'CREATE DATABASE "{database_name}"'))
    finally:
        await admin_engine.dispose()


async def _drop_database(admin_database_url: str, database_name: str) -> None:
    admin_engine = create_async_engine(admin_database_url, isolation_level="AUTOCOMMIT")
    try:
        async with admin_engine.connect() as connection:
            await connection.execute(
                text(
                    "SELECT pg_terminate_backend(pid) "
                    "FROM pg_stat_activity "
                    "WHERE datname = :database_name AND pid <> pg_backend_pid()"
                ),
                {"database_name": database_name},
            )
            await connection.execute(text(f'DROP DATABASE IF EXISTS "{database_name}"'))
    finally:
        await admin_engine.dispose()


@contextmanager
def temporary_database_sync(prefix: str):
    base_database_url = get_base_database_url()
    database_name = f"{prefix}_{uuid4().hex}"
    admin_database_url = build_database_url(base_database_url, "postgres")
    database_url = build_database_url(base_database_url, database_name)

    asyncio.run(_create_database(admin_database_url, database_name))
    try:
        yield database_url
    finally:
        asyncio.run(_drop_database(admin_database_url, database_name))
