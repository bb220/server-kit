def test_health_endpoint_returns_200_and_expected_payload(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "message": "ok",
        "data": {"service": "api", "status": "alive"},
    }
