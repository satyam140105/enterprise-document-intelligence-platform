# 04 — Tech Stack

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Rule | Prefer unified portfolio stack; avoid unnecessary tools |
| Version | 1.0 |

## 1. Stack decisions

| Layer | Choice | Version (pin later) | Why |
|-------|--------|---------------------|-----|
| Language | Python | ≥3.11 | Portfolio standard |
| API | FastAPI + Uvicorn | pin in requirements | Serving + OpenAPI |
| Validation | Pydantic v2 | via FastAPI | Request/response contracts |
| Database | PostgreSQL + pgvector | pin image tag | Metadata + vectors |
| Embeddings | sentence-transformers / Hugging Face | pin model id in config | Semantic search |
| OCR / PDF | pdfplumber, pypdf; pytesseract optional | pin in requirements | Digital-first extraction |
| RAG | Custom thin orchestration | in-package | Not LangChain-heavy |
| LLM adapter | Configurable (local or API) | config | Generation for ask/extract |
| Tracking | MLflow | pin in requirements | Local `./mlruns` for eval |
| Containers | Docker + Compose | — | API + Postgres |
| CI | GitHub Actions | — | lint + pytest |
| Quality | pytest, ruff | pin | Portfolio DNA |
| Orchestration | Makefile + scripts | — | Keep simple |
| Demo UI | Swagger (`/docs`) | — | Primary; Streamlit later |

## 2. Explicitly out of stack (v1)

- LangChain / LlamaIndex as primary application framework  
- Kubernetes  
- Kafka / streaming ingest  
- Custom React frontend  
- Prompt-engineering “gallery” products  
- Claiming managed multi-region cloud as required  

## 3. Local toolchain

| Tool | Use |
|------|-----|
| git | Version control |
| pytest | Tests |
| ruff | Lint |
| make | Common tasks (`up`, `ingest`, `eval`, `serve`, `test`, `lint`) |
| uvicorn | Local API |
| docker compose | API + Postgres |

## 4. Dependency files

- `requirements.txt` — runtime + dev baseline  
- `pyproject.toml` — package metadata + pytest path  
- Lock file: pin versions in `requirements.txt` before public demo; optional `uv`/`pip-tools` later  

## 5. Environment matrix

| Env | Purpose | Notes |
|-----|---------|-------|
| local | Dev | `.venv`, Compose Postgres, MLflow `./mlruns` |
| ci | Tests | GitHub Actions; fixtures + optional service containers |
| demo | Recruiter demo | Compose up + sample corpus + Swagger |

## 6. Decisions locked

Python 3.11+, FastAPI, PostgreSQL + pgvector, HF embeddings, custom RAG, MLflow, Docker, pytest, ruff. No LangChain-heavy core. Swagger primary UI.
