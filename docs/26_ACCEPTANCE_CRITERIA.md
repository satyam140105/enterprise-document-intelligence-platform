# 26 — Acceptance Criteria

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Use | Gate for Design Phase docs freeze; later gate for implementation release |
| Version | 1.0 |

## 1. Documentation gates (Design Phase)

- [x] Docs in `00_MASTER_INDEX` marked Ready (Design Phase)  
- [x] No critical `[FILL]` left in PRD, Architecture, Dataset, Processing, Model, Evaluation, API  
- [x] Doc 13 titled Document Processing Pipeline (not feature engineering)  
- [x] `docs/status.md` shows Status: Design Phase · Version 1.0 · Scope: Frozen · Current Phase: Software Design  
- [ ] README quickstart works as written (verify after implementation)  

## 2. Functional gates (implementation — not started)

- [ ] Sample corpus prepared under `data/samples/`  
- [ ] Ingest accepts PDF/TXT and stores document + chunks  
- [ ] Embeddings written to pgvector  
- [ ] `POST /v1/search` returns ranked chunks  
- [ ] `POST /v1/ask` returns answer with citations  
- [ ] `POST /v1/extract` returns schema fields  
- [ ] Evaluation report produced under `reports/EVALUATION_REPORT.md`  
- [ ] API `GET /health` returns 200 with DB readiness  
- [ ] Invalid payload returns 422  

## 3. Quality gates

- [ ] `pytest` passes  
- [ ] `ruff check` passes  
- [ ] No secrets in git history  
- [ ] `.env.example` complete  

## 4. AI performance gates

| Criterion | Rule |
|-----------|------|
| Hit-rate @k computed | Required after eval — numbers only from real runs |
| Citations on demo asks | Required |
| Faithfulness checklist | Required for demo questions |
| Limitations documented | Required |
| Numeric scores hardcoded in docs | Forbidden — no invented scores |

## 5. MLOps / deploy gates

- [ ] MLflow run exists under `./mlruns` for final eval config (when eval executed)  
- [ ] Docker Compose brings up API + Postgres  
- [ ] Swagger demo path works  

## 6. Git / professionalism gates

- [ ] Conventional commits used  
- [ ] `main` history readable  
- [ ] LICENSE present  

## 7. Traceability IDs

| ID | Criterion |
|----|-----------|
| AC-DOC-01 | Docs Ready (Design Phase) + later evaluation report present |
| AC-PIPE-01 | Ingest → extract → chunk → embed path works |
| AC-ML-01 | Retrieval hit-rate computed from real eval |
| AC-ML-02 | Citation coverage / faithfulness checklist documented |
| AC-RAG-01 | `/v1/ask` returns citations |
| AC-API-01 | `/v1/ingest` works on sample |
| AC-API-02 | `/v1/search` 200 on valid query |
| AC-API-03 | `/v1/ask` 200 with citations |
| AC-API-04 | `/v1/extract` 200 on valid schema |
| AC-API-05 | `/health` 200 |
| AC-SEC-01 | Auth disabled for `API_KEY=change-me`; enforced otherwise |
| AC-GIT-01 | Conventional commits + LICENSE |

## 8. Sign-off

| Role | Name | Date | OK? |
|------|------|------|-----|
| Author | Mohammad Ahmadian | 2026-07-26 | Design Phase docs locked; implementation not started |

## 9. Decisions locked

Design Phase acceptance for documentation is complete. Implementation gates remain open until code exists.
