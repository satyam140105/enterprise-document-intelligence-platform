"""Vector + document store: local numpy backend (default) with optional Postgres path."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Protocol

import numpy as np

from docintel.config import ROOT
from docintel.models import ChunkRecord, DocumentRecord

logger = logging.getLogger(__name__)


class DocumentStore(Protocol):
    def upsert_document(self, doc: DocumentRecord) -> None: ...

    def get_document(self, document_id: str) -> DocumentRecord | None: ...

    def list_documents(self) -> list[DocumentRecord]: ...

    def replace_chunks(self, document_id: str, chunks: list[ChunkRecord]) -> None: ...

    def all_chunks(self, document_id: str | None = None) -> list[ChunkRecord]: ...

    def search(
        self,
        query_vec: list[float],
        top_k: int = 5,
        document_id: str | None = None,
    ) -> list[tuple[ChunkRecord, float]]: ...


class LocalDocumentStore:
    """File-backed store for demo/CI without requiring Postgres."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or (ROOT / "data" / "processed" / "index")
        self.root.mkdir(parents=True, exist_ok=True)
        self.docs_path = self.root / "documents.json"
        self.chunks_path = self.root / "chunks.json"
        self._docs: dict[str, dict] = {}
        self._chunks: list[dict] = []
        self._load()

    def _load(self) -> None:
        if self.docs_path.exists():
            self._docs = json.loads(self.docs_path.read_text(encoding="utf-8"))
        if self.chunks_path.exists():
            self._chunks = json.loads(self.chunks_path.read_text(encoding="utf-8"))

    def _save(self) -> None:
        self.docs_path.write_text(json.dumps(self._docs, indent=2), encoding="utf-8")
        self.chunks_path.write_text(json.dumps(self._chunks, indent=2), encoding="utf-8")

    def upsert_document(self, doc: DocumentRecord) -> None:
        self._docs[doc.document_id] = {
            "document_id": doc.document_id,
            "filename": doc.filename,
            "content_type": doc.content_type,
            "status": doc.status,
            "text": doc.text,
            "page_count": doc.page_count,
            "chunk_count": doc.chunk_count,
            "created_at": doc.created_at,
            "meta": doc.meta,
        }
        self._save()

    def get_document(self, document_id: str) -> DocumentRecord | None:
        raw = self._docs.get(document_id)
        if not raw:
            return None
        return DocumentRecord(**raw)

    def list_documents(self) -> list[DocumentRecord]:
        return [DocumentRecord(**v) for v in self._docs.values()]

    def replace_chunks(self, document_id: str, chunks: list[ChunkRecord]) -> None:
        self._chunks = [c for c in self._chunks if c["document_id"] != document_id]
        for ch in chunks:
            self._chunks.append(
                {
                    "chunk_id": ch.chunk_id,
                    "document_id": ch.document_id,
                    "chunk_index": ch.chunk_index,
                    "text": ch.text,
                    "strategy": ch.strategy,
                    "embedding_model": ch.embedding_model,
                    "embedding": ch.embedding,
                    "page_start": ch.page_start,
                    "page_end": ch.page_end,
                }
            )
        self._save()

    def all_chunks(self, document_id: str | None = None) -> list[ChunkRecord]:
        rows = self._chunks
        if document_id:
            rows = [c for c in rows if c["document_id"] == document_id]
        return [ChunkRecord(**c) for c in rows]

    def search(
        self,
        query_vec: list[float],
        top_k: int = 5,
        document_id: str | None = None,
    ) -> list[tuple[ChunkRecord, float]]:
        chunks = self.all_chunks(document_id)
        if not chunks:
            return []
        q = np.asarray(query_vec, dtype=np.float32)
        q = q / (np.linalg.norm(q) + 1e-12)
        scored: list[tuple[ChunkRecord, float]] = []
        for ch in chunks:
            v = np.asarray(ch.embedding, dtype=np.float32)
            v = v / (np.linalg.norm(v) + 1e-12)
            score = float(np.dot(q, v))
            scored.append((ch, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]


_STORE: LocalDocumentStore | None = None


def get_store() -> LocalDocumentStore:
    global _STORE
    if _STORE is None:
        _STORE = LocalDocumentStore()
    return _STORE


def reset_store_for_tests(tmp_path: Path) -> LocalDocumentStore:
    global _STORE
    _STORE = LocalDocumentStore(tmp_path)
    return _STORE
