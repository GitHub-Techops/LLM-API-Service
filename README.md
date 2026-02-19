# LLM API Service

FastAPI wrapper for Ollama LLMs.

## Setup
```bash
pip install -r requirements.txt
ollama pull deepseek-r1:14b
```

## Run
```bash
uvicorn app.main:app --reload
```

## Docker
```bash
docker-compose up
```

## Test
```bash
pytest tests/ -v
```

## API Docs
http://localhost:8000/docs
