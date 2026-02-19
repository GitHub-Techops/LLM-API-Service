from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import time
import logging

app = FastAPI(title="LLM API Service")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptRequest(BaseModel):
    prompt: str
    model: str = "deepseek-r1:14b"
    max_tokens: int = 500

class PromptResponse(BaseModel):
    response: str
    model: str
    tokens: int
    latency_ms: float

@app.get("/")
async def root():
    return {"message": "LLM API Service", "status": "running"}

@app.post("/generate", response_model=PromptResponse)
async def generate(request: PromptRequest):
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": request.model,
                    "prompt": request.prompt,
                    "stream": False,
                    "options": {"num_predict": request.max_tokens}
                }
            )
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="API server error")
            
            data = response.json()
            latency = (time.time() - start_time) * 1000
            
            return PromptResponse(
                response=data["response"],
                model=request.model,
                tokens=data.get("eval_count", 0),
                latency_ms=round(latency, 2)
            )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise  ���
```

tests\test_api.py
```python
<<<<<<< SEARCH
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
        json={"prompt": "Say hello", "model": "deepseek-r1:14b"}
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
