# LinkedIn Project — Paste Ready

## Project name
```
Enterprise Document Intelligence Platform
```

## Description

```
Status: Released · Flagship Portfolio Project

Enterprise-grade intelligent document processing (IDP) platform for OCR/text extraction, semantic search, RAG Q&A with citations, and structured field extraction.

Scope:
• Ingest PDF/TXT (digital-first extraction)
• Chunking + sentence-transformers embeddings
• Semantic retrieval with cosine similarity
• RAG answers with chunk citations (extractive default; optional LLM)
• Configurable field extraction
• Evaluation: retrieval hit-rate, citation coverage, faithfulness checklist
• FastAPI (/health, /v1/ingest, /v1/search, /v1/ask, /v1/extract)
• Docker + CI + full engineering docs

Eval (sample corpus):
• Retrieval hit-rate@5: 1.00
• Citation coverage: 1.00
• Faithfulness checklist: 1.00

Target roles: Applied AI Engineer, LLM Engineer

Stack: Python · FastAPI · sentence-transformers · custom RAG · MLflow · Docker

Limitations documented: public/sample corpus; not a production plant archive.

GitHub: github.com/ahmadian-dev/enterprise-document-intelligence-platform
```
