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
            raise  # Re-raise the HTTPException without modification

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/status")
async def server_status():
    return {"status": "running"}
