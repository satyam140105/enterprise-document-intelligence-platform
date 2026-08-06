# 26 — Acceptance Criteria

| Field | Value |
|-------|--------|
| Status | Ready · Release gates closed |
| Use | Gate for Design Phase docs freeze; gate for Released |
| Version | 1.0 |
| Last updated | 2026-07-26 |

## 1. Documentation gates (Design Phase)

- [x] Docs in `00_MASTER_INDEX` marked Ready (Design Phase)  
- [x] No critical `[FILL]` left in PRD, Architecture, Dataset, Processing, Model, Evaluation, API  
- [x] Doc 13 titled Document Processing Pipeline (not feature engineering)  
- [x] `docs/status.md` shows Status: **Released**  
- [x] README quickstart works as written  

## 2. Functional gates (implementation)

- [x] Sample corpus under `data/samples/`  
- [x] Ingest accepts PDF/TXT and stores document + chunks  
- [x] Embeddings persisted (local file-backed store for demo/CI; Postgres/pgvector path documented for enterprise Compose)  
- [x] `POST /v1/search` returns ranked chunks  
- [x] `POST /v1/ask` returns answer with citations  
- [x] `POST /v1/extract` returns schema fields  
- [x] Evaluation report under `reports/EVALUATION_REPORT.md`  
- [x] API `GET /health` returns 200  
- [x] Invalid payload returns 422  

## 3. Quality gates

- [x] `pytest` passes  
- [x] `ruff check` passes (clean after fix)  
- [x] No secrets in git history  
- [x] `.env.example` present  

## 4. AI performance gates

| Criterion | Rule | Result |
|-----------|------|--------|
| Hit-rate @k computed | Real run only | **1.000** @5 |
| Citations on demo asks | Required | Met |
| Faithfulness checklist | Required | **1.000** |
| Limitations documented | Required | README |
| Invented scores | Forbidden | Not used |

## 5. MLOps / deploy gates

- [x] Eval artifacts under `reports/`  
- [x] Docker + Compose files present  
- [x] Swagger path works (`/docs`)  

## 6. Git / professionalism gates

- [x] Conventional commits used  
- [x] `main` history readable  
- [x] LICENSE present  

## 7. Traceability IDs

| ID | Criterion | Status |
|----|-----------|--------|
| AC-DOC-01 | Docs + evaluation report | Pass |
| AC-PIPE-01 | Ingest → extract → chunk → embed | Pass |
| AC-ML-01 | Hit-rate from real eval | Pass |
| AC-ML-02 | Citation / faithfulness documented | Pass |
| AC-RAG-01 | `/v1/ask` citations | Pass |
| AC-API-01–05 | API surface | Pass |
| AC-GIT-01 | Conventional commits + LICENSE | Pass |

## 8. Sign-off

| Role | Name | Date | OK? |
|------|------|------|-----|
| Author | Satyam Swain | 2026-07-26 | **Released** — implementation + presentation complete |

## 9. Decisions locked

Release acceptance closed for v1.0 on the sample-corpus demo path. Enterprise pgvector Compose remains the documented production persistence option.
