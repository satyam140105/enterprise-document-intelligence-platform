# 12 — Data Pipeline

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Version | 1.0 |

## 1. Pipeline stages

```text
acquire samples → validate type/size → persist document row →
text extract (doc 13) → chunk → embed → upsert pgvector →
mark ready → (optional) eval harness
```

## 2. Stage details

### Stage A — Acquire
- Place or script-assemble corpus into `data/samples/` / `data/raw/`  
- Output: files ready for ingest  

### Stage B — Validate
- Checks: allowed MIME/types (PDF, TXT); max size; non-empty file  
- On failure: reject with clear validation error (do not insert `ready` docs)

### Stage C — Persist metadata
- Insert `documents` row with `status=pending`  
- Store `source_path` / checksum when available  

### Stage D — Process (see doc 13)
- Extract → chunk → embed → write `chunks`  

### Stage E — Ready / failed
- Success: `status=ready`, chunk_count available  
- Failure: `status=failed`, `error_message` set  

### Stage F — Evaluate (offline)
- Run labeled retrieval / ask checklist  
- Write `reports/EVALUATION_REPORT.md`; log to MLflow when configured  

## 3. Idempotency

Re-ingesting the same checksum may update or skip per config (`ingest.dedupe`). Re-running embedding after model change requires explicit reindex command.

## 4. Pipeline entrypoints

| Entrypoint | Purpose |
|------------|---------|
| `POST /v1/ingest` | Online ingest path |
| `python -m docintel.ingest.cli` | Batch ingest samples |
| `python -m docintel.evaluation.run` | Offline eval |
| `scripts/prepare_sample_corpus.py` | Assemble/download samples |

## 5. Scheduling (v1)

Manual only (CLI / Makefile / Swagger). No cron or orchestrator.

## 6. Data quality metrics to log

| Metric | Where logged |
|--------|----------------|
| documents ready/failed counts | stdout + optional reports |
| chunks per document | DB + ingest response |
| mean chunk token estimate | optional eval report |
| retrieval hit-rate @k | `reports/EVALUATION_REPORT.md` + MLflow |

## 7. Decisions locked

Pipeline stages and entrypoints above are final for Design Phase v1. Document processing detail lives in doc 13.
