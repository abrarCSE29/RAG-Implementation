from __future__ import annotations

import logging
from time import perf_counter

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config.settings import Settings, get_settings
from app.services.rag_service import RAGService


def create_app(settings: Settings | None = None, rag_service: RAGService | None = None) -> FastAPI:
    resolved_settings = settings or get_settings()
    logger = logging.getLogger("rag")
    application = FastAPI(
        title=resolved_settings.app_name,
        version=resolved_settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    application.state.settings = resolved_settings
    application.state.rag_service = rag_service or RAGService(resolved_settings)
    application.state.metrics = {
        "requests_total": 0,
        "queries_total": 0,
        "ingestions_total": 0,
        "last_request_ms": 0.0,
    }

    @application.middleware("http")
    async def collect_metrics(request, call_next):
        start = perf_counter()
        response = await call_next(request)
        duration_ms = (perf_counter() - start) * 1000
        metrics = request.app.state.metrics
        metrics["requests_total"] += 1
        metrics["last_request_ms"] = round(duration_ms, 2)
        logger.info("%s %s -> %s in %.2fms", request.method, request.url.path, response.status_code, duration_ms)
        return response

    application.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(router, prefix="/api")
    return application


app = create_app()
