from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi import Request

from app.api.dependencies import get_app_settings, get_rag_service, require_api_key
from app.config.settings import Settings
from app.schemas import ChunkListResponse, ChunkRecord, DocumentListResponse, DocumentRecord, HealthResponse, IngestionResult, MetricsResponse, QueryRequest, QueryResponse, SourceChunk
from app.services.rag_service import RAGService

router = APIRouter(tags=["rag"])


@router.get("/health", response_model=HealthResponse)
def health(settings: Settings = Depends(get_app_settings)) -> HealthResponse:
    return HealthResponse(
        app_name=settings.app_name,
        environment=settings.environment,
        features={
            "ingestion": settings.enable_ingestion,
            "rag": settings.enable_rag,
            "reranking": settings.enable_reranking,
            "citations": settings.enable_citations,
            "api_key_auth": settings.enable_api_key_auth,
            "ocr": settings.enable_ocr,
        },
    )


@router.get("/documents", response_model=DocumentListResponse, dependencies=[Depends(require_api_key)])
def list_documents(rag_service: RAGService = Depends(get_rag_service)) -> DocumentListResponse:
    documents = [DocumentRecord(**record) for record in rag_service.list_documents()]
    return DocumentListResponse(count=len(documents), documents=documents)


@router.get("/documents/chunks", response_model=ChunkListResponse, dependencies=[Depends(require_api_key)])
def list_chunks(
    document_id: str | None = None,
    rag_service: RAGService = Depends(get_rag_service),
) -> ChunkListResponse:
    chunks = [ChunkRecord(**record) for record in rag_service.list_chunks(document_id=document_id)]
    return ChunkListResponse(count=len(chunks), chunks=chunks)


@router.get("/metrics", response_model=MetricsResponse, dependencies=[Depends(require_api_key)])
def metrics(request: Request) -> MetricsResponse:
    metrics_data = request.app.state.metrics
    return MetricsResponse(**metrics_data)


@router.post("/documents/upload", response_model=IngestionResult, dependencies=[Depends(require_api_key)])
async def upload_documents(
    request: Request,
    files: list[UploadFile] = File(...),
    rag_service: RAGService = Depends(get_rag_service),
    settings: Settings = Depends(get_app_settings),
) -> IngestionResult:
    if not files:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No files provided")

    saved_paths: list[Path] = []
    settings.uploads_dir.mkdir(parents=True, exist_ok=True)

    for upload_file in files:
        file_name = Path(upload_file.filename or "uploaded-file").name
        destination = settings.uploads_dir / file_name
        contents = await upload_file.read()
        if len(contents) > settings.max_upload_mb * 1024 * 1024:
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=f"{file_name} exceeds the allowed size")
        destination.write_bytes(contents)
        saved_paths.append(destination)

    result = rag_service.ingest_paths(saved_paths)
    request.app.state.metrics["ingestions_total"] += result["chunk_count"]
    return IngestionResult(**result)


@router.post("/query", response_model=QueryResponse, dependencies=[Depends(require_api_key)])
def query(payload: QueryRequest, request: Request, rag_service: RAGService = Depends(get_rag_service)) -> QueryResponse:
    request.app.state.metrics["queries_total"] += 1
    result = rag_service.query(payload.question)
    return QueryResponse(
        answer=result["answer"],
        sources=[SourceChunk(**source) for source in result["sources"]],
        retrieved_count=result["retrieved_count"],
        model_name=result["model_name"],
    )
