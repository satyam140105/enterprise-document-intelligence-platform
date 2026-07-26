# 13 — Document Processing Pipeline

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Note | This is **not** classical feature engineering — it is IDP text processing |
| Version | 1.0 |

## 1. Purpose

Convert ingested PDF/TXT into clean text, chunks, and embeddings suitable for semantic search, RAG citations, and structured extraction.

## 2. End-to-end stages

```text
bytes → detect type → extract text → normalize →
chunk (strategy) → embed → persist chunks + vectors →
ready for search / ask / extract
```

## 3. Text extraction

### Digital PDF / TXT (primary)
| Tool | Use |
|------|-----|
| pdfplumber | Preferred for digital PDFs with text layers |
| pypdf | Fallback / simple extraction |
| native UTF-8 read | TXT files |

### Scanned PDF / images (optional)
| Tool | Use |
|------|-----|
| pytesseract | Optional OCR path when text layer missing |

**v1 stance:** Digital-first. OCR may be disabled by default in config (`ocr.enabled: false`). When enabled, mark quality as best-effort in logs and docs.

## 4. Normalization

- Unicode normalize; strip null bytes  
- Collapse excessive whitespace while preserving paragraph breaks when possible  
- Record `page_count` when available  
- Do not silently invent missing pages  

## 5. Chunking strategies (documented)

| Strategy id | Description | Typical config |
|-------------|-------------|----------------|
| `fixed_tokens` | Fixed token window with overlap | `chunk_size`, `overlap` |
| `recursive` | Paragraph/sentence-aware recursive split | `chunk_size`, `overlap`, separators |
| `page` | One chunk per page (PDF) | page boundaries |

**Rules:**
- Strategy selected via `configs/default.yaml`  
- Persist `strategy` on each chunk row  
- Keep chunk text sufficient for citation snippets  
- Avoid tiny fragments that destroy retrieval  

## 6. Embeddings

| Item | Decision |
|------|----------|
| Library | sentence-transformers / Hugging Face |
| Model | Configured model id (pin in config; document in README when chosen) |
| Input | Chunk text |
| Output | Fixed-dim vector → pgvector |
| Versioning | Store `embedding_model` on chunk; reindex on model change |

## 7. Persistence contract

Each successful chunk write includes: `document_id`, `chunk_index`, `text`, optional page range, `strategy`, `embedding`, `embedding_model`.

## 8. Failure modes

| Failure | Behavior |
|---------|----------|
| Empty extraction | Mark document `failed` |
| OCR unavailable when required | Fail with actionable message |
| Embedding model load error | Fail processing; API may report 503 on dependent routes |
| Partial chunk write | Prefer transactional cleanup or compensating delete of partial chunks |

## 9. Alignment with search / RAG

- Search embeds the query with the **same** model used for chunks  
- Ask uses retrieved chunk texts as citation sources  
- Extract may use full document text and/or top chunks depending on schema size  

## 10. Decisions locked

Digital-first extraction, documented chunk strategies, HF embeddings, pgvector persistence. No LangChain document loaders as the core processing path.
