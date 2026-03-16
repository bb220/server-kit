import json

from fastapi.testclient import TestClient

from server_kit.main import create_app


def test_successful_requests_emit_completion_log(monkeypatch, capsys):
    monkeypatch.setenv("LOG_FORMAT", "json")
    app = create_app()

    with TestClient(app) as client:
        response = client.get("/health", headers={"X-Request-ID": "req-123"})

    output_lines = [
        line for line in capsys.readouterr().out.splitlines() if line.strip()
    ]
    events = [json.loads(line) for line in output_lines]
    completion_event = next(
        event for event in events if event["event"] == "http.request.completed"
    )

    assert response.status_code == 200
    assert completion_event["event"] == "http.request.completed"
    assert completion_event["level"] == "info"
    assert completion_event["request_id"] == "req-123"
    assert completion_event["method"] == "GET"
    assert completion_event["path"] == "/health"
    assert completion_event["status_code"] == 200
    assert isinstance(completion_event["duration_ms"], float)
    assert completion_event["duration_ms"] >= 0
