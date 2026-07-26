# 27 — Development Roadmap

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Project | Enterprise Document Intelligence Platform |
| Project status | **Design Phase** · Version 1.0 · Scope Frozen · Current Phase: Software Design |
| Last updated | 2026-07-26 |

## 1. Phases

| Phase | Name | Outcome |
|-------|------|---------|
| 0 | Design documentation | Specs Ready (Design Phase) — **current** |
| 1 | Scaffold + database | Package layout, Compose Postgres, migrations |
| 2 | Document processing | Extract, chunk, embed, persist |
| 3 | Retrieval + RAG + extract | Search, ask with citations, structured extract |
| 4 | Evaluation + API polish | Harness, MLflow, Swagger completeness |
| 5 | Packaging + demo | CI, Docker polish, README demo, tag v0.1.0 |

## 2. Detailed backlog

### Phase 0 — Documentation (complete)
- [x] Fill 01 PRD  
- [x] Fill 04 Tech Stack decisions  
- [x] Fill 09 Database Design (pgvector)  
- [x] Fill 11 Dataset Strategy  
- [x] Fill 13 Document Processing Pipeline  
- [x] Fill 14–15 Model + Evaluation  
- [x] Fill 10 API schema  
- [x] Fill 26 Acceptance criteria  
- [x] Mark all docs Ready (Design Phase) in 00  
- [x] Create `docs/status.md` = Design Phase · Scope Frozen  

### Phase 1 — Scaffold + database
- [ ] Create `src/docintel` package layout  
- [ ] `pyproject.toml`, requirements, Makefile  
- [ ] Docker Compose Postgres + pgvector  
- [ ] Migrations for `documents` / `chunks`  
- [ ] Health endpoint + DB readiness  

### Phase 2 — Document processing
- [ ] Ingest API + CLI  
- [ ] PDF/TXT extraction (digital-first)  
- [ ] Optional OCR flag path  
- [ ] Chunking strategies (`fixed_tokens`, `recursive`)  
- [ ] Embeddings + pgvector upsert  
- [ ] Unit tests for chunking/extract  

### Phase 3 — Search, RAG, extract
- [ ] Semantic search endpoint  
- [ ] Thin custom RAG ask + citations  
- [ ] Schema-driven extract  
- [ ] Insufficient-context behavior  
- [ ] API tests  

### Phase 4 — Evaluation
- [ ] Labeled query fixtures  
- [ ] Hit-rate @k harness  
- [ ] Citation coverage + faithfulness checklist  
- [ ] MLflow logging  
- [ ] `reports/EVALUATION_REPORT.md` with real metrics only  

### Phase 5 — Release polish
- [ ] GitHub Actions CI  
- [ ] Demo assets (doc 25)  
- [ ] README final  
- [ ] Tag `v0.1.0`  
- [ ] Update `docs/status.md` when presenting as Released  

## 3. Suggested calendar

| Week | Focus |
|------|--------|
| Week 0 | Phase 0 docs (done 2026-07-26) |
| Week 1 | Phase 1–2 scaffold + processing |
| Week 2 | Phase 3 retrieval / RAG / extract |
| Week 3 | Phase 4–5 evaluation, CI, demo |

## 4. Dependencies / blockers

| Blocker | Owner | Status |
|---------|-------|--------|
| Sample corpus licenses | Mohammad Ahmadian | Confirm at Phase 2 |
| No LangChain-heavy core / Swagger-primary | Locked | Confirmed |
| Scope Frozen (Design Phase) | Locked | Confirmed |

## 5. Next action

1. Begin Phase 1 implementation using `28_CURSOR_MASTER_PROMPT.md`  
2. Keep docs in sync if contracts change  
3. Write real metrics only to `reports/EVALUATION_REPORT.md` after evaluation  

## 6. Decisions locked

Roadmap above is the Design Phase plan. Implementation has not started.
