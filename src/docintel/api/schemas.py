"""Pydantic API schemas."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    database: bool
    embedding_model_loaded: bool
    version: str
    store_backend: str = "local"


class IngestPathRequest(BaseModel):
    path: str = Field(..., description="Local path relative to repo or absolute")


class IngestResponse(BaseModel):
    document_id: str
    filename: str
    status: str
    chunk_count: int
    content_type: str


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)
    document_id: str | None = None


class SearchHit(BaseModel):
    chunk_id: str
    document_id: str
    score: float
    snippet: str
    chunk_index: int


class SearchResponse(BaseModel):
    query: str
    results: list[SearchHit]


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)
    document_id: str | None = None


class Citation(BaseModel):
    chunk_id: str
    document_id: str
    score: float
    snippet: str


class AskResponse(BaseModel):
    question: str
    answer: str
    citations: list[Citation]
    mode: str


class ExtractRequest(BaseModel):
    document_id: str
    field_schema: dict[str, str] | None = None


class ExtractResponse(BaseModel):
    document_id: str
    filename: str
    fields: dict[str, Any]
