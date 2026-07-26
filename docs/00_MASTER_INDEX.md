# 00 — Master Index

| Field | Value |
|-------|--------|
| Project | Enterprise Document Intelligence Platform |
| Package | `docintel` |
| Repo | `enterprise-document-intelligence-platform` |
| Owner | Mohammad Ahmadian |
| Docs status | **All docs Ready (Design Phase)** |
| Project status | **Design Phase** (see `docs/status.md`) |
| Version | 1.0 |
| Scope | Frozen |
| Current Phase | Software Design |
| Last updated | 2026-07-26 |

## How to use these docs

1. Specs are locked for Design Phase — implement and review against numbered docs (01 → 28).  
2. Prefer these decisions over assumptions; update the owning doc in the same PR if a contract changes.  
3. Keep language precise and recruiter-readable — no hype.  
4. Metrics after evaluation: `reports/EVALUATION_REPORT.md` (do not invent numbers in docs).  
5. Coding sessions: start from `28_CURSOR_MASTER_PROMPT.md`.  
6. Implementation has **not** started; this set freezes scope before code.

## Document register

| ID | Document | Status | Owner fill priority |
|----|----------|--------|---------------------|
| 00 | Master Index (this file) | Ready (Design Phase) | Keep in sync |
| 01 | Product Requirements (PRD) | Ready (Design Phase) | P0 |
| 02 | Software Design Specification | Ready (Design Phase) | P0 |
| 03 | System Architecture | Ready (Design Phase) | P0 |
| 04 | Tech Stack | Ready (Design Phase) | P0 |
| 05 | Feature Specification | Ready (Design Phase) | P0 |
| 06 | User Stories | Ready (Design Phase) | P1 |
| 07 | User Flow | Ready (Design Phase) | P1 |
| 08 | UI/UX Specification | Ready (Design Phase) | P2 |
| 09 | Database Design | Ready (Design Phase) | P0 |
| 10 | API Specification | Ready (Design Phase) | P0 |
| 11 | Dataset Strategy | Ready (Design Phase) | P0 |
| 12 | Data Pipeline | Ready (Design Phase) | P0 |
| 13 | Document Processing Pipeline | Ready (Design Phase) | P0 |
| 14 | Model Development | Ready (Design Phase) | P0 |
| 15 | Model Evaluation | Ready (Design Phase) | P0 |
| 16 | MLOps Pipeline | Ready (Design Phase) | P1 |
| 17 | Monitoring & Observability | Ready (Design Phase) | P1 |
| 18 | Security | Ready (Design Phase) | P1 |
| 19 | Testing Strategy | Ready (Design Phase) | P1 |
| 20 | Deployment | Ready (Design Phase) | P1 |
| 21 | Project Structure | Ready (Design Phase) | P0 |
| 22 | Coding Standards | Ready (Design Phase) | P1 |
| 23 | Git Workflow | Ready (Design Phase) | P0 |
| 24 | Documentation Standard | Ready (Design Phase) | P1 |
| 25 | Demo Specification | Ready (Design Phase) | P1 |
| 26 | Acceptance Criteria | Ready (Design Phase) | P0 |
| 27 | Development Roadmap | Ready (Design Phase) | P0 |
| 28 | Cursor Master Prompt | Ready (Design Phase) | P0 |

## Definition of “docs complete” (Design Phase)

- [x] All P0 docs marked Ready (Design Phase)  
- [x] No unresolved `[FILL]` in locked specs  
- [x] Architecture overview in doc 03  
- [x] Acceptance criteria testable (doc 26)  
- [x] Project status documented (`docs/status.md` = Design Phase · Scope Frozen)  
- [ ] Implementation started (not yet)

## Related brand context

Target roles: **Applied AI Engineer**, **LLM Engineer**  
Portfolio presentation goal: enterprise-grade Intelligent Document Processing (OCR/NLP/LLM, custom RAG, evaluation, API, MLOps) — not prompt-demo-only, not notebook-only  
README subtitle concept: Enterprise-Grade Intelligent Document Processing System powered by OCR, NLP and Large Language Models
