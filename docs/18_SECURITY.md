# 18 — Security

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Context | Portfolio project — apply proportional controls |
| Version | 1.0 |

## 1. Threat model (simple)

| Threat | Risk | Mitigation |
|--------|------|------------|
| Secret leakage in git | High | `.gitignore`, `.env.example` only |
| Unauthorized API use | Medium | Optional `X-API-Key`; bind localhost for private demos |
| Malicious uploads | Medium | Type allowlist, size limits, no executable ingest |
| Prompt injection via documents | Medium | Treat docs as untrusted; constrain system instructions; citations over blind trust |
| Dependency vulns | Medium | Pin versions; occasional audit |
| Path traversal | Medium | Resolve paths under allowed dirs only |

## 2. Secrets management

- Local: `.env` (never commit)  
- CI: GitHub Secrets only if needed  
- LLM API keys never logged  
- Rotate demo keys before public screenshots  

## 3. API security

| Control | v1 |
|---------|-----|
| HTTPS | Local HTTP OK; terminate TLS at reverse proxy if hosted later |
| Auth | Optional `X-API-Key`; **disabled** when `API_KEY=change-me` |
| Rate limit | None in v1 |
| CORS | Restrictive default |
| Input validation | Pydantic required |
| Upload limits | Configured max size |

## 4. Data security

- No proprietary customer documents in public repo  
- Sample corpus attribution in README  
- Avoid logging full extracted text at INFO  

## 5. Dependency & supply chain

- Prefer pinned versions before public release  
- Optional later: `pip audit` / Dependabot  

## 6. Secure coding notes

- No `eval` on user input  
- Sanitize filenames; store under controlled paths  
- Do not log API keys or LLM provider secrets  
- Document content is untrusted input for LLM prompts  

## 7. Decisions locked

Auth default off for local demo (`API_KEY=change-me`). Enable by setting a real key for shared deployments. Sample corpus only in public artifacts.
