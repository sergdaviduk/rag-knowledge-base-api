from uuid import UUID
from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)


class DocumentCreated(BaseModel):
    id: UUID
    chunks: int


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=20)


class SearchResult(BaseModel):
    document_id: UUID
    title: str
    content: str
    score: float


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=20)


class AskResponse(BaseModel):
    answer: str
    sources: list[SearchResult]
