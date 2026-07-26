# 01 — Product Requirements Document (PRD)

| Field | Value |
|-------|--------|
| Product name | Enterprise Document Intelligence Platform |
| Status | Ready (Design Phase) |
| Version | 1.0 |
| Author | Mohammad Ahmadian |
| Date | 2026-07-26 |
| Scope | Frozen |
| Current Phase | Software Design |

## 1. Problem statement

Organizations accumulate PDFs and text documents that are hard to search, query, and extract structured fields from at scale. Manual review is slow; keyword search misses semantic matches; ad-hoc LLM prompts lack citations, evaluation, and a reproducible serving path.

**Pain today:**  
Scattered files, weak semantic retrieval, answers without provenance, and no honest evaluation of retrieval or grounded generation.

**Desired outcome:**  
An Intelligent Document Processing (IDP) system that ingests PDF/TXT, extracts text, chunks and embeds content into PostgreSQL + pgvector, supports semantic search and RAG Q&A with citations, extracts configurable structured fields, and exposes a documented FastAPI surface — with an evaluation harness for retrieval hit-rate and citation coverage / faithfulness checklist.

## 2. Product vision

> An enterprise-oriented document intelligence platform that turns a public/sample corpus into searchable, citable knowledge via OCR/NLP, sentence-transformer embeddings, custom RAG orchestration, and FastAPI services — with MLflow-tracked evaluation where relevant.

## 3. Goals & non-goals

### Goals
- Ingest PDF and TXT documents into a durable store  
- Extract text (digital PDF first; optional OCR path for scans)  
- Chunk, embed (Hugging Face / sentence-transformers), and index in pgvector  
- Semantic search over chunks  
- RAG Q&A with source citations  
- Structured field extraction against a configurable schema  
- Evaluation harness: retrieval hit-rate + answer citation coverage / faithfulness checklist  
- FastAPI: `health`, `ingest`, `search`, `ask`, `extract`  
- Demonstrate production AI practices: config-driven pipelines, Docker, pytest, ruff, GitHub Actions, MLflow for eval/experiment tracking  

### Non-goals (explicitly out of scope for v1)
- Claiming production plant / regulated enterprise deployment  
- LangChain-heavy orchestration (thin custom RAG only)  
- Prompt-Engineer positioning or prompt-gallery demos  
- Full DMS / SharePoint replacement or multi-tenant SaaS  
- Real-time collaborative editing or e-signature workflows  
- Custom React UI (Swagger primary; Streamlit optional later)  
- Fine-tuning large proprietary LLMs as a v1 requirement  

## 4. Target users

| Persona | Role | Needs |
|---------|------|--------|
| P-Analyst | Knowledge / operations analyst | Search documents; ask questions with citations; extract fields |
| P-AI | Applied AI / LLM engineer | Reproducible ingest→RAG→eval path; honest metrics |
| P-Ops | Platform / integrator | Health endpoint, OpenAPI contract, Docker Compose |
| P-HM | Hiring manager | Architecture, evaluation honesty, runnable demo |

## 5. Success metrics (product)

| Metric | Definition | Target (v1) |
|--------|------------|-------------|
| Retrieval quality | Hit-rate @k on labeled query set | Documented in `reports/EVALUATION_REPORT.md` after eval runs — no invented numbers |
| Answer grounding | Citation coverage / faithfulness checklist | Documented after eval; checklist must pass for demo queries |
| API usability | OpenAPI + working paths | Recruiter can call ingest/search/ask/extract from Swagger |
| Reproducibility | Seeded config + MLflow where used | Same config yields logged params/metrics under `./mlruns` |
| Latency (local) | Search / ask interactive | Suitable for interactive demo (no hard SLA; log latency) |

## 6. Problem framing

| Item | Decision |
|------|----------|
| Domain | Intelligent Document Processing (IDP) |
| Primary tasks | Semantic retrieval; RAG Q&A with citations; structured extraction |
| Corpus | Public / sample documents only (see doc 11) |
| Citation policy | Answers must reference retrieved chunk IDs / document IDs |
| Honesty | No production plant claims; limitations documented |

## 7. Constraints

| Constraint | Detail |
|------------|--------|
| Data | Public/sample corpus; license attribution required |
| Latency | Local single-instance API + PostgreSQL; no multi-region SLA |
| Privacy / compliance | No real customer PII in public repo; sample docs only |
| Cloud | Local Docker Compose first; no required cloud vendor |
| Budget | Portfolio project — lean, unified portfolio stack |
| Positioning | Applied AI / LLM Engineer — not Prompt Engineer |

## 8. Assumptions

1. Digital PDFs are the primary path; scanned OCR via pytesseract is optional and may be limited in v1.  
2. Embeddings use a documented sentence-transformers / HF model from config.  
3. Generation uses a configurable local or API LLM adapter; thin custom orchestration wraps retrieve → prompt → cite.  
4. Auth may stay disabled for local demo when `API_KEY=change-me`.  
5. PostgreSQL + pgvector is required for v1 vector storage.  

## 9. Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Hallucinated answers without citations | High | Force citation objects; faithfulness checklist in eval |
| Poor chunking → weak retrieval | High | Document chunk strategies; evaluate hit-rate @k |
| OCR quality on scans | Medium | Digital-first v1; optional OCR path clearly labeled |
| Overclaiming production readiness | High | Explicit limitations in README + evaluation docs |
| LangChain sprawl | Medium | Custom thin RAG modules only |

## 10. Release definition (portfolio v1 — after implementation)

A hiring manager can:
1. Read architecture + evaluation docs  
2. Run ingest → search → ask → extract from README / Swagger  
3. See citations on ask responses  
4. Review evaluation report with real metrics (not invented)  
5. See MLflow run history under `./mlruns` where applicable  

**Current project status:** Design Phase · Scope Frozen (see `docs/status.md`). Implementation not started.

## 11. Decisions locked

All product decisions for Design Phase v1 are locked in this PRD and sibling docs 02–28. Scope is frozen until an explicit scope-change updates these docs.
