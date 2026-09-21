# RAG Knowledge Base API

Production-style Retrieval-Augmented Generation (RAG) backend built with FastAPI, PostgreSQL + pgvector and OpenAI-compatible LLM APIs.

## Features

- REST API with FastAPI
- document ingestion and chunking
- vector embeddings stored in PostgreSQL/pgvector
- semantic similarity search
- RAG answers grounded in retrieved context
- source references returned with every answer
- async SQLAlchemy
- Docker Compose
- health checks
- pytest tests
- configurable embedding/chat models

## Architecture

```
Client -> FastAPI -> RAG service -> PostgreSQL + pgvector
                         |
                         +-> Embeddings API
                         +-> Chat/LLM API
```

Documents are split into chunks. Each chunk receives an embedding and is stored in pgvector. A question is embedded, the nearest chunks are retrieved with cosine distance, and only that context is sent to the LLM.

## API

- `GET /health`
- `POST /api/v1/documents` — ingest text
- `POST /api/v1/search` — semantic search
- `POST /api/v1/ask` — RAG answer with sources

Interactive documentation: `/docs`.

## Quick start

1. Copy environment variables:

```bash
cp .env.example .env
```

2. Add your API key to `.env`.

3. Start:

```bash
docker compose up --build
```

4. Open `http://localhost:8000/docs`.

## Example

```bash
curl -X POST http://localhost:8000/api/v1/documents \
  -H "Content-Type: application/json" \
  -d '{"title":"FastAPI notes","content":"FastAPI is a modern Python framework for building APIs."}'
```

```bash
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is FastAPI?"}'
```

## Tests

```bash
pytest
```

## Tech stack

Python 3.12, FastAPI, Pydantic, SQLAlchemy, PostgreSQL, pgvector, httpx, Docker, pytest.
