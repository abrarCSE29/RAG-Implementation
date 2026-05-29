from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and `.env`."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Production RAG"
    app_version: str = "1.0.0"
    environment: str = "development"

    api_key: str = "dev-api-key"
    enable_api_key_auth: bool = True
    api_key_header: str = "X-API-Key"

    enable_ingestion: bool = True
    enable_rag: bool = True
    enable_reranking: bool = True
    enable_citations: bool = True
    enable_streaming: bool = False
    enable_ocr: bool = False
    enable_deduplication: bool = True

    allowed_extensions: list[str] = Field(
        default_factory=lambda: [
            ".txt",
            ".md",
            ".rst",
            ".pdf",
            ".docx",
            ".pptx",
            ".html",
            ".htm",
            ".csv",
            ".json",
            ".xml",
            ".rtf",
            ".png",
            ".jpg",
            ".jpeg",
            ".tif",
            ".tiff",
        ]
    )

    data_dir: Path = Path("data")
    uploads_dir: Path = Path("data/uploads")
    sample_corpus_dir: Path = Path("data/test_corpus")

    qdrant_collection_name: str = "rag_documents"
    qdrant_url: str = "http://qdrant:6333"
    qdrant_api_key: str | None = None
    qdrant_local_path: Path | None = None

    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_model_name: str = "google/flan-t5-base"
    llm_max_new_tokens: int = 256
    llm_temperature: float = 0.1
    llm_top_p: float = 0.95

    chunk_size: int = 900
    chunk_overlap: int = 140
    retrieval_k: int = 5
    rerank_top_n: int = 3

    max_upload_mb: int = 25
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()