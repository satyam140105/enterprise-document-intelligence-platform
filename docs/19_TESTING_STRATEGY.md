# 19 — Testing Strategy

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Version | 1.0 |

## 1. Test pyramid

| Layer | Tools | Scope |
|-------|-------|-------|
| Unit | pytest | chunking, normalization, schema validation, pure helpers |
| Integration | pytest | ingest→search smoke with Postgres (Compose or testcontainer); API TestClient |
| Evaluation gates | scripts / checklist | metrics present in reports after full eval |
| Manual | checklist | demo path (Swagger) |

## 2. Required tests (v1)

| Test | File | Priority |
|------|------|----------|
| Package imports | `tests/test_smoke.py` | P0 |
| Chunking strategies produce non-empty chunks | `tests/test_chunking.py` | P0 |
| Text extract on sample TXT/PDF fixture | `tests/test_extract_text.py` | P0 |
| API health | `tests/test_api.py` | P0 |
| Ingest validation errors (422) | `tests/test_api.py` | P0 |
| Search / ask schema validation | `tests/test_api.py` | P0 |
| Ask returns citations field | `tests/test_api.py` | P1 |
| Auth disabled vs enabled behavior | `tests/test_api_auth.py` | P1 |
| Retrieval hit-rate smoke on tiny fixture | `tests/test_eval_smoke.py` | P1 |

## 3. Test data

- Tiny fixtures under `tests/fixtures/` (short TXT + minimal PDF if practical)  
- Must not require large corpus download in CI  

## 4. Commands

```bash
pytest -q
ruff check src tests
```

## 5. Coverage target

Critical modules (`processing`, `api` schemas, retrieval helpers). No vanity global % gate.

## 6. Definition of done for a PR

- [ ] Tests green  
- [ ] Lint clean  
- [ ] Docs updated if contract changed  

## 7. Decisions locked

pytest + ruff are required CI checks for the portfolio quality bar once implementation begins.
