from pathlib import Path

from app.core.document_loader import DocumentIngestor
from app.config.settings import Settings


def test_document_ingestor_supports_multiple_plaintext_formats(tmp_path: Path) -> None:
    settings = Settings(enable_ocr=False)
    ingestor = DocumentIngestor(settings)

    txt_file = tmp_path / "sample.txt"
    txt_file.write_text("Hello world\nThis is a test document.", encoding="utf-8")

    html_file = tmp_path / "sample.html"
    html_file.write_text("<html><body><h1>Report</h1><p>Quarterly summary.</p></body></html>", encoding="utf-8")

    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("name,score\nAlice,10\nBob,12", encoding="utf-8")

    json_file = tmp_path / "sample.json"
    json_file.write_text('{"team": "search", "status": "ready"}', encoding="utf-8")

    documents = ingestor.load_files([txt_file, html_file, csv_file, json_file])
    chunks = ingestor.chunk_documents(documents)

    assert len(documents) == 4
    assert len(chunks) >= 4
    assert any("Quarterly summary" in chunk.text for chunk in chunks)
    assert any(chunk.metadata.get("mime_type") == "text/csv" for chunk in chunks)
