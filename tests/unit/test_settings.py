import pytest
from pydantic import ValidationError

from server_kit.settings import get_settings


def test_settings_use_defaults_when_env_is_unset(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("LOG_FORMAT", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("DATABASE_POOL_SIZE", raising=False)
    monkeypatch.delenv("DATABASE_MAX_OVERFLOW", raising=False)
    monkeypatch.delenv("DATABASE_POOL_TIMEOUT", raising=False)
    monkeypatch.delenv("DATABASE_POOL_RECYCLE", raising=False)
    monkeypatch.delenv("DATABASE_ECHO", raising=False)

    settings = get_settings()

    assert settings.log_level == "INFO"
    assert settings.log_format == "dev"
    assert (
        settings.database_url
        == "postgresql+asyncpg://postgres:postgres@localhost:5432/server_kit"
    )
    assert settings.database_pool_size == 10
    assert settings.database_max_overflow == 20
    assert settings.database_pool_timeout == 30
    assert settings.database_pool_recycle == 3600
    assert settings.database_echo is False


def test_settings_read_values_from_environment(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("LOG_FORMAT", "json")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+asyncpg://app:secret@db.internal:5432/customers",
    )
    monkeypatch.setenv("DATABASE_POOL_SIZE", "5")
    monkeypatch.setenv("DATABASE_MAX_OVERFLOW", "8")
    monkeypatch.setenv("DATABASE_POOL_TIMEOUT", "15")
    monkeypatch.setenv("DATABASE_POOL_RECYCLE", "1200")
    monkeypatch.setenv("DATABASE_ECHO", "true")

    settings = get_settings()

    assert settings.log_level == "DEBUG"
    assert settings.log_format == "json"
    assert settings.database_url == "postgresql+asyncpg://app:secret@db.internal:5432/customers"
    assert settings.database_pool_size == 5
    assert settings.database_max_overflow == 8
    assert settings.database_pool_timeout == 15
    assert settings.database_pool_recycle == 1200
    assert settings.database_echo is True


def test_settings_read_values_from_dotenv(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("LOG_FORMAT", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("DATABASE_POOL_SIZE", raising=False)
    monkeypatch.delenv("DATABASE_MAX_OVERFLOW", raising=False)
    monkeypatch.delenv("DATABASE_POOL_TIMEOUT", raising=False)
    monkeypatch.delenv("DATABASE_POOL_RECYCLE", raising=False)
    monkeypatch.delenv("DATABASE_ECHO", raising=False)
    (tmp_path / ".env").write_text(
        (
            "LOG_LEVEL=INFO\n"
            "LOG_FORMAT=json\n"
            "DATABASE_URL=postgresql+asyncpg://dotenv:dotenv@localhost:5432/dotenv_db\n"
            "DATABASE_POOL_SIZE=12\n"
            "DATABASE_MAX_OVERFLOW=4\n"
            "DATABASE_POOL_TIMEOUT=45\n"
            "DATABASE_POOL_RECYCLE=1800\n"
            "DATABASE_ECHO=true\n"
        ),
        encoding="utf-8",
    )

    settings = get_settings()

    assert settings.log_level == "INFO"
    assert settings.log_format == "json"
    assert settings.database_url == "postgresql+asyncpg://dotenv:dotenv@localhost:5432/dotenv_db"
    assert settings.database_pool_size == 12
    assert settings.database_max_overflow == 4
    assert settings.database_pool_timeout == 45
    assert settings.database_pool_recycle == 1800
    assert settings.database_echo is True


def test_settings_rejects_invalid_log_format(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LOG_FORMAT", "plain")

    with pytest.raises(ValidationError):
        get_settings()
