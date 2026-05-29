from __future__ import annotations

from functools import lru_cache

from app.config.settings import Settings, get_settings


class HuggingFaceEmbedder:
    """CPU-friendly sentence embedding wrapper with lazy model loading."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._model = None

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.settings.embedding_model_name, device="cpu")
        return self._model

    @property
    def dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        vectors = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False)
        return vectors.tolist()

    def embed_query(self, text: str) -> list[float]:
        vector = self.model.encode([text], convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False)[0]
        return vector.tolist()


@lru_cache(maxsize=1)
def get_embedder() -> HuggingFaceEmbedder:
    return HuggingFaceEmbedder()