# 17 — Monitoring and Observability

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Version | 1.0 |

## 1. Goals

Detect: service health issues, bad inputs, latency regressions, DB/embedding readiness failures, and empty-retrieval patterns. Full production APM/drift platforms are out of scope.

## 2. Logging

| Item | Decision |
|------|----------|
| Format | JSON structured logs to stdout |
| Fields | timestamp, request_id, route, latency_ms, status_code, document_id (optional), retrieval_k (optional) |
| PII | Avoid logging full document bodies; snippets truncated |
| Destination | stdout (Docker-friendly) |

## 3. Metrics (application)

| Metric | Type | Notes |
|--------|------|-------|
| request counts by route/status | log-derived | v1 |
| `latency_ms` | per-request log field | v1 |
| DB / embedding readiness | exposed via `/health` | v1 |
| empty retrieval count | log field or counter | useful for RAG quality |

**v1 approach:** structured logs only — no Prometheus endpoint required.

## 4. ML monitoring (lightweight)

| Signal | How | Action |
|--------|-----|--------|
| Input schema failures | count 422s in logs | investigate client contract |
| Empty retrievals | log on search/ask | review chunking / corpus |
| Extract schema misses | 422 on unknown schema | fix client or add schema |

## 5. Health & readiness

| Probe | Endpoint | Meaning |
|-------|----------|---------|
| Liveness | `GET /health` | process up |
| Readiness | `/health` with `database: true` (and embedding loaded when required) | can serve |

## 6. Alerting

Portfolio v1: none automated — manual log review during demo/ops.

## 7. Decisions locked

Stdout JSON logs + `/health` are the Design Phase observability surface.
