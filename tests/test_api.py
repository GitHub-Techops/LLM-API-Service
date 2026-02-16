import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_generate():
    response = client.post(
        "/generate",
        json={"prompt": "Say hello", "model": "llama3.2:1b"}
    )
    assert response.status_code == 200
    assert "response" in response.json()
    assert "latency_ms" in response.json()
