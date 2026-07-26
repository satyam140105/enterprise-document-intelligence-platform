"""FastAPI service — Enterprise Document Intelligence Platform."""

from __future__ import annotations

import logging
import os
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, File, Header, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from docintel import __version__
from docintel.api.schemas import (
    AskRequest,
    AskResponse,
    Citation,
    ExtractRequest,
    ExtractResponse,
    HealthResponse,
    IngestPathRequest,
    IngestResponse,
    SearchHit,
    SearchRequest,
    SearchResponse,
)
from docintel.config import ROOT, load_config
from docintel.data.store import get_store
from docintel.embeddings import encoder as emb
from docintel.ingestion.pipeline import ingest_file, ingest_upload
from docintel.retrieval.rag import ask, extract_fields, semantic_search

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def _api_key_enabled() -> bool:
    key = os.getenv("API_KEY", "").strip()
    return bool(key) and key != "change-me"


def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if not _api_key_enabled():
        return
    if not x_api_key or x_api_key != os.getenv("API_KEY", ""):
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    cfg = load_config()
    model = cfg.get("processing", {}).get(
        "embedding_model", "sentence-transformers/all-MiniLM-L6-v2"
    )
    try:
        emb.get_embedding_model(model)
        logger.info("Embedding model ready: %s", model)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Embedding model not loaded at startup: %s", exc)
    get_store()
    yield


app = FastAPI(
    title="Enterprise Document Intelligence Platform",
    description=(
        "Enterprise-grade intelligent document processing for OCR/text extraction, "
        "semantic search, RAG Q&A with citations, and structured field extraction. "
        "Portfolio project by Mohammad Ahmadian — Applied AI / LLM Engineer."
    ),
    version=__version__,
    lifespan=lifespan,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    logger.info(
        "method=%s path=%s status=%s latency_ms=%.2f",
        request.method,
        request.url.path,
        response.status_code,
        (time.perf_counter() - start) * 1000,
    )
    return response


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    loaded = emb.model_loaded_name() is not None
    return HealthResponse(
        status="ok" if loaded else "degraded",
        database=True,  # local store always available; Postgres optional in Compose
        embedding_model_loaded=loaded,
        version=__version__,
        store_backend="local",
    )


@app.post("/v1/ingest", response_model=IngestResponse, dependencies=[Depends(verify_api_key)])
async def ingest_upload_endpoint(
    file: Annotated[UploadFile, File()],
) -> IngestResponse:
    try:
        data = await file.read()
        max_mb = int(load_config().get("api", {}).get("max_upload_mb", 20))
        if len(data) > max_mb * 1024 * 1024:
            raise HTTPException(status_code=422, detail=f"File exceeds {max_mb}MB")
        doc = ingest_upload(file.filename or "upload.bin", data)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return IngestResponse(
        document_id=doc.document_id,
        filename=doc.filename,
        status=doc.status,
        chunk_count=doc.chunk_count,
        content_type=doc.content_type,
    )


@app.post("/v1/ingest/path", response_model=IngestResponse, dependencies=[Depends(verify_api_key)])
def ingest_path_endpoint(body: IngestPathRequest) -> IngestResponse:
    path = Path(body.path)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        raise HTTPException(status_code=422, detail=f"Path not found: {path}")
    try:
        doc = ingest_file(path)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return IngestResponse(
        document_id=doc.document_id,
        filename=doc.filename,
        status=doc.status,
        chunk_count=doc.chunk_count,
        content_type=doc.content_type,
    )


@app.post("/v1/search", response_model=SearchResponse, dependencies=[Depends(verify_api_key)])
def search(req: SearchRequest) -> SearchResponse:
    results = semantic_search(req.query, top_k=req.top_k, document_id=req.document_id)
    return SearchResponse(
        query=req.query,
        results=[
            SearchHit(
                chunk_id=r["chunk_id"],
                document_id=r["document_id"],
                score=r["score"],
                snippet=r["snippet"],
                chunk_index=r["chunk_index"],
            )
            for r in results
        ],
    )


@app.post("/v1/ask", response_model=AskResponse, dependencies=[Depends(verify_api_key)])
def ask_endpoint(req: AskRequest) -> AskResponse:
    resp = ask(req.question, top_k=req.top_k, document_id=req.document_id)
    return AskResponse(
        question=resp["question"],
        answer=resp["answer"],
        citations=[Citation(**c) for c in resp["citations"]],
        mode=resp["mode"],
    )


@app.post("/v1/extract", response_model=ExtractResponse, dependencies=[Depends(verify_api_key)])
def extract_endpoint(req: ExtractRequest) -> ExtractResponse:
    try:
        result = extract_fields(req.document_id, schema=req.field_schema)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return ExtractResponse(**result)


@app.exception_handler(Exception)
async def unhandled(_request: Request, exc: Exception):
    logger.exception("Unhandled: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
