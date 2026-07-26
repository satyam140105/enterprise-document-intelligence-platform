# 10 — API Specification

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Style | REST · JSON · OpenAPI via FastAPI |
| Base URL (local) | `http://localhost:8000` |
| Version prefix | `/v1` |

## 1. Auth

| Mode | Detail |
|------|--------|
| Selected | Optional header `X-API-Key` |
| Default | **Disabled** when `API_KEY=change-me` |
| Enabled | When `API_KEY` is any other non-empty value, require matching header |
| Notes | Never commit real keys; document in `.env.example` |

## 2. Endpoints

### `GET /health`
**Purpose:** Liveness + dependency readiness  
**Response 200:**
```json
{
  "status": "ok",
  "database": true,
  "embedding_model_loaded": true,
  "version": "1.0.0"
}
```

### `POST /v1/ingest`
**Purpose:** Ingest a PDF or TXT document  

**Request:** `multipart/form-data` with `file` (preferred), or JSON with `path` for local sample ingest in demo mode.

**Response 200:**
```json
{
  "document_id": "<uuid>",
  "filename": "sample.pdf",
  "status": "ready",
  "chunk_count": 0,
  "content_type": "application/pdf"
}
```
`chunk_count` and final `status` reflect processing outcome. Async processing may initially return `processing` if implemented; Design Phase default preference: synchronous processing for demo simplicity unless config enables background jobs.

**Errors:**
| Code | When |
|------|------|
| 422 | Unsupported type / validation |
| 401 | Bad API key (if enabled) |
| 503 | Database unavailable |

### `POST /v1/search`
**Purpose:** Semantic search over chunks  

**Request:**
```json
{
  "query": "What is the warranty period?",
  "top_k": 5,
  "document_id": null
}
```

**Response 200:**
```json
{
  "query": "What is the warranty period?",
  "results": [
    {
      "chunk_id": "<uuid>",
      "document_id": "<uuid>",
      "score": 0.0,
      "snippet": "...",
      "chunk_index": 0
    }
  ]
}
```
Numeric scores come from the live index — do not hardcode fabricated scores in docs.

### `POST /v1/ask`
**Purpose:** RAG Q&A with citations  

**Request:**
```json
{
  "question": "What is the warranty period?",
  "top_k": 5,
  "document_id": null
}
```

**Response 200:**
```json
{
  "answer": "<generated grounded answer>",
  "citations": [
    {
      "document_id": "<uuid>",
      "chunk_id": "<uuid>",
      "score": 0.0,
      "snippet": "..."
    }
  ],
  "retrieval_k": 5,
  "model_name": "<from config>"
}
```

**Insufficient context:** return a clear message and empty or minimal citations — do not invent facts.

**Errors:** 422 / 401 / 503 as above.

### `POST /v1/extract`
**Purpose:** Structured field extraction  

**Request:**
```json
{
  "document_id": "<uuid>",
  "schema_name": "invoice_basic"
}
```

**Response 200:**
```json
{
  "document_id": "<uuid>",
  "schema_name": "invoice_basic",
  "fields": {
    "vendor_name": null,
    "invoice_date": null,
    "total_amount": null
  },
  "evidence": [
    {
      "field": "vendor_name",
      "chunk_id": "<uuid>",
      "snippet": "..."
    }
  ]
}
```
Field values are runtime outputs — docs must not invent sample “production” extractions as proven accuracy.

## 3. Versioning policy

- URL version `/v1`  
- Embedding model id and app version in health/metadata  
- Breaking schema change → `/v2`  

## 4. Example curl

```bash
curl -s http://localhost:8000/health

curl -s -X POST http://localhost:8000/v1/ingest \
  -H "X-API-Key: change-me" \
  -F "file=@data/samples/sample.pdf"

curl -s -X POST http://localhost:8000/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query":"warranty period","top_k":5}'

curl -s -X POST http://localhost:8000/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the warranty period?","top_k":5}'

curl -s -X POST http://localhost:8000/v1/extract \
  -H "Content-Type: application/json" \
  -d '{"document_id":"<uuid>","schema_name":"invoice_basic"}'
```

## 5. Decisions locked

v1 API surface is health, ingest, search, ask, extract. Swagger is the primary client. No Prompt-Engineer playground endpoints.
