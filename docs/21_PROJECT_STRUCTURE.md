# 21 — Project Structure

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Note | Canonical layout for `enterprise-document-intelligence-platform` |
| Version | 1.0 |

## 1. Canonical layout

```text
enterprise-document-intelligence-platform/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── requirements.txt
├── pyproject.toml
├── Makefile
├── Dockerfile
├── docker-compose.yml
├── migrations/              # SQL or Alembic
├── configs/
│   ├── default.yaml
│   ├── prompts/
│   ├── schemas/
│   └── experiments/
├── data/
│   ├── raw/                 # gitignored if large
│   ├── samples/             # tiny demo corpus
│   ├── eval/                # labeled queries
│   └── README.md
├── notebooks/               # exploration only — not source of truth
├── src/docintel/
│   ├── __init__.py
│   ├── ingest/
│   ├── processing/          # extract, chunk, normalize
│   ├── embeddings/
│   ├── store/               # postgres + pgvector
│   ├── retrieval/
│   ├── rag/
│   ├── extraction/
│   ├── evaluation/
│   └── api/
├── tests/
│   └── fixtures/
├── scripts/
│   └── prepare_sample_corpus.py
├── docs/                    # this documentation set + status.md
├── reports/
│   ├── figures/
│   ├── metrics/
│   └── EVALUATION_REPORT.md
└── mlruns/                  # gitignored local MLflow
```

## 2. Module responsibilities

| Path | Responsibility |
|------|----------------|
| `docintel.ingest` | accept files, create document rows, orchestrate processing |
| `docintel.processing` | text extraction, OCR optional, chunking, normalization |
| `docintel.embeddings` | HF / sentence-transformers encode |
| `docintel.store` | PostgreSQL + pgvector access |
| `docintel.retrieval` | semantic search |
| `docintel.rag` | thin custom retrieve→generate→cite |
| `docintel.extraction` | schema-driven field extraction |
| `docintel.evaluation` | hit-rate + citation/faithfulness harness |
| `docintel.api` | FastAPI app, schemas, auth |

## 3. What must not live in git

- `.env`, large corpora, secrets, heavy `mlruns/` dirs, proprietary customer PDFs  

## 4. Planned packaging

| Path | When |
|------|------|
| `Dockerfile` / `docker-compose.yml` | Serving / demo |
| `.github/workflows/ci.yml` | lint + pytest |
| `notebooks/00_explore.ipynb` | optional exploration only |

## 5. Decisions locked

Package name `docintel` under `src/`. PostgreSQL + pgvector required. No LangChain-centric package layout. Implementation not started.
