# 03 — System Architecture

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Diagram path | Text diagram below (optional export: `docs/assets/architecture.png`) |
| Version | 1.0 |

## 1. Architecture overview

Clients upload PDF/TXT via FastAPI ingest. The processing pipeline extracts text (digital-first; optional OCR), applies a configured chunking strategy, embeds chunks with a sentence-transformers / Hugging Face model, and persists documents, chunks, and vectors in PostgreSQL + pgvector. Semantic search queries the vector index. RAG ask retrieves top-k chunks, packs context, generates an answer through a thin custom orchestration layer, and returns citations. Structured extraction runs schema-driven field extraction with optional evidence snippets. Evaluation jobs measure retrieval hit-rate and citation coverage / faithfulness checklist and may log to local MLflow (`./mlruns`). Demo UI is Swagger; Streamlit is optional later.

## 2. High-level diagram (text)

```text
[PDF / TXT corpus] --> [POST /v1/ingest]
                              |
                              v
                    [Extract text / optional OCR]
                              |
                              v
                         [Chunking]
                              |
                              v
              [HF sentence-transformers embeddings]
                              |
                              v
                 [PostgreSQL + pgvector store]
                     /        |        \
                    v         v         v
           [GET/POST search] [ask RAG] [extract]
                    |         |         |
                    +----+----+----+----+
                         |
                         v
              [FastAPI + Swagger /docs]
                         |
                         v
              [stdout structured logs]
                         |
          [Eval harness + MLflow ./mlruns]
```

Tool for optional export: Mermaid / Excalidraw → `docs/assets/architecture.png`.

## 3. C4-style views

### Context
- Users/systems that call the API: analysts, demo clients, hiring-manager review via Swagger  
- External systems: Hugging Face model downloads; optional LLM API provider; local PostgreSQL  

### Containers
| Container | Tech | Role |
|-----------|------|------|
| API | FastAPI + Uvicorn | Ingest, search, ask, extract, health |
| Database | PostgreSQL + pgvector | Documents, chunks, embeddings |
| Eval job | Python CLI (`docintel.evaluation`) | Hit-rate + faithfulness checklist |
| Tracking | MLflow local `./mlruns` | Eval/experiment logs |
| Packaging | Docker Compose | API + Postgres |

### Components (API)
| Component | Role |
|-----------|------|
| routers | HTTP endpoints |
| schemas | Pydantic request/response models |
| services | ingest, search, ask, extract orchestration |
| store | DB access |
| auth | optional `X-API-Key` middleware |
| logging | structured request logs |

## 4. Runtime sequence — ingest

1. Client `POST /v1/ingest` with file or path reference  
2. Validate content type (PDF/TXT)  
3. Persist document row (`status=pending`)  
4. Extract text (pdfplumber/pypdf; optional pytesseract)  
5. Chunk per config strategy  
6. Embed chunks; upsert into pgvector  
7. Mark document `ready` (or `failed` with message)  
8. Return `document_id` + status  

## 5. Runtime sequence — ask (RAG)

1. Client `POST /v1/ask` with question (+ optional filters)  
2. Embed query; retrieve top-k chunks from pgvector  
3. If insufficient context, return explicit insufficient-context response  
4. Pack citations + context into thin custom prompt  
5. Generate answer via configured LLM adapter  
6. Return answer + citation list (chunk/document IDs, scores, snippets)  
7. Structured log with latency and retrieval_k  

## 6. Cross-cutting concerns

| Concern | Approach |
|---------|----------|
| Config | YAML + env |
| Secrets | `.env` (never commit); `.env.example` only |
| Observability | Structured stdout logs (doc 17) |
| Security | Optional API key; Pydantic validation; upload limits (doc 18) |

## 7. Non-functional targets

| NFR | Target |
|-----|--------|
| Availability | Single instance OK for portfolio |
| Latency p95 | Interactive local demo; log `latency_ms` |
| Throughput | Suitable for demo corpus size |
| Reproducibility | Fixed seed where applicable + pinned deps + MLflow params |

## 8. Decisions locked

Architecture for Design Phase v1 is fixed: FastAPI + PostgreSQL/pgvector + custom RAG + HF embeddings + Docker Compose + Swagger. Implementation not started.
