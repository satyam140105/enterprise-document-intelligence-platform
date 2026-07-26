# 24 — Documentation Standard

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Version | 1.0 |

## 1. Principles

1. Docs precede non-trivial code  
2. One concern per file (see 00–28 set)  
3. Recruiter-readable English; short sentences  
4. Status header on every doc  
5. No hype adjectives  
6. No fabricated metric numbers — point to `reports/EVALUATION_REPORT.md`  
7. No Prompt-Engineer positioning  

## 2. Status values

| Status | Meaning |
|--------|---------|
| Draft — fill me | Template incomplete (should not remain) |
| Ready (Design Phase) | Decisions filled; guides implementation |
| Ready | Decisions filled (generic) |
| Implemented | Matches code |
| Deprecated | Superseded — leave note |
| Design Phase / Released | Project presentation status (`docs/status.md`) |

## 3. `[FILL]` convention

- Replace all `[FILL]` before marking Ready (Design Phase)  
- This documentation set is **Ready (Design Phase)** with locked decisions  
- Implementation has **not** started  

## 4. Diagrams

- Prefer SVG/PNG under `docs/assets/`  
- Always caption with date + status  
- Keep Mermaid/text diagrams in markdown when simple  

## 5. Sync rules

When code changes a contract (API, chunking, metrics):
1. Update the owning doc in the **same PR**  
2. Bump “Last updated” in `00_MASTER_INDEX.md`  

## 6. README vs /docs

| Surface | Content |
|---------|---------|
| README | Short pitch, quickstart, status, links |
| `/docs` | Full specifications |
| `docs/status.md` | Single source of project status for portfolio |

## 7. Language

- American English  
- Glossary: IDP = Intelligent Document Processing; RAG = retrieval-augmented generation; hit-rate @k = retrieval primary metric  

## 8. Brand tone

Professional, technical, enterprise. No hype. Accurate status labels only. Target roles: Applied AI Engineer, LLM Engineer.
