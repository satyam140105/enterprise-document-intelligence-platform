# 25 — Demo Specification

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Audience | Hiring managers / technical recruiters |
| Version | 1.0 |

## 1. Demo goals

In ≤ 3 minutes, show:
1. Clear problem framing (enterprise IDP: search, citable Q&A, extraction)  
2. Pipeline awareness (extract → chunk → embed → pgvector)  
3. Evaluation honesty (hit-rate + citation/faithfulness; metrics from report)  
4. Working API via Swagger (ingest / search / ask / extract)  

## 2. Demo formats

| Format | Required? |
|--------|-----------|
| Live API via Swagger | Yes (after implementation) |
| 90–180s silent video + captions | Optional |
| Screenshots in README | Yes (after implementation) |
| Notebook tour | No |
| Prompt gallery | No |

## 3. Demo script (captions)

1. Problem: turn sample documents into searchable, citable knowledge  
2. Stack: FastAPI, PostgreSQL + pgvector, HF embeddings, custom RAG (10s)  
3. Ingest a sample PDF/TXT (20s)  
4. Search → show scored chunks (20s)  
5. Ask → show answer **with citations** (40–60s)  
6. Extract → show structured fields for a schema (20s)  
7. Limitations: public/sample corpus; not production plant deployment (10s)  
8. Links: GitHub + docs (5s)  

## 4. Sample requests for live demo

```json
{
  "query": "What is the warranty period?",
  "top_k": 5
}
```

```json
{
  "question": "What is the warranty period?",
  "top_k": 5
}
```

```json
{
  "document_id": "<uuid from ingest>",
  "schema_name": "invoice_basic"
}
```

Expected: search results with scores; ask JSON with `answer` + `citations`; extract JSON with `fields`. Exact numeric scores depend on live index — see evaluation report for quality context after runs.

## 5. Assets checklist

- [ ] Swagger screenshots  
- [ ] Architecture diagram (from doc 03)  
- [ ] Evaluation report (real metrics only)  
- [ ] README quickstart  

## 6. Anti-patterns

- Demo without citations  
- Invented “98% accuracy” claims  
- Prompt-Engineer framing  
- Claiming regulated production deployment  

## 7. Decisions locked

Swagger-primary demo. Citations mandatory on ask. Honest limitations required.
