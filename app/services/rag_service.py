from __future__ import annotations

from pathlib import Path
from typing import Any

from app.config.settings import Settings, get_settings
from app.core.document_loader import DocumentIngestor
from app.core.embeddings import HuggingFaceEmbedder
from app.core.llm import LocalHuggingFaceLLM
from app.core.reranker import SimpleReranker
from app.core.vectorstore import QdrantVectorStore, SearchHit


class RAGService:
    """Production-oriented orchestration for ingestion, retrieval, and generation."""

    def __init__(
        self,
        settings: Settings | None = None,
        ingestor: DocumentIngestor | None = None,
        embedder: HuggingFaceEmbedder | None = None,
        llm: LocalHuggingFaceLLM | None = None,
        vector_store: QdrantVectorStore | None = None,
        reranker: SimpleReranker | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.ingestor = ingestor or DocumentIngestor(self.settings)
        self.embedder = embedder or HuggingFaceEmbedder(self.settings)
        self.llm = llm or LocalHuggingFaceLLM(self.settings)
        self.vector_store = vector_store or QdrantVectorStore(self.settings)
        self.reranker = reranker or SimpleReranker()

    def ingest_paths(self, paths: list[Path | str]) -> dict[str, Any]:
        if not self.settings.enable_ingestion:
            raise ValueError("Document ingestion is disabled in configuration")

        documents = self.ingestor.load_files([Path(path) for path in paths])
        chunks = self.ingestor.chunk_documents(documents)
        if not chunks:
            return {"files": [Path(path).name for path in paths], "document_count": 0, "chunk_count": 0}

        embeddings = self.embedder.embed_documents([chunk.text for chunk in chunks])
        self.vector_store.ensure_collection(self.embedder.dimension)
        self.vector_store.upsert_chunks(chunks, embeddings)

        return {
            "files": [Path(path).name for path in paths],
            "document_count": len(documents),
            "chunk_count": len(chunks),
        }

    def query(self, question: str) -> dict[str, Any]:
        if not self.settings.enable_rag:
            return {"answer": "RAG is disabled in configuration.", "sources": [], "retrieved_count": 0, "model_name": self.settings.llm_model_name}

        question_vector = self.embedder.embed_query(question)
        hits = self.vector_store.search(question_vector, limit=self.settings.retrieval_k)
        if self.settings.enable_reranking and hits:
            hits = self.reranker.rerank(question, hits, self.settings.rerank_top_n)

        if not hits:
            return {
                "answer": "I could not find relevant context in the indexed documents.",
                "sources": [],
                "retrieved_count": 0,
                "model_name": self.settings.llm_model_name,
            }

        prompt = self._build_prompt(question, hits)
        answer = self.llm.generate(prompt)
        if self.settings.enable_citations:
            answer = self._append_citations(answer, hits)

        return {
            "answer": answer,
            "sources": [self._hit_to_source(hit) for hit in hits],
            "retrieved_count": len(hits),
            "model_name": self.settings.llm_model_name,
        }

    def list_documents(self) -> list[dict[str, Any]]:
        return self.vector_store.list_documents()

    def list_chunks(self, document_id: str | None = None) -> list[dict[str, Any]]:
        return self.vector_store.list_chunks(document_id=document_id)

    def _build_prompt(self, question: str, hits: list[SearchHit]) -> str:
        context_lines = []
        for index, hit in enumerate(hits, start=1):
            context_lines.append(
                f"[{index}] Source: {hit.source_name} | Chunk: {hit.chunk_id}\n{hit.text.strip()}"
            )

        context = "\n\n".join(context_lines)
        return (
            "You are a concise assistant for a document intelligence system. "
            "Answer only from the provided context. If the context is insufficient, say that clearly. "
            "Prefer bullet points if they improve readability.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n"
            "Answer:"
        )

    def _append_citations(self, answer: str, hits: list[SearchHit]) -> str:
        citations = ", ".join(sorted({hit.source_name for hit in hits}))
        if citations:
            return f"{answer}\n\nSources: {citations}"
        return answer

    @staticmethod
    def _hit_to_source(hit: SearchHit) -> dict[str, Any]:
        return {
            "chunk_id": hit.chunk_id,
            "document_id": hit.document_id,
            "source_name": hit.source_name,
            "score": hit.score,
            "text": hit.text,
            "metadata": hit.metadata,
        }