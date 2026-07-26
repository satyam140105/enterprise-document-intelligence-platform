# 06 — User Stories

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Format | As a … I want … so that … |
| Version | 1.0 |

## Personas (short)

- **P-Analyst:** Knowledge / operations analyst  
- **P-AI:** Applied AI / LLM engineer  
- **P-Ops:** Someone deploying the API  
- **P-HM:** Hiring manager reviewing the repo (meta)

---

## Stories

### US-01 — Ingest documents
**As a** P-Analyst  
**I want** to upload PDF/TXT documents  
**So that** they become searchable knowledge  

**Acceptance pointers:** AC-API-01, AC-PIPE-01 (doc 26)

### US-02 — Semantic search
**As a** P-Analyst  
**I want** to search by meaning, not only keywords  
**So that** I find relevant passages quickly  

**Acceptance pointers:** AC-API-02

### US-03 — Ask with citations
**As a** P-Analyst  
**I want** answers grounded in retrieved chunks with citations  
**So that** I can verify claims  

**Acceptance pointers:** AC-API-03, AC-RAG-01

### US-04 — Extract structured fields
**As a** P-Analyst  
**I want** configurable field extraction from a document  
**So that** I can populate structured records  

**Acceptance pointers:** AC-API-04

### US-05 — Evaluate retrieval & grounding
**As a** P-AI  
**I want** a reproducible evaluation harness for hit-rate and citation/faithfulness checks  
**So that** I avoid demo theater  

**Acceptance pointers:** AC-ML-01, AC-ML-02

### US-06 — Serve via OpenAPI
**As a** P-Ops / integrator  
**I want** a documented REST API with examples  
**So that** other systems can integrate  

**Acceptance pointers:** AC-API-01 … AC-API-05

### US-07 — Health check
**As a** P-Ops  
**I want** `GET /health`  
**So that** orchestration can probe liveness and dependency readiness  

**Acceptance pointers:** AC-API-05

### US-08 — Recruiter review
**As a** P-HM  
**I want** clear docs, architecture, and honest evaluation  
**So that** I can assess Applied AI / LLM engineering quality  

**Acceptance pointers:** AC-DOC-01, AC-GIT-01

### US-09 — Optional API protection
**As a** P-Ops  
**I want** optional `X-API-Key` auth that defaults off for local demo (`API_KEY=change-me`)  
**So that** shared demos can be locked without blocking local development  

**Acceptance pointers:** AC-SEC-01

---

## Story → feature map

| Story | Features |
|-------|----------|
| US-01 | F01, F13 |
| US-02 | F07, F14 |
| US-03 | F08, F15 |
| US-04 | F09, F16 |
| US-05 | F10, F11 |
| US-06 | F13–F16 |
| US-07 | F12 |
| US-08 | docs + F10 |
| US-09 | F17 |
