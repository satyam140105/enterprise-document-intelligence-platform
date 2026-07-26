# 07 — User Flow

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Version | 1.0 |

## 1. Primary flows

### Flow A — Corpus prepare & ingest (Analyst / MLE)

```text
1. Place sample corpus under data/samples/ (or download per data/README.md)
2. Start Postgres + API (docker compose / make up)
3. POST /v1/ingest for each sample document (or batch script)
4. Poll status via response / health readiness until documents are ready
5. Confirm chunks exist via search smoke query
```

**Happy path notes:** Documents reach `ready`; embeddings stored.  
**Failure path:** unsupported type or extract failure → `failed` status + clear message.

### Flow B — Search & ask (Analyst)

```text
1. Open Swagger /docs
2. POST /v1/search with a natural-language query
3. Review scored chunks
4. POST /v1/ask with the same question
5. Read answer and verify citations against snippets
```

### Flow C — Structured extraction (Analyst)

```text
1. Choose schema_name from configs/schemas/
2. POST /v1/extract with document_id + schema_name
3. Receive fields object + evidence when available
4. Invalid schema → 422
```

### Flow D — Evaluation (Applied AI engineer)

```text
1. Ensure labeled query set under data/eval/
2. Run: python -m docintel.evaluation.run --config configs/default.yaml
3. Review reports/EVALUATION_REPORT.md and MLflow ./mlruns
4. Do not invent metrics in docs
```

### Flow E — Hiring manager review (async)

```text
1. Open README
2. Read docs/00 → 03 → 11 → 13 → 15
3. Open Swagger /docs; try /health, search, ask
4. Inspect evaluation report (after implementation) and git history
5. Form hire signal from process quality + honesty of metrics
```

## 2. Sequence — ask request

```text
Client → API: POST /v1/ask
API → Auth: optional API key check
API → Validator: check schema
API → Embedder: query vector
Embedder → Retriever: top-k from pgvector
Retriever → RAG: pack context
RAG → LLM adapter: generate
RAG → API: answer + citations
API → Client: JSON response
API → Logger: structured log line
```

## 3. Edge cases

| Case | Expected behavior |
|------|-------------------|
| Unsupported file type | HTTP 422 |
| Empty query | HTTP 422 |
| No retrieval hits | Empty search results; ask returns insufficient-context style response |
| DB down | HTTP 503 |
| Bad API key (auth enabled) | HTTP 401 |
| Unknown schema_name | HTTP 422 |
| Oversized upload | HTTP 413 or 422 per configured limit |

## 4. UI flow

None beyond FastAPI Swagger UI at `/docs` for v1 (see doc 08). Streamlit deferred.
