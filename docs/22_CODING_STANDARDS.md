# 22 — Coding Standards

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Version | 1.0 |

## 1. Language & style

- Python 3.11+  
- Formatter/linter: **ruff**  
- Line length: 100  
- Type hints on public functions: **required**  

## 2. Naming

| Kind | Convention |
|------|------------|
| Modules/files | snake_case |
| Classes | PascalCase |
| Constants | UPPER_SNAKE |
| Config keys | snake_case in YAML |

## 3. Project rules

1. No business logic in API routers — call services  
2. No notebooks as source of truth  
3. Config over hardcoded paths and model ids  
4. Thin custom RAG — do not introduce LangChain as the core framework  
5. Explicit errors with clear messages  
6. Same embedding model for index and query  
7. Answers must carry citation structures from retrieval  
8. Do not invent evaluation metrics in docs or README  
9. No Prompt-Engineer positioning in comments, README, or demos  

## 4. Imports

- Prefer absolute imports from `docintel.*`  
- Avoid wildcard imports  

## 5. Docstrings

Public functions: one-line summary + args/returns when non-obvious.

## 6. Logging

Use module logger: `logging.getLogger(__name__)`  
No `print` in library code (CLI OK sparingly)  
Do not log secrets or full document bodies at INFO  

## 7. Forbidden for portfolio quality

- Committed secrets  
- `# noqa` spam without reason  
- Silent `except:`  
- Fabricated evaluation metrics in docs or README  
- LangChain-heavy rewrites without updating docs 02–04  

## 8. Optional later

mypy strict mode may be added; not a Design Phase gate.
