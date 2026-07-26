"""Retrieval and RAG generation (thin custom orchestration)."""

from __future__ import annotations

import logging
import os
import re
from typing import Any

from docintel.config import load_config
from docintel.data.store import get_store
from docintel.embeddings.encoder import embed_query

logger = logging.getLogger(__name__)


def semantic_search(
    query: str,
    top_k: int | None = None,
    document_id: str | None = None,
    cfg: dict | None = None,
) -> list[dict[str, Any]]:
    cfg = cfg or load_config()
    top_k = top_k or int(cfg.get("retrieval", {}).get("top_k", 5))
    model_name = cfg.get("processing", {}).get(
        "embedding_model", "sentence-transformers/all-MiniLM-L6-v2"
    )
    qvec = embed_query(query, model_name)
    hits = get_store().search(qvec, top_k=top_k, document_id=document_id)
    return [
        {
            "chunk_id": ch.chunk_id,
            "document_id": ch.document_id,
            "score": score,
            "snippet": ch.text[:400],
            "text": ch.text,
            "chunk_index": ch.chunk_index,
        }
        for ch, score in hits
    ]


def ask(
    question: str,
    top_k: int | None = None,
    document_id: str | None = None,
    cfg: dict | None = None,
) -> dict[str, Any]:
    """
    Retrieve → pack context → generate answer with citations.

    Uses optional OpenAI-compatible LLM when LLM_API_KEY is set;
    otherwise extractive grounded answer (portfolio-safe default).
    """
    cfg = cfg or load_config()
    hits = semantic_search(question, top_k=top_k, document_id=document_id, cfg=cfg)
    citations = [
        {
            "chunk_id": h["chunk_id"],
            "document_id": h["document_id"],
            "score": h["score"],
            "snippet": h["snippet"],
        }
        for h in hits
    ]
    if not hits:
        return {
            "question": question,
            "answer": "No relevant passages found in the indexed corpus.",
            "citations": [],
            "mode": "extractive",
        }

    answer, mode = _generate_answer(question, hits)
    return {
        "question": question,
        "answer": answer,
        "citations": citations,
        "mode": mode,
    }


def _generate_answer(question: str, hits: list[dict[str, Any]]) -> tuple[str, str]:
    api_key = os.getenv("LLM_API_KEY", "").strip()
    if api_key:
        try:
            return _llm_answer(question, hits), "llm"
        except Exception as exc:  # noqa: BLE001
            logger.warning("LLM generation failed; falling back to extractive: %s", exc)
    return _extractive_answer(question, hits), "extractive"


def _extractive_answer(question: str, hits: list[dict[str, Any]]) -> str:
    """Grounded extractive response with explicit citation markers."""
    parts = [
        f"Based on the retrieved passages for: “{question}”",
        "",
    ]
    for i, h in enumerate(hits[:3], start=1):
        cite = f"[{i}:chunk:{h['chunk_id'][:8]}]"
        snippet = h["text"].strip().replace("\n", " ")
        if len(snippet) > 320:
            snippet = snippet[:317] + "..."
        parts.append(f"{cite} {snippet}")
    parts.append("")
    parts.append(
        "Citations refer to retrieved chunk IDs. This answer is extractive "
        "(no external LLM key configured)."
    )
    return "\n".join(parts)


def _llm_answer(question: str, hits: list[dict[str, Any]]) -> str:
    import httpx

    base = os.getenv("LLM_API_BASE", "https://api.openai.com/v1").rstrip("/")
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    key = os.getenv("LLM_API_KEY", "")
    context = "\n\n".join(
        f"[chunk_id={h['chunk_id']}]\n{h['text']}" for h in hits[:5]
    )
    prompt = (
        "Answer the question using ONLY the context. "
        "Cite chunk_id values inline like [chunk_id=...]. "
        "If unknown, say you cannot find it in the documents.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}"
    )
    resp = httpx.post(
        f"{base}/chat/completions",
        headers={"Authorization": f"Bearer {key}"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a precise document QA assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.1,
        },
        timeout=60.0,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def extract_fields(
    document_id: str,
    schema: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Structured field extraction against a simple schema.

    Schema maps field_name -> regex pattern (Python).
    Defaults cover warranty / invoice-like portfolio samples.
    """
    store = get_store()
    doc = store.get_document(document_id)
    if not doc:
        raise ValueError(f"Unknown document_id: {document_id}")
    text = doc.text
    schema = schema or {
        "warranty_period": r"(?i)warranty\s*(?:period)?\s*[:\-]?\s*([^\n\.]+)",
        "effective_date": r"(?i)effective\s*date\s*[:\-]?\s*([0-9]{4}-[0-9]{2}-[0-9]{2}|[A-Za-z]+ \d{1,2}, \d{4})",
        "invoice_total": r"(?i)(?:total|amount due)\s*[:\-]?\s*\$?\s*([0-9,]+\.?[0-9]*)",
        "policy_id": r"(?i)policy\s*(?:id|number)\s*[:\-]?\s*([A-Z0-9\-]+)",
    }
    fields: dict[str, Any] = {}
    for name, pattern in schema.items():
        m = re.search(pattern, text)
        fields[name] = m.group(1).strip() if m else None
    return {
        "document_id": document_id,
        "filename": doc.filename,
        "fields": fields,
    }
