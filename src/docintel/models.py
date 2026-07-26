"""Shared domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


def new_id() -> str:
    return str(uuid4())


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass
class DocumentRecord:
    document_id: str
    filename: str
    content_type: str
    status: str
    text: str
    page_count: int | None = None
    chunk_count: int = 0
    created_at: str = field(default_factory=utc_now)
    meta: dict[str, Any] = field(default_factory=dict)


@dataclass
class ChunkRecord:
    chunk_id: str
    document_id: str
    chunk_index: int
    text: str
    strategy: str
    embedding_model: str
    embedding: list[float]
    page_start: int | None = None
    page_end: int | None = None
