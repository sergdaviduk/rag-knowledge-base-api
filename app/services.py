from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.llm import llm
from app.models import Chunk, Document
from app.schemas import SearchResult


def split_text(text: str, chunk_size: int = 900, overlap: int = 120) -> list[str]:
    text = " ".join(text.split())
    if not text:
        return []
    chunks, start = [], 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks


async def ingest(session: AsyncSession, title: str, content: str) -> tuple[Document, int]:
    parts = split_text(content)
    vectors = await llm.embed(parts)
    document = Document(title=title, content=content)
    session.add(document)
    await session.flush()
    session.add_all([
        Chunk(document_id=document.id, position=i, content=part, embedding=vector)
        for i, (part, vector) in enumerate(zip(parts, vectors))
    ])
    await session.commit()
    return document, len(parts)


async def search(session: AsyncSession, query: str, limit: int) -> list[SearchResult]:
    vector = (await llm.embed([query]))[0]
    distance = Chunk.embedding.cosine_distance(vector)
    stmt = (
        select(Chunk, Document.title, distance.label("distance"))
        .join(Document, Document.id == Chunk.document_id)
        .order_by(distance)
        .limit(limit)
    )
    rows = (await session.execute(stmt)).all()
    return [
        SearchResult(
            document_id=chunk.document_id,
            title=title,
            content=chunk.content,
            score=max(0.0, 1.0 - float(dist)),
        )
        for chunk, title, dist in rows
    ]
