from uuid import UUID


def test_request_id_is_generated_and_returned(client):
    response = client.get("/health")

    assert response.status_code == 200
    request_id = response.headers["X-Request-ID"]
    assert UUID(request_id)


def test_request_id_from_header_is_preserved(client):
    response = client.get("/health", headers={"X-Request-ID": "req-123"})

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "req-123"
