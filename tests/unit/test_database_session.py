from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from server_kit.main import create_app


def test_app_lifespan_initializes_database_resources():
    app = create_app()

    with TestClient(app):
        assert isinstance(app.state.db_engine, AsyncEngine)
        assert isinstance(app.state.session_factory, async_sessionmaker)
        assert app.state.session_factory.class_ is AsyncSession


def test_app_lifespan_disposes_database_engine(monkeypatch):
    app = create_app()
    disposed_engine = None

    async def fake_dispose_database_engine(engine):
        nonlocal disposed_engine
        disposed_engine = engine

    monkeypatch.setattr(
        "server_kit.main.dispose_database_engine", fake_dispose_database_engine
    )

    with TestClient(app):
        engine = app.state.db_engine

    assert disposed_engine is engine
