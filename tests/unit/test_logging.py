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

    get_logger("server_kit.test").info("app.startup", feature="logging")

    output = capsys.readouterr().out.strip()
    event = json.loads(output)
    assert event["event"] == "app.startup"
    assert event["feature"] == "logging"
    assert event["level"] == "info"
    assert "timestamp" in event
    assert event["logger"] == "server_kit.test"


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
    structlog.contextvars.bind_contextvars(
        request_id="req-123",
        method="GET",
        path="/health",
    )

    get_logger("server_kit.test").info(
        "http.request.completed",
        status_code=200,
        duration_ms=3.5,
    )

    output = capsys.readouterr().out.strip()
    structlog.contextvars.clear_contextvars()
    event = json.loads(output)
    assert event["event"] == "http.request.completed"
    assert event["request_id"] == "req-123"
    assert event["method"] == "GET"
    assert event["path"] == "/health"
    assert event["status_code"] == 200
    assert event["duration_ms"] == 3.5
