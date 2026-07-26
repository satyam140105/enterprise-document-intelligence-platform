"""Embedding service via sentence-transformers (lazy load)."""

from __future__ import annotations

import logging
import threading
from functools import lru_cache

import numpy as np

logger = logging.getLogger(__name__)
_LOCK = threading.Lock()
_MODEL = None
_MODEL_NAME: str | None = None


def get_embedding_model(model_name: str):
    global _MODEL, _MODEL_NAME
    with _LOCK:
        if _MODEL is not None and _MODEL_NAME == model_name:
            return _MODEL
        logger.info("Loading embedding model: %s", model_name)
        from sentence_transformers import SentenceTransformer

        _MODEL = SentenceTransformer(model_name)
        _MODEL_NAME = model_name
        return _MODEL


def embed_texts(texts: list[str], model_name: str) -> list[list[float]]:
    if not texts:
        return []
    model = get_embedding_model(model_name)
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    arr = np.asarray(vectors, dtype=np.float32)
    return [row.tolist() for row in arr]


def embed_query(text: str, model_name: str) -> list[float]:
    return embed_texts([text], model_name)[0]


@lru_cache(maxsize=1)
def model_loaded_name() -> str | None:
    return _MODEL_NAME
