# 05 — Feature Specification

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Product | Enterprise Document Intelligence Platform |
| Version | 1.0 |

## 1. Feature list (v1)

| ID | Feature | Priority | Depends on | Status |
|----|---------|----------|------------|--------|
| F01 | Document ingest (PDF/TXT) | P0 | DB | In scope |
| F02 | Text extraction (digital PDF / TXT) | P0 | F01 | In scope |
| F03 | Optional OCR path (pytesseract) for scans | P2 | F02 | In scope (optional) |
| F04 | Chunking strategies (config-selectable) | P0 | F02 | In scope |
| F05 | Embeddings (sentence-transformers / HF) | P0 | F04 | In scope |
| F06 | pgvector persistence | P0 | F05 | In scope |
| F07 | Semantic search | P0 | F06 | In scope |
| F08 | RAG Q&A with citations | P0 | F07 | In scope |
| F09 | Structured field extraction (configurable schema) | P0 | F02 | In scope |
| F10 | Evaluation harness (hit-rate + citation/faithfulness) | P0 | F07/F08 | In scope |
| F11 | MLflow logging for eval/experiments | P1 | F10 | In scope |
| F12 | FastAPI `GET /health` | P0 | — | In scope |
| F13 | FastAPI `POST /v1/ingest` | P0 | F01 | In scope |
| F14 | FastAPI `POST /v1/search` | P0 | F07 | In scope |
| F15 | FastAPI `POST /v1/ask` | P0 | F08 | In scope |
| F16 | FastAPI `POST /v1/extract` | P0 | F09 | In scope |
| F17 | Optional `X-API-Key` auth | P1 | API | In scope |
| F18 | Structured request logging (stdout) | P1 | API | In scope |
| F19 | Docker Compose (API + Postgres) | P1 | API + DB | In scope |
| F20 | CI: lint + pytest | P1 | — | In scope |

## 2. Feature details

### F01 / F13 — Ingest
- **Description:** Accept PDF or TXT upload; create document record; kick off processing  
- **Inputs:** multipart file or configured sample path  
- **Outputs:** `document_id`, status  
- **Acceptance:** see doc 26  

### F04 — Chunking
- **Description:** At least two documented strategies (e.g. fixed token window with overlap; recursive/paragraph-aware)  
- **Config:** `configs/default.yaml` strategy + sizes  
- **Output:** chunk rows linked to `document_id`  

### F07 / F14 — Semantic search
- **Description:** Embed query; return top-k chunks with scores and snippets  
- **Filters:** optional `document_id`  

### F08 / F15 — Ask (RAG)
- **Description:** Retrieve → pack context → generate → return answer + citations  
- **Failure mode:** insufficient context returns explicit message, not fabricated certainty  

### F09 / F16 — Extract
- **Description:** Apply named schema to a document; return structured fields + evidence when available  
- **Schemas:** under `configs/schemas/`  

### F10 — Evaluation
- **Description:** Offline harness on labeled queries; hit-rate @k; citation coverage; faithfulness checklist  
- **Outputs:** `reports/EVALUATION_REPORT.md` — real numbers only  

## 3. Out of scope features (v1)

| Idea | Why deferred |
|------|----------------|
| Custom React UI | Swagger-only UX decision |
| Streamlit demo | Optional later; not required for Design Phase freeze |
| Multi-tenant ACL / SSO | Outside portfolio scope |
| LangChain agent tools | Explicit stack exclusion |
| Fine-tuning pipeline as required path | Not needed for v1 demo |
| Production plant deployment claims | Honesty constraint |

## 4. Dependency graph (simple)

```text
F01 → F02 → F04 → F05 → F06 → F07 → F08
                 └→ F09
F07/F08 → F10 → F11
F01 → F13
F07 → F14
F08 → F15
F09 → F16
F12 independent
API → F17, F18
F19 after API + DB
F20 parallel after package exists
```
