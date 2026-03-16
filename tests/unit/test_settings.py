import pytest
from pydantic import ValidationError

from server_kit.settings import get_settings


def test_settings_log_level_defaults_when_unset(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("LOG_FORMAT", raising=False)

    settings = get_settings()

    assert settings.log_level == "INFO"
    assert settings.log_format == "dev"


def test_settings_reads_log_level_from_env(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("LOG_FORMAT", "json")

    settings = get_settings()

    assert settings.log_level == "DEBUG"
    assert settings.log_format == "json"


def test_settings_reads_log_level_from_dotenv(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("LOG_FORMAT", raising=False)
    (tmp_path / ".env").write_text(
        "LOG_LEVEL=INFO\nLOG_FORMAT=json\n",
        encoding="utf-8",
    )

    settings = get_settings()

    assert settings.log_level == "INFO"
    assert settings.log_format == "json"


def test_settings_rejects_invalid_log_format(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LOG_FORMAT", "plain")

    with pytest.raises(ValidationError):
        get_settings()
