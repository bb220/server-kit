import pytest
from pydantic import ValidationError

from server_kit.settings import get_settings


@pytest.fixture(autouse=True)
def reset_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_settings_log_level_defaults_when_unset(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    settings = get_settings()

    assert settings.log_level == "INFO"


def test_settings_reads_log_level_from_env(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    settings = get_settings()

    assert settings.log_level == "DEBUG"


def test_settings_reads_log_level_from_dotenv(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    (tmp_path / ".env").write_text("LOG_LEVEL=INFO\n", encoding="utf-8")

    settings = get_settings()

    assert settings.log_level == "INFO"
