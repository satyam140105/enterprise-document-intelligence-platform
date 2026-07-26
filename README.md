# Enterprise Document Intelligence Platform

![Status](https://img.shields.io/badge/status-design_phase-yellow)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

**Mohammad Ahmadian — AI / Machine Learning Engineer**

Enterprise-Grade Intelligent Document Processing System powered by OCR, NLP and Large Language Models.

> **Status:** Design Phase · Version 1.0 · Scope Frozen · Current Phase: Software Design  
> Implementation has not started. Specs live under [`docs/`](docs/00_MASTER_INDEX.md).

## Recruiter snapshot

| Item | Detail |
|------|--------|
| Domain | Intelligent Document Processing (IDP) |
| Focus | OCR · document understanding · extraction · semantic search · RAG Q&A with citations |
| Target roles | Applied AI Engineer · LLM Engineer |
| Stack direction | Python · FastAPI · PostgreSQL/pgvector · HF embeddings · custom RAG · Docker |
| Docs | Full engineering pack `docs/00`–`28` (same DNA as Project 1) |

## What this platform will do

1. Ingest enterprise documents (PDF / TXT)  
2. Extract text (digital-first; OCR path for scans)  
3. Chunk → embed → store in pgvector  
4. Semantic search + citation-oriented RAG answers  
5. Configurable structured field extraction  
6. Evaluation harness (retrieval + answer quality checks)  
7. FastAPI delivery with OpenAPI docs  

## Documentation

Start here: [`docs/00_MASTER_INDEX.md`](docs/00_MASTER_INDEX.md) · [`docs/status.md`](docs/status.md)

| Notable docs | Purpose |
|--------------|---------|
| `01` PRD | Problem, goals, non-goals |
| `03` Architecture | System design |
| `10` API | Contract |
| `13` Document Processing Pipeline | IDP-specific (replaces classic FE doc from Project 1) |
| `28` Cursor Master Prompt | Implementation sessions |

## Repository layout (target)

```text
src/docintel/   ingestion · ocr · chunking · embeddings · retrieval · generation · evaluation · api
configs/        default.yaml
docs/           design pack (Ready)
presentation/   demo · architecture · dashboard · video · hiring copy (after implementation)
data/           raw / processed (gitignored content)
tests/          pytest
```

## Quick start (after implementation)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
set PYTHONPATH=src
uvicorn docintel.api.main:app --app-dir src --host 0.0.0.0 --port 8000
```

## Portfolio DNA

This repository follows the same standards as **Production ML Platform for Predictive Maintenance**:

- Same `/docs` numbering (with Project-2 swap: `13_DOCUMENT_PROCESSING_PIPELINE`)  
- Same repo hygiene, README pattern, demo/presentation pack pattern  
- Same packaging and Git conventional-commit discipline  

## Contact

mohammad.ahmadian.dev@gmail.com · [github.com/ahmadian-dev](https://github.com/ahmadian-dev) · Turkey (GMT+3)

## License

MIT — see [LICENSE](LICENSE).
