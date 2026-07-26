"""Unit tests for document intelligence pipeline."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from docintel.chunking.split import chunk_text
from docintel.data.store import reset_store_for_tests
from docintel.ingestion.pipeline import ingest_file
from docintel.ocr.extract import normalize_text
from docintel.retrieval.rag import ask, extract_fields, semantic_search


def test_normalize_and_chunk():
    text = normalize_text("Hello\n\n\nWorld\n\nThis is a longer paragraph for chunking.")
    chunks = chunk_text(text, strategy="recursive", chunk_size=20, overlap=5)
    assert len(chunks) >= 1
    assert all(isinstance(c, str) and c for c in chunks)


def test_ingest_search_ask(tmp_path: Path):
    reset_store_for_tests(tmp_path)
    sample = Path("data/samples/warranty_policy.txt")
    if not sample.exists():
        sample = Path(__file__).resolve().parents[1] / "data" / "samples" / "warranty_policy.txt"
    doc = ingest_file(sample)
    assert doc.status == "ready"
    assert doc.chunk_count > 0

    hits = semantic_search("warranty period manufacturing defects", top_k=3)
    assert hits
    assert hits[0]["score"] > 0.1

    resp = ask("What is the warranty period?")
    assert resp["citations"]
    assert "chunk" in resp["answer"].lower() or "[" in resp["answer"]

    fields = extract_fields(doc.document_id)
    assert fields["fields"]["warranty_period"] is not None
    assert fields["fields"]["policy_id"] == "POL-2048-WX"


def test_api_health_and_search(tmp_path: Path, monkeypatch):
    reset_store_for_tests(tmp_path)
    sample = Path(__file__).resolve().parents[1] / "data" / "samples" / "technical_faq.txt"
    ingest_file(sample)

    from docintel.api import main as api_main

    with TestClient(api_main.app) as client:
        health = client.get("/health")
        assert health.status_code == 200
        body = health.json()
        assert "version" in body

        search = client.post("/v1/search", json={"query": "audit log retention", "top_k": 3})
        assert search.status_code == 200
        assert len(search.json()["results"]) >= 1
