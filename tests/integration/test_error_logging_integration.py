import json

from fastapi import APIRouter
from fastapi.testclient import TestClient

from server_kit.main import create_app


def test_unhandled_exceptions_are_logged_with_request_context(monkeypatch, capsys):
    monkeypatch.setenv("LOG_FORMAT", "json")
    app = create_app()
    router = APIRouter()

    @router.get("/boom")
    async def boom():
        raise RuntimeError("boom")

    app.include_router(router)

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/boom", headers={"X-Request-ID": "req-123"})

    output_lines = [
        line for line in capsys.readouterr().out.splitlines() if line.strip()
    ]
    events = [json.loads(line) for line in output_lines]
    error_event = next(
        event for event in events if event["event"] == "unhandled_exception"
    )

    assert response.status_code == 500
    assert error_event["event"] == "unhandled_exception"
    assert error_event["level"] == "error"
    assert error_event["request_id"] == "req-123"
    assert error_event["method"] == "GET"
    assert error_event["path"] == "/boom"
    assert "RuntimeError: boom" in error_event["exception"]
