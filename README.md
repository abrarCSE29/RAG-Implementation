# Production RAG System

A production-grade, modular Retrieval-Augmented Generation (RAG) system built with FastAPI, Qdrant, and local Hugging Face LLMs. Designed to run on CPU-only machines (with ~16 GB RAM) while providing enterprise features like API key authentication, modular feature toggles, multi-format document ingestion, and a Streamlit showcase UI.

## Features

- **FastAPI Backend**: High-performance async API with built-in metrics and Swagger docs.
- **Qdrant Vector Database**: Robust vector storage with deterministic chunk IDs for idempotent upserts. No duplicate data when re-indexing the same file.
- **Local Local LLM Support**: Uses `transformers` pipelines configured for CPU inference (`device=-1`). Choose any efficient Hugging Face model.
- **Multi-format Ingestion**: Out-of-the-box support for:
  - Text & Markdown (`.txt`, `.md`, `.rst`, `.rtf`)
  - PDFs (`.pdf` via `pypdf`)
  - Office Files (`.docx`, `.pptx`)
  - Web & Structure (`.html`, `.csv`, `.json`, `.xml`)
  - Images (`.png`, `.jpg`, `.jpeg` with optional OCR via Tesseract)
- **Modular Architecture**: Feature flags in `settings.py` allow you to toggle:
  - API Key Authentication
  - RAG Retrieval
  - Reranking
  - Source Citations in Responses
  - Deduplication
  - OCR Fallback
- **Streamlit Demo UI**: An interactive chat interface to showcase the capabilities, upload documents, and visualize embeddings.
- **Docker-Ready**: Everything runs via a single `docker compose up` command.

## Architecture & Tech Stack

- **API/Server**: [FastAPI](https://fastapi.tiangolo.com/), Uvicorn
- **Vector Store**: [Qdrant](https://qdrant.tech/)
- **Embeddings & Generating**: [Hugging Face](https://huggingface.co/) via `sentence-transformers` and `transformers` wrappers.
- **Ingestion**: `langchain-text-splitters`, `beautifulsoup4`, `python-docx`, `pypdf`.
- **UI**: [Streamlit](https://streamlit.io/)

---

## 🚀 Quick Start (Docker - Recommended)

The easiest way to get the system running is using Docker. This will spin up the FastAPI service, the Qdrant database, and the Streamlit UI.

1. **Clone the Repo & Set up Config**:
   ```bash
   cp .env.example .env
   # Edit .env with your desired API_KEY and model names
   ```

2. **Build and Run**:
   ```bash
   docker compose up --build
   ```

3. **Access Services**:
   - API Docs (Swagger): http://localhost:8000/docs
   - Streamlit UI: http://localhost:8501
   - Qdrant Dashboard (if mapped): http://localhost:6333/dashboard

---

## 🛠️ Local Development Setup

If you prefer to run it locally without Docker:

1. **Create a Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: If you want to use the OCR feature for images, you must install Tesseract on your system (e.g., `apt-get install tesseract-ocr` or `brew install tesseract`).*

3. **Start Qdrant**:
   You still need a vector database. You can run Qdrant via Docker locally:
   ```bash
   docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
   ```
   *(Update your `.env` to point `QDRANT_URL` to `http://localhost:6333`)*

4. **Run the API**:
   ```bash
   python3 run.py
   # API will be available at http://127.0.0.1:8000/docs
   ```

5. **Run the Streamlit UI** (in a separate terminal):
   ```bash
   streamlit run streamlit_app.py
   # UI will be available at http://127.0.0.1:8501
   ```

---

## API Endpoints

Once the FastAPI server is running, the following endpoints are available:

- `GET /api/health`: Healthcheck endpoint for readiness probes.
- `GET /api/documents`: List ingested documents.
- `POST /api/documents/upload`: Upload and ingest new documents (multipart/form-data).
- `POST /api/query`: Submitting a query for RAG processing.
- `GET /api/metrics`: Internal application metrics and request counts.

*Note: All endpoints under `/api/` (except health and metrics) require the `X-API-Key` header if `ENABLE_API_KEY_AUTH` is set to true.*

---

## Testing

The project uses `pytest` for automated test coverage. Make sure all dependencies are installed.

```bash
pytest
```

## Sample Corpus

To test the ingestion engine, you can generate a sample test corpus of ~10 mixed-format documents (~11MB):

```bash
python scripts/generate_test_corpus.py
```
This script creates synthetic PDF, HTML, JSON, CSV, and markdown files in the `data/test_corpus/` directory.

---

## Project Structure

```
├── app/
│   ├── api/          # FastAPI routes, dependencies, and metrics
│   ├── config/       # Pydantic Settings and env loading
│   ├── core/         # Core logic: Embedders, LLM wrappers, Document Loader, Vector Store
│   ├── services/     # RAG Orchestration layer (connecting core components)
│   ├── web/          # Streamlit UI pages and API client
│   └── main.py       # FastAPI application factory
├── scripts/          # Helper scripts (corpus generation)
├── tests/            # Pytest test suite
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py            # Local uvicorn entrypoint
└── streamlit_app.py  # Streamlit entrypoint
```
  
