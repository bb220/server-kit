import json
import logging

import structlog

from server_kit.logging import configure_logging, get_logger
from server_kit.settings import Settings


def test_configure_logging_uses_console_renderer_for_dev(capsys):
    configure_logging(Settings(log_format="dev", log_level="INFO"))

    get_logger("server_kit.test").info("dev_log", feature="logging")

    output = capsys.readouterr().out
    assert "dev_log" in output
    assert "feature" in output
    assert "logging" in output


def test_configure_logging_uses_json_renderer_for_json(capsys):
    configure_logging(Settings(log_format="json", log_level="INFO"))

    get_logger("server_kit.test").info("json_log", feature="logging")

    output = capsys.readouterr().out.strip()
    event = json.loads(output)
    assert event["event"] == "json_log"
    assert event["feature"] == "logging"
    assert event["level"] == "info"


def test_stdlib_logger_uses_structlog_formatter(capsys):
    configure_logging(Settings(log_format="json", log_level="INFO"))

    logging.getLogger("uvicorn.error").info("uvicorn_log")

    output = capsys.readouterr().out.strip()
    event = json.loads(output)
    assert event["event"] == "uvicorn_log"
    assert event["logger"] == "uvicorn.error"
    assert event["level"] == "info"


def test_request_contextvars_are_merged_into_logs(capsys):
    configure_logging(Settings(log_format="json", log_level="INFO"))
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id="req-123")

    get_logger("server_kit.test").info("bound_log")

    output = capsys.readouterr().out.strip()
    structlog.contextvars.clear_contextvars()
    event = json.loads(output)
    assert event["event"] == "bound_log"
    assert event["request_id"] == "req-123"
