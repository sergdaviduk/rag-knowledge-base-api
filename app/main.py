from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, get_session
from app.models import Base
from app.schemas import AskRequest, AskResponse, DocumentCreate, DocumentCreated, SearchRequest, SearchResult
from app.services import ingest, search
from app.llm import llm


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="RAG Knowledge Base API",
    version="1.0.0",
    description="Production-style semantic search and RAG backend.",
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/v1/documents", response_model=DocumentCreated, status_code=201)
async def create_document(payload: DocumentCreate, session: AsyncSession = Depends(get_session)):
    document, count = await ingest(session, payload.title, payload.content)
    return DocumentCreated(id=document.id, chunks=count)


@app.post("/api/v1/search", response_model=list[SearchResult])
async def semantic_search(payload: SearchRequest, session: AsyncSession = Depends(get_session)):
    return await search(session, payload.query, payload.limit)


@app.post("/api/v1/ask", response_model=AskResponse)
async def ask(payload: AskRequest, session: AsyncSession = Depends(get_session)):
    sources = await search(session, payload.question, payload.limit)
    context = "\n\n".join(f"[{i + 1}] {item.content}" for i, item in enumerate(sources))
    answer = await llm.answer(payload.question, context)
    return AskResponse(answer=answer, sources=sources)
