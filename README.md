# LLM API Service

FastAPI wrapper for Ollama LLMs.

## Setup
```bash
pip install -r requirements.txt
ollama pull qwen2.5-coder:14b
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

## Model Comparison

I have tested three models—`llama3.2:1b`, `deepseek-r1:14b`, and `qwen2.5-coder:14b`. After evaluating their performance, I found that `qwen2.5-coder:14b` is significantly faster and more effective for solving coding problems on my current system configuration (32GB RAM, RTX4070 Super 12GB GPU, i7-1200F CPU).

**Key Features of qwen2.5-coder:14b:**
- **Speed:** Optimized for faster processing times 🚀
- **Effectiveness:** Better performance in solving coding problems 💡
- **Scalability:** Efficient use of system resources 🛠️

These findings have led me to update the default model in my FastAPI application to `qwen2.5-coder:14b`.

## Contributing

Contributions are welcome! Please feel free to open issues or pull requests.

## License

This project is licensed under the MIT License.
