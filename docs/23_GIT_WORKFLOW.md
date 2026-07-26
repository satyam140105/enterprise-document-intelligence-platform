# 23 — Git Workflow

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Audience | Owner + Cursor agent commits |
| Version | 1.0 |

## 1. Why this matters

Hiring managers open **GitHub history**. Prefer small, meaningful commits over one giant dump.

## 2. Branch model (solo-friendly)

| Branch | Purpose |
|--------|---------|
| `main` | Stable, always runnable docs + passing smoke tests (once code exists) |
| `feat/<short-name>` | Feature work |
| `fix/<short-name>` | Bugfixes |
| `docs/<short-name>` | Documentation-only |

Merge to `main` via PR (even solo) when possible — shows process.

## 3. Conventional commits

Format:
```text
<type>(optional-scope): <imperative summary>

[optional body]
```

### Types
| Type | Use |
|------|-----|
| `feat` | New user-facing capability |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | No behavior change |
| `test` | Tests only |
| `chore` | Tooling, gitignore, deps housekeeping |
| `build` | Docker/CI packaging |
| `perf` | Performance |

### Good examples
```text
docs: lock Ready Design Phase specs for document intelligence platform
chore: scaffold docintel package layout
feat(ingest): add PDF/TXT ingest and document status tracking
feat(processing): add fixed_tokens and recursive chunking strategies
feat(retrieval): add pgvector semantic search
feat(rag): add ask endpoint with citation payloads
feat(extract): add schema-driven field extraction
test: add API validation and chunking tests
fix(store): correct pgvector upsert for re-ingest
```

### Bad examples
```text
update
final
stuff
fixed everything
WIP
```

## 4. Commit granularity

Prefer:
1. scaffold / chore  
2. filled docs (this Design Phase set)  
3. DB migrations + store  
4. processing (extract/chunk/embed)  
5. retrieval + rag + extract  
6. evaluation  
7. API polish  
8. docker/ci  

Do **not** mix unrelated refactors with feature commits.

## 5. Messages rules

- Imperative mood: “add”, not “added”  
- ≤ ~72 chars subject  
- Explain **why** in body when non-obvious  
- Never commit secrets, large corpora, or proprietary customer PDFs  

## 6. PR description template

```markdown
## Summary
- …

## Test plan
- [ ] pytest
- [ ] ruff
- [ ] manual API check (if applicable)
```

## 7. Release tags

When portfolio implementation criteria met:
```text
git tag -a v0.1.0 -m "Release v0.1.0 — enterprise document intelligence platform"
```

## 8. Remote

Expected GitHub remote: `ahmadian-dev/enterprise-document-intelligence-platform` (confirm when pushing).

## 9. Decisions locked

Conventional commits + `main` protection via readable history are the professionalism bar — matching portfolio DNA from the predictive maintenance project.
