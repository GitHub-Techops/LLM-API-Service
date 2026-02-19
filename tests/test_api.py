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
    assert response.status = 200

def test_generate():
    response = client.post(
        "/generate",
        json={"prompt": "Say hello", "model": "deepseek-r1:8b"}
    )
    assert response.status_code == 200
    assert "response" in response.json()
    assert "latency_ms" in response.json()
    response_text = response.json()["response"]
    assert "hello" in response_text.lower()

def test_generate_invalid_model():
    response = client.post(
        "/generate",
        json={"prompt": "Say hello", "model": "invalid-model"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "API server error"

def test_server_status():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "running"}
