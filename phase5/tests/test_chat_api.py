from fastapi.testclient import TestClient
from phase5.backend.main import app, startup_event
import pytest

startup_event()
client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_funds():
    response = client.get("/api/funds")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_suggestions():
    response = client.get("/api/suggestions")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_chat():
    response = client.post("/api/chat", json={"query": "What is the expense ratio?"})
    assert response.status_code == 200
    assert "response" in response.json()
