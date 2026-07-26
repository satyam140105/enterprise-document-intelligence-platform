# 08 — UI / UX Specification

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Product stance | **API-first**; Swagger primary for v1 |
| Version | 1.0 |

## 1. Decision

| Option | Choice |
|--------|--------|
| A. No custom UI in v1 — Swagger UI only | **Yes (primary)** |
| B. Minimal Streamlit demo | Optional later — not required for Design Phase freeze |
| C. Thin React dashboard | No |

**Selected:** A — FastAPI `/docs` (Swagger) is the interactive surface for v1. Streamlit may be added later without changing API contracts.

## 2. Swagger-only UX

- Primary UX = FastAPI `/docs`  
- Clear example payloads in OpenAPI for ingest, search, ask, extract  
- Consistent field naming with docs/10  
- `/redoc` available as secondary read-only view  

**Screens to capture for demo (doc 25):**
- [ ] `/docs` overview  
- [ ] Example ingest 200  
- [ ] Example search 200 with scores  
- [ ] Example ask 200 with citations  
- [ ] Example extract 200  
- [ ] `/health` JSON  

## 3. Streamlit / custom UI

Not required for Design Phase or v1 release bar. If added later: thin demo only; must call the same FastAPI contracts; update this doc first.

## 4. Accessibility / language

- English UI copy (OpenAPI descriptions)  
- Error messages actionable (field-level validation detail)  
- Tone: professional, technical, enterprise — no hype  
- No Prompt-Engineer styling or “magic prompt” UX  

## 5. Non-goals

- Full DMS replacement UI  
- Mobile-native app  
- Dashboards, charts, or branding chrome beyond Swagger defaults (unless presentation assets live outside `/docs`)  
