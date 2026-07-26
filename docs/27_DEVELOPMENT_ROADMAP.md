# 27 — Development Roadmap

| Field | Value |
|-------|--------|
| Status | Ready · Phases 0–5 complete |
| Project | Enterprise Document Intelligence Platform |
| Project status | **Released** · Version 1.0 · Scope Frozen |
| Last updated | 2026-07-26 |

## 1. Phases

| Phase | Name | Outcome |
|-------|------|---------|
| 0 | Design documentation | Specs Ready — done |
| 1 | Scaffold + persistence | Package layout, local store (+ optional Postgres path) — done |
| 2 | Document processing | Extract, chunk, embed, persist — done |
| 3 | Retrieval + RAG + extract | Search, ask with citations, structured extract — done |
| 4 | Evaluation + API polish | Harness, metrics, Swagger — done |
| 5 | Packaging + demo | CI, Docker, presentation, Released — done |

## 2. Backlog status

All Phase 0–5 checklist items for v1.0 are complete. See `docs/status.md` and `presentation/README.md`.

## 3. Honest implementation notes

- Default demo persistence: **local file-backed vector store** (CI-friendly).  
- Postgres/pgvector remains the enterprise Compose option documented in design docs.  
- Default answers: **extractive** unless `LLM_API_KEY` is set.

## 4. Next actions (post-release)

1. Record 90s demo video → `presentation/video/demo-90s.mp4`  
2. Push remote `enterprise-document-intelligence-platform` when ready  
3. Paste LinkedIn / Upwork copy from `presentation/copy/`  
