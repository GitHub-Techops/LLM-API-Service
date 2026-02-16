from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import time

app = FastAPI(title="LLM API Service")

class PromptRequest(BaseModel):
    prompt: str
    model: str = "llama3.2:1b"
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
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": request.model,
                    "prompt": request.prompt,
                    "stream": False,
                    "options": {"num_predict": request.max_tokens}
                }
            )
            response.raise_for_status()
            data = response.json()
            
            latency = (time.time() - start_time) * 1000
            
            return PromptResponse(
                response=data["response"],
                model=request.model,
                tokens=data.get("eval_count", 0),
                latency_ms=round(latency, 2)
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy"}