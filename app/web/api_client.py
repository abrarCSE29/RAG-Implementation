from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


@dataclass(slots=True)
class APIClient:
    base_url: str
    api_key: str | None = None
    timeout: float = 120.0

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers

    def health(self) -> dict[str, Any]:
        response = requests.get(f"{self.base_url}/api/health", timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def documents(self) -> dict[str, Any]:
        response = requests.get(f"{self.base_url}/api/documents", headers=self._headers(), timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def chunks(self, document_id: str | None = None) -> dict[str, Any]:
        params = {"document_id": document_id} if document_id else None
        response = requests.get(
            f"{self.base_url}/api/documents/chunks",
            headers=self._headers(),
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def metrics(self) -> dict[str, Any]:
        response = requests.get(f"{self.base_url}/api/metrics", headers=self._headers(), timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def query(self, question: str) -> dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/api/query",
            json={"question": question},
            headers=self._headers(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def upload(self, files: list[Any]) -> dict[str, Any]:
        request_files = [("files", file) for file in files]
        response = requests.post(
            f"{self.base_url}/api/documents/upload",
            files=request_files,
            headers={"X-API-Key": self.api_key} if self.api_key else {},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
