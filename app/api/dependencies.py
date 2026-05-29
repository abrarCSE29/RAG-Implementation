from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status

from app.config.settings import Settings
from app.services.rag_service import RAGService


def get_app_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_rag_service(request: Request) -> RAGService:
    return request.app.state.rag_service


def require_api_key(
    request: Request,
    settings: Settings = Depends(get_app_settings),
) -> None:
    if not settings.enable_api_key_auth:
        return

    if not settings.api_key:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="API key is not configured")

    api_key = request.headers.get(settings.api_key_header)
    if api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")
