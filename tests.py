import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "Server is running"}


def test_process_query_invalid_data():
    data = {
        "cadastre_number": "12345",
        "latitude": "invalid",
        "longitude": -74.0060
    }
    response = client.post("/query", json=data)
    assert response.status_code == 422
    assert "detail" in response.json()


def test_update_query_result_invalid_data():
    data = {
        "request_id": "invalid",
        "result": True
    }
    response = client.put("/result", json=data)
    assert response.status_code == 422
    assert "detail" in response.json()


def test_get_query_history():
    response = client.get("/history")
    assert response.status_code == 200
    assert "history" in response.json()


def test_get_query_history_with_cadastre_number():
    response = client.get("/history?cadastre_number=12345")
    assert response.status_code == 200
    assert "history" in response.json()
