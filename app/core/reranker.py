from __future__ import annotations

import re

from app.core.vectorstore import SearchHit


class SimpleReranker:
    """Lightweight lexical reranker that complements vector search."""

    def rerank(self, question: str, hits: list[SearchHit], top_n: int) -> list[SearchHit]:
        question_tokens = set(self._tokenize(question))
        scored: list[tuple[float, SearchHit]] = []
        for hit in hits:
            content_tokens = set(self._tokenize(hit.text))
            overlap = len(question_tokens & content_tokens)
            lexical_score = overlap / max(len(question_tokens), 1)
            combined_score = (hit.score * 0.7) + (lexical_score * 0.3)
            scored.append((combined_score, hit))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [hit for _, hit in scored[:top_n]]

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return re.findall(r"[a-z0-9]+", text.lower())
