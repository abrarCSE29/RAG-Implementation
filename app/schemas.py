from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(default="ok")
    app_name: str
    environment: str
    features: dict[str, bool]


class MetricsResponse(BaseModel):
    requests_total: int
    queries_total: int
    ingestions_total: int
    last_request_ms: float


class QueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)


class SourceChunk(BaseModel):
    chunk_id: str
    document_id: str
    source_name: str
    score: float
    text: str
    metadata: dict[str, Any]


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    retrieved_count: int
    model_name: str


class DocumentRecord(BaseModel):
    document_id: str
    source_name: str
    source_path: str | None = None
    mime_type: str | None = None
    chunk_count: int
    metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentListResponse(BaseModel):
    count: int
    documents: list[DocumentRecord]


class ChunkRecord(BaseModel):
    chunk_id: str
    document_id: str
    source_name: str
    text: str
    chunk_index: int | None = None
    source_path: str | None = None
    mime_type: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ChunkListResponse(BaseModel):
    count: int
    chunks: list[ChunkRecord]


class IngestionResult(BaseModel):
    files: list[str]
    document_count: int
    chunk_count: int
    status: str = "embedded"
