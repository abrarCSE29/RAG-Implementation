from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http import models

from app.config.settings import Settings, get_settings
from app.core.document_loader import DocumentChunk


@dataclass(slots=True)
class SearchHit:
    chunk_id: str
    document_id: str
    source_name: str
    score: float
    text: str
    metadata: dict[str, Any]


class QdrantVectorStore:
    """Qdrant-backed persistence and semantic search layer."""

    def __init__(self, settings: Settings | None = None, client: QdrantClient | None = None) -> None:
        self.settings = settings or get_settings()
        self.client = client or self._create_client()

    def _create_client(self) -> QdrantClient:
        if self.settings.qdrant_local_path:
            return QdrantClient(path=str(self.settings.qdrant_local_path))
        return QdrantClient(url=self.settings.qdrant_url, api_key=self.settings.qdrant_api_key)

    def ensure_collection(self, vector_size: int) -> None:
        if self.client.collection_exists(self.settings.qdrant_collection_name):
            return
        self.client.create_collection(
            collection_name=self.settings.qdrant_collection_name,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
        )

    def upsert_chunks(self, chunks: list[DocumentChunk], embeddings: list[list[float]]) -> None:
        points: list[models.PointStruct] = []
        for chunk, vector in zip(chunks, embeddings, strict=True):
            payload = {
                "chunk_id": chunk.chunk_id,
                "document_id": chunk.document_id,
                "source_name": chunk.source_name,
                "text": chunk.text,
                **chunk.metadata,
            }
            points.append(models.PointStruct(id=chunk.chunk_id, vector=vector, payload=payload))

        self.client.upsert(collection_name=self.settings.qdrant_collection_name, points=points)

    def search(self, query_vector: list[float], limit: int) -> list[SearchHit]:
        if hasattr(self.client, "search"):
            results = self.client.search(
                collection_name=self.settings.qdrant_collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=True,
            )
        else:
            response = self.client.query_points(
                collection_name=self.settings.qdrant_collection_name,
                query=query_vector,
                limit=limit,
                with_payload=True,
            )
            results = getattr(response, "points", response)

        hits: list[SearchHit] = []
        for result in results:
            payload = result.payload or {}
            hits.append(
                SearchHit(
                    chunk_id=str(result.id),
                    document_id=str(payload.get("document_id", "")),
                    source_name=str(payload.get("source_name", "")),
                    score=float(result.score or 0.0),
                    text=str(payload.get("text", "")),
                    metadata={k: v for k, v in payload.items() if k != "text"},
                )
            )
        return hits

    def list_documents(self) -> list[dict[str, Any]]:
        if not self.client.collection_exists(self.settings.qdrant_collection_name):
            return []

        documents: dict[str, dict[str, Any]] = {}
        offset = None
        while True:
            points, offset = self.client.scroll(
                collection_name=self.settings.qdrant_collection_name,
                limit=100,
                offset=offset,
                with_payload=True,
            )
            for point in points:
                payload = point.payload or {}
                document_id = str(payload.get("document_id", point.id))
                if document_id not in documents:
                    documents[document_id] = {
                        "document_id": document_id,
                        "source_name": str(payload.get("source_name", "")),
                        "source_path": payload.get("source_path"),
                        "mime_type": payload.get("mime_type"),
                        "metadata": {k: v for k, v in payload.items() if k not in {"text", "source_name", "source_path", "mime_type"}},
                        "chunk_count": 1,
                    }
                else:
                    documents[document_id]["chunk_count"] += 1

            if offset is None:
                break
        return list(documents.values())

    def list_chunks(self, document_id: str | None = None) -> list[dict[str, Any]]:
        if not self.client.collection_exists(self.settings.qdrant_collection_name):
            return []

        chunks: list[dict[str, Any]] = []
        offset = None
        while True:
            points, offset = self.client.scroll(
                collection_name=self.settings.qdrant_collection_name,
                limit=100,
                offset=offset,
                with_payload=True,
            )
            for point in points:
                payload = point.payload or {}
                current_document_id = str(payload.get("document_id", point.id))
                if document_id and current_document_id != document_id:
                    continue

                chunks.append(
                    {
                        "chunk_id": str(payload.get("chunk_id", point.id)),
                        "document_id": current_document_id,
                        "source_name": str(payload.get("source_name", "")),
                        "text": str(payload.get("text", "")),
                        "chunk_index": payload.get("chunk_index"),
                        "source_path": payload.get("source_path"),
                        "mime_type": payload.get("mime_type"),
                        "metadata": {
                            k: v
                            for k, v in payload.items()
                            if k not in {"text", "source_name", "source_path", "mime_type", "chunk_id", "document_id", "chunk_index"}
                        },
                    }
                )

            if offset is None:
                break
        return chunks
