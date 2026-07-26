"""Ingestion and processing pipeline."""

from __future__ import annotations

import logging
from pathlib import Path

from docintel.chunking.split import chunk_text
from docintel.config import load_config
from docintel.data.store import get_store
from docintel.embeddings.encoder import embed_texts
from docintel.models import ChunkRecord, DocumentRecord, new_id
from docintel.ocr.extract import extract_text_from_bytes, extract_text_from_path

logger = logging.getLogger(__name__)


def ingest_file(path: Path, cfg: dict | None = None) -> DocumentRecord:
    cfg = cfg or load_config()
    text, content_type, page_count = extract_text_from_path(path)
    return _process_document(
        filename=path.name,
        content_type=content_type,
        text=text,
        page_count=page_count,
        cfg=cfg,
    )


def ingest_upload(filename: str, data: bytes, cfg: dict | None = None) -> DocumentRecord:
    cfg = cfg or load_config()
    text, content_type, page_count = extract_text_from_bytes(data, filename)
    return _process_document(
        filename=filename,
        content_type=content_type,
        text=text,
        page_count=page_count,
        cfg=cfg,
    )


def _process_document(
    filename: str,
    content_type: str,
    text: str,
    page_count: int | None,
    cfg: dict,
) -> DocumentRecord:
    store = get_store()
    proc = cfg.get("processing", {})
    strategy = proc.get("chunk_strategy", "recursive")
    chunk_size = int(proc.get("chunk_size", 512))
    overlap = int(proc.get("chunk_overlap", 64))
    model_name = proc.get("embedding_model", "sentence-transformers/all-MiniLM-L6-v2")

    document_id = new_id()
    doc = DocumentRecord(
        document_id=document_id,
        filename=filename,
        content_type=content_type,
        status="processing",
        text=text,
        page_count=page_count,
    )
    store.upsert_document(doc)

    if not text.strip():
        doc.status = "failed"
        doc.meta["error"] = "empty_text"
        store.upsert_document(doc)
        raise ValueError("Document produced empty text after extraction")

    pieces = chunk_text(text, strategy=strategy, chunk_size=chunk_size, overlap=overlap)
    vectors = embed_texts(pieces, model_name)
    chunks: list[ChunkRecord] = []
    for i, (piece, vec) in enumerate(zip(pieces, vectors)):
        chunks.append(
            ChunkRecord(
                chunk_id=new_id(),
                document_id=document_id,
                chunk_index=i,
                text=piece,
                strategy=strategy,
                embedding_model=model_name,
                embedding=vec,
            )
        )
    store.replace_chunks(document_id, chunks)
    doc.chunk_count = len(chunks)
    doc.status = "ready"
    store.upsert_document(doc)
    logger.info("Ingested %s → %s chunks (%s)", filename, len(chunks), document_id)
    return doc
