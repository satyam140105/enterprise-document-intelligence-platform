# 16 — MLOps Pipeline

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Scope | Portfolio-grade MLOps (practical, not enterprise theater) |
| Version | 1.0 |

## 1. MLOps capabilities in v1

| Capability | In v1? | How |
|------------|--------|-----|
| Experiment tracking | Yes | MLflow local `./mlruns` for eval configs |
| Reproducible configs | Yes | YAML + pinned model ids |
| Artifact versioning | Yes | embedding model id + chunk strategy + prompt versions |
| Model registry | Manual | Document selected demo config in reports |
| CI tests | Yes | GitHub Actions: ruff + pytest |
| CD auto-deploy | No | Manual Docker Compose |
| Feature store | No | |
| Online drift service | Light | schema/422 logging only (doc 17) |

## 2. Offline eval pipeline (batch)

```text
checkout → setup python → install deps →
compose up db → ingest samples →
run evaluation → log mlflow →
write reports/EVALUATION_REPORT.md
```

## 3. Promotion rules (manual is OK)

| Stage | Criteria |
|-------|----------|
| Demo config | Passes tests + evaluation gates (doc 26) |
| Serving config | Manual: env/config points to selected embedding + LLM settings |

## 4. Environments

| Env | Tracking URI | Notes |
|-----|--------------|-------|
| local | `./mlruns` | Compose Postgres |
| demo | `./mlruns` or baked report only | Sample corpus |

## 5. CI jobs (planned)

| Job | Trigger | Steps |
|-----|---------|-------|
| `lint-test` | PR / push | ruff, pytest |
| `eval-smoke` | `workflow_dispatch` / optional | tiny fixture retrieval smoke |

## 6. Rollback

Revert config to previous embedding/chunk settings and reindex if needed; restart API container. Keep prior evaluation report for comparison.

## 7. Decisions locked

Local MLflow only for Design Phase v1. No remote tracking server required for demo.
