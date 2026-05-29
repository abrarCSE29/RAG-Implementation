from dataclasses import dataclass

from app.config.settings import Settings
from app.core.vectorstore import SearchHit
from app.services.rag_service import RAGService


@dataclass
class FakeEmbedder:
    dimension: int = 3

    def embed_documents(self, texts):
        return [[1.0, 0.0, 0.0] for _ in texts]

    def embed_query(self, text):
        return [1.0, 0.0, 0.0]


class FakeLLM:
    def generate(self, prompt: str) -> str:
        return "The answer comes from the indexed documents."


class FakeVectorStore:
    def __init__(self):
        self.points = []

    def ensure_collection(self, vector_size):
        self.vector_size = vector_size

    def upsert_chunks(self, chunks, embeddings):
        self.points = list(zip(chunks, embeddings, strict=True))

    def search(self, query_vector, limit):
        return [
            SearchHit(
                chunk_id="doc-1:0",
                document_id="doc-1",
                source_name="handbook.txt",
                score=0.91,
                text="The handbook explains the release checklist.",
                metadata={"page": 1},
            )
        ]

    def list_documents(self):
        return [
            {
                "document_id": "doc-1",
                "source_name": "handbook.txt",
                "source_path": "/tmp/handbook.txt",
                "mime_type": "text/plain",
                "chunk_count": 1,
                "metadata": {},
            }
        ]


def test_query_returns_citations_and_sources() -> None:
    settings = Settings(enable_reranking=False, enable_citations=True, api_key="test-key")
    service = RAGService(
        settings=settings,
        embedder=FakeEmbedder(),
        llm=FakeLLM(),
        vector_store=FakeVectorStore(),
    )

    result = service.query("What does the handbook explain?")

    assert result["retrieved_count"] == 1
    assert "Sources: handbook.txt" in result["answer"]
    assert result["sources"][0]["source_name"] == "handbook.txt"
