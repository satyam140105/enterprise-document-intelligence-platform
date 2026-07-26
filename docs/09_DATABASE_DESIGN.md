# 09 — Database Design

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| v1 decision | **PostgreSQL + pgvector** |
| Version | 1.0 |

## 1. Decision

Does v1 need a database?

| Choice | When |
|--------|------|
| No DB | Insufficient for durable vectors + metadata demo |
| SQLite + files | Weak vector story for this portfolio accent |
| **PostgreSQL + pgvector** | Selected — documents, chunks, embeddings |

**Selected:** PostgreSQL + pgvector.

## 2. Storage layout (files + DB)

| Path / store | Contents |
|--------------|----------|
| `data/raw/` | Optional local originals (gitignored if large) |
| `data/samples/` | Tiny committed sample corpus for demo/CI |
| `data/eval/` | Labeled queries for evaluation (committed fixtures OK) |
| PostgreSQL | `documents`, `chunks`, embeddings via pgvector |
| `reports/` | Evaluation narratives and metrics JSON |
| `mlruns/` | MLflow local tracking (gitignored) |

## 3. Relational model

### `documents`
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | `document_id` |
| filename | TEXT | Original name |
| content_type | TEXT | `application/pdf` / `text/plain` |
| status | TEXT | `pending` / `processing` / `ready` / `failed` |
| source_path | TEXT | Storage path |
| page_count | INT NULL | When applicable |
| checksum | TEXT NULL | Optional integrity |
| error_message | TEXT NULL | On failure |
| created_at | TIMESTAMPTZ | Default now() |
| updated_at | TIMESTAMPTZ | Default now() |

### `chunks`
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | `chunk_id` |
| document_id | UUID FK | → documents.id |
| chunk_index | INT | Order within document |
| text | TEXT | Chunk content |
| page_start | INT NULL | Optional |
| page_end | INT NULL | Optional |
| token_estimate | INT NULL | Approx |
| strategy | TEXT | Chunking strategy name |
| embedding | VECTOR(dim) | pgvector; dim from config |
| embedding_model | TEXT | Model id used |
| created_at | TIMESTAMPTZ | Default now() |

**Indexes:** IVFFlat or HNSW on `embedding` (choose one in implementation; document choice in migration notes). B-tree on `document_id`, `status`.

### Optional `ingestion_jobs` (if useful)
Deferred unless needed; document status fields may suffice for v1.

## 4. ER diagram

```text
documents 1───* chunks
                 │
                 └── embedding vector(dim)
```

## 5. Migrations

Tool: SQL migrations under `migrations/` or Alembic (prefer simple SQL for portfolio clarity unless Alembic already fits).  
Strategy: versioned up scripts; Compose applies on first boot.

## 6. Embedding dimension policy

`dim` is locked by the selected embedding model in config. Changing models requires re-embed + migration or new column/version tag. Never mix dimensions in one column without a version strategy.

## 7. Decisions locked

PostgreSQL + pgvector with `documents` and `chunks` is the Design Phase persistence model. No Mongo/FAISS-only primary store.
