# 02 — Software Design Specification (SDS)

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Depends on | 01_PRD, 03_Architecture, 04_Tech Stack |
| Version | 1.0 |
| Scope | Frozen |

## 1. Design principles

1. Ingest / index / query separation  
2. Config-driven pipelines (`configs/`)  
3. Thin custom RAG orchestration (no LangChain-heavy dependency surface)  
4. Citations required on generated answers  
5. Fail loud on bad input (Pydantic API validation)  
6. Digital-PDF-first text extraction; optional OCR path labeled  
7. Evaluation before demo claims — metrics only from real runs  
8. Honest limitations: sample corpus, not production plant deployment  

## 2. System context

**In scope modules:**
- Document ingest & metadata persistence  
- Text extraction (pdfplumber / pypdf; optional pytesseract)  
- Chunking strategies  
- Embedding + pgvector store  
- Semantic search  
- RAG ask with citations  
- Structured field extraction  
- Evaluation harness + MLflow logging where relevant  
- FastAPI surface  
- Structured logging / basic observability hooks  

**Out of scope modules (v1):**  
Custom React UI, Streamlit (optional later), multi-tenant SaaS, LangChain-centric apps, fine-tuning pipelines as required path, plant/ERP connectors.

## 3. Logical components

| Component | Responsibility | Package path |
|-----------|----------------|--------------|
| Ingest | Accept PDF/TXT; store blob/metadata | `docintel.ingest` |
| Extractor | Text extraction / OCR path | `docintel.processing` |
| Chunker | Strategy-based chunking | `docintel.processing` |
| Embedder | sentence-transformers / HF embeddings | `docintel.embeddings` |
| Store | PostgreSQL + pgvector CRUD | `docintel.store` |
| Retriever | Semantic search @k | `docintel.retrieval` |
| RAG | Prompt assembly + generation + citations | `docintel.rag` |
| Extract | Schema-driven field extraction | `docintel.extraction` |
| Eval | Hit-rate + citation/faithfulness checklist | `docintel.evaluation` |
| API | HTTP contract | `docintel.api` |
| Config | YAML defaults + env overrides | `configs/` |

## 4. Key design decisions (ADR-lite)

### ADR-001 — Vector store
- **Decision:** PostgreSQL + pgvector  
- **Why:** Unified portfolio stack; durable metadata + vectors; SQL-friendly  
- **Rejected:** In-memory-only FAISS as sole store — insufficient for API demo persistence  

### ADR-002 — RAG orchestration
- **Decision:** Thin custom retrieve → context pack → generate → cite  
- **Why:** Clear control for hiring-manager review; avoids LangChain-heavy surface  
- **Rejected:** Full LangChain/LlamaIndex app as primary architecture  

### ADR-003 — Serving interface
- **Decision:** FastAPI REST (`/health`, `/v1/ingest`, `/v1/search`, `/v1/ask`, `/v1/extract`)  
- **Why:** OpenAPI/Swagger for recruiters; matches portfolio DNA  

### ADR-004 — OCR stance
- **Decision:** Digital PDF/TXT first; pytesseract optional for scans  
- **Why:** Reliable demo path; OCR quality variance documented  

### ADR-005 — Auth
- **Decision:** Optional `X-API-Key`; disabled when `API_KEY=change-me`  
- **Why:** Safe local demo default; easy to enable for shared demos  

### ADR-006 — UI
- **Decision:** Swagger primary; Streamlit optional later  
- **Why:** API-first portfolio posture  

## 5. Data contracts

### Document (conceptual)
```text
document_id: uuid
filename: str
content_type: application/pdf | text/plain
status: pending | processing | ready | failed
source_path: str
page_count: int | null
created_at: datetime
error_message: str | null
```

### Chunk (conceptual)
```text
chunk_id: uuid
document_id: uuid
chunk_index: int
text: str
page_start / page_end: int | null
token_estimate: int
embedding: vector(dim)  # pgvector
strategy: str  # e.g. fixed_tokens | recursive | page
```

### Search result
```text
chunk_id, document_id, score, text_snippet, metadata
```

### Ask response
```text
answer: str
citations: [{ document_id, chunk_id, score, snippet }]
model_name: str
retrieval_k: int
```

### Extract response
```text
document_id, schema_name, fields: { name: value },
citations / evidence per field when available
```

## 6. Error handling strategy

| Layer | Behavior |
|-------|----------|
| Ingest validation | Reject unsupported types; clear 422 |
| Processing | Mark document `failed` with message; do not crash API process |
| Retrieval | Empty results → honest empty list / “insufficient context” ask path |
| API | HTTP 422 bad payload; 401 bad API key (if enabled); 503 DB/model unavailable; 5xx logged |

## 7. Extensibility

How to add a chunking strategy:  
Implement under `docintel.processing.chunking`, register name in config, document in docs/13, add unit tests.

How to add an embedding model:  
Config swap of HF model id; re-index required; bump embedding version tag in DB metadata.

How to add an extraction schema:  
YAML/JSON schema under `configs/schemas/`; no Prompt-Engineer gallery — schemas are product config.

## 8. Decisions locked

No open design questions for Design Phase v1. Future work (Streamlit, hosted demo, multi-tenant) stays out of scope until explicitly scoped.
