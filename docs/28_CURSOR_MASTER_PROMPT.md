# 28 — Cursor Master Prompt

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Purpose | Paste into Cursor when implementing this repo |
| Version | 1.0 |

---

## Master prompt (copy below)

```text
You are implementing the portfolio project:
Enterprise Document Intelligence Platform
Repo: enterprise-document-intelligence-platform
Package: docintel
Owner: Satyam Swain (AI / Machine Learning Engineer)
Target roles: Applied AI Engineer, LLM Engineer
README subtitle concept: Enterprise-Grade Intelligent Document Processing System powered by OCR, NLP and Large Language Models

PROJECT STATUS
Design Phase · Version 1.0 · Scope Frozen · Current Phase: Software Design
Implementation has NOT started unless this session explicitly begins Phase 1+.
Progression: Design Phase → Phase 1 Scaffold/DB → Phase 2 Document Processing → Phase 3 Retrieval/RAG/Extract → Phase 4 Evaluation → Phase 5 Packaging/Demo → Released.

LOCKED DECISIONS (do not reopen without updating docs)
- Domain: Intelligent Document Processing (IDP)
- Ingest: PDF + TXT
- Extraction: pdfplumber/pypdf digital-first; pytesseract optional for scans
- Chunking: documented strategies (fixed_tokens, recursive; page optional) via config
- Embeddings: sentence-transformers / Hugging Face (NOT LangChain-heavy)
- Store: PostgreSQL + pgvector
- RAG: thin custom orchestration (retrieve → pack → generate → cite)
- Features: semantic search; RAG Q&A with citations; structured field extraction (configurable schemas)
- Evaluation: retrieval hit-rate @k + citation coverage / faithfulness checklist
- Tracking: MLflow local ./mlruns where relevant
- API: FastAPI — GET /health, POST /v1/ingest, POST /v1/search, POST /v1/ask, POST /v1/extract
- Auth: optional X-API-Key; disabled when API_KEY=change-me
- UI: Swagger primary; Streamlit optional later
- Deploy: local uvicorn + Docker Compose (API + Postgres)
- Stack: Python 3.11+, FastAPI, PostgreSQL+pgvector, HF embeddings, MLflow, Docker, pytest, ruff, GitHub Actions
- NO Prompt-Engineer positioning
- NO LangChain as core framework
- Corpus: public/sample only — do NOT claim production plant deployment
- Do NOT invent metric numbers — write them to reports/EVALUATION_REPORT.md after eval runs
- Tone: professional, technical, enterprise, no hype

CRITICAL RULES
1. Read and obey docs in /docs. Prefer filled specs over assumptions.
2. Do not invent product behavior that contradicts Ready (Design Phase) docs; update docs in the same change if a contract must change.
3. Do not commit secrets, proprietary customer PDFs, or large binaries.
4. Use conventional commits (feat/fix/docs/test/chore/refactor/build/perf).
5. Keep ingest/process/retrieve/serve separation. Config-driven via configs/default.yaml.
6. Ask responses must include citation structures.
7. Write/update tests for new behavior. Keep ruff-clean.
8. Update docs in the same change when API/processing/metric contracts change.
9. Code quality should impress hiring managers: clear structure, honest metrics, readable git history.

CURRENT PHASE
Phase 0 — Design docs complete. Next: Phase 1 (scaffold + database) unless the session task says otherwise.

TASK FOR THIS SESSION
[exact task, e.g. “Scaffold src/docintel + docker-compose Postgres/pgvector per docs/09 and docs/21”]

DONE MEANS
- Code matches relevant docs
- Tests added/updated (once code phase starts)
- README commands still accurate when touched
- Suggest a conventional commit message (do not commit unless I ask)

OUT OF SCOPE THIS SESSION
[list anything not to touch]
```

---

## Session prompt templates

### A) Scaffold + database (Phase 1)
```text
Implement Phase 1 per docs/09, 20, 21. Create src/docintel package, docker-compose with pgvector Postgres, migrations for documents/chunks, GET /health with database readiness. No RAG yet. Propose conventional commit message when done.
```

### B) Document processing (Phase 2)
```text
Implement Phase 2 per docs/12–13. Digital-first PDF/TXT extraction, fixed_tokens + recursive chunking, HF embeddings, pgvector upsert, POST /v1/ingest. Optional OCR behind config flag. Add unit tests. No ask/extract yet unless needed for smoke.
```

### C) Search + RAG + extract (Phase 3)
```text
Implement Phase 3 per docs/10 and docs/05. POST /v1/search, POST /v1/ask with citations (thin custom RAG), POST /v1/extract with configs/schemas. Insufficient-context behavior required. Swagger examples. Tests for validation + citations field.
```

### D) Evaluation + polish (Phase 4–5)
```text
Implement evaluation per docs/15–16 and packaging per docs/19–20. Hit-rate @k + citation/faithfulness checklist. Log to ./mlruns. Write reports/EVALUATION_REPORT.md with real metrics only. Add GitHub Actions lint/pytest. Do not invent scores.
```

---

## Agent checklist before finishing a session

- [ ] Specs consulted  
- [ ] No unexplained new dependencies  
- [ ] No LangChain-heavy core introduced  
- [ ] No Prompt-Engineer framing  
- [ ] Tests run (or explain why not)  
- [ ] Commit message proposed  
- [ ] Open questions listed only if docs must change  

## Locked answers (do not ask again)

- Stack locked in doc 04 (FastAPI, Postgres+pgvector, HF embeddings, custom RAG)  
- API surface locked in doc 10  
- Doc 13 is Document Processing Pipeline (not feature engineering)  
- Auth locked (`change-me` disables)  
- Swagger-primary UI; Streamlit optional later  
- Sample/public corpus only; no fake production metrics  
- Status: Design Phase until implementation milestones complete and status.md is updated  
