# 20 — Deployment

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Version | 1.0 |

## 1. Deployment targets

| Target | In v1? |
|--------|--------|
| Local uvicorn + local/Compose Postgres | Yes |
| Docker Compose (API + Postgres) | Yes |
| Cloud (Railway/Render/AWS) | Optional later — not required for Design Phase |
| Kubernetes | No |

## 2. Local run

```bash
export PYTHONPATH=src
# ensure DATABASE_URL and model configs are set
uvicorn docintel.api.main:app --host 0.0.0.0 --port 8000
```

Preferred demo path: `docker compose up` (API + pgvector Postgres).

## 3. Docker

**Dockerfile goals:**
- Python 3.11-slim  
- Install deps  
- Copy `src`, configs  
- Expose 8000  
- Non-root user: yes (preferred)

**Compose goals:**
- `db` service: PostgreSQL with pgvector image  
- `api` service: depends on healthy db  
- Volume for sample data optional  

**Build/run (illustrative):**
```bash
docker compose up --build
```

## 4. Required env vars

See `.env.example`. Typical:

| Variable | Purpose |
|----------|---------|
| `API_KEY` | `change-me` disables auth; other values enable `X-API-Key` |
| `DATABASE_URL` | Postgres connection string |
| `EMBEDDING_MODEL` | HF / sentence-transformers model id |
| `LLM_*` | Provider/model settings for ask/extract |
| `MLFLOW_TRACKING_URI` | Default `./mlruns` for eval |

## 5. Model / index bundling

| Strategy | Choice |
|----------|--------|
| Download embedding weights at first run | Supported |
| Bake small sample corpus | Supported for demo |
| Prebuilt pgvector dump | Optional convenience |

## 6. Health for orchestrators

- Probe: `GET /health`  
- Expect `database: true` before sending traffic  

## 7. Decisions locked

Local Compose + uvicorn are the Design Phase deploy targets. No K8s requirement.
