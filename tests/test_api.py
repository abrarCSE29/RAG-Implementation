from pathlib import Path

from fastapi.testclient import TestClient

from app.config.settings import Settings
from app.main import create_app


class FakeService:
    def __init__(self):
        self.ingested = []

    def ingest_paths(self, paths):
        self.ingested = [Path(path) for path in paths]
        return {"files": [path.name for path in self.ingested], "document_count": len(self.ingested), "chunk_count": len(self.ingested)}

    def query(self, question):
        return {
            "answer": "stub answer",
            "sources": [],
            "retrieved_count": 0,
            "model_name": "stub-model",
        }

    def list_documents(self):
        return []


def test_health_and_auth_flow(tmp_path: Path) -> None:
    settings = Settings(api_key="test-key", uploads_dir=tmp_path / "uploads", enable_api_key_auth=True)
    app = create_app(settings=settings, rag_service=FakeService())
    client = TestClient(app)

    health_response = client.get("/api/health")
    assert health_response.status_code == 200

    unauthorized = client.post("/api/query", json={"question": "hello"})
    assert unauthorized.status_code == 401

    authorized = client.post("/api/query", json={"question": "hello"}, headers={"X-API-Key": "test-key"})
    assert authorized.status_code == 200

    upload_response = client.post(
        "/api/documents/upload",
        files={"files": ("example.txt", b"hello world", "text/plain")},
        headers={"X-API-Key": "test-key"},
    )
    assert upload_response.status_code == 200
    assert upload_response.json()["document_count"] == 1

    metrics_response = client.get("/api/metrics", headers={"X-API-Key": "test-key"})
    assert metrics_response.status_code == 200
    metrics = metrics_response.json()
    assert metrics["queries_total"] == 1
    assert metrics["ingestions_total"] == 1
    assert metrics["requests_total"] >= 4
