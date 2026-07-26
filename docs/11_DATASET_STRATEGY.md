# 11 — Dataset Strategy

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Critical for | Credibility with hiring managers |
| Version | 1.0 |

## 1. Dataset choice

| Item | Value |
|------|--------|
| Corpus type | Public / sample document set for portfolio demo |
| Formats | PDF (digital-text preferred), TXT |
| Domain fit | Intelligent Document Processing — searchable enterprise-like docs |
| Size | Small curated sample sufficient for local demo + CI fixtures |
| License | Must be redistributable or link-only; attribute in README |

## 2. Why this approach

A small, attributable sample corpus keeps the repo honest and runnable. Hiring managers care more about ingest→chunk→embed→retrieve→cite→evaluate discipline than a private enterprise dump. Digital-text PDFs reduce OCR variance for the primary demo path.

## 3. Corpus policy

| Rule | Detail |
|------|--------|
| No customer PII | Do not commit real client documents |
| Attribution | Cite sources and licenses in `data/README.md` |
| Samples committed | Tiny files under `data/samples/` for smoke demo |
| Large raw | gitignored under `data/raw/` if downloaded |
| Eval set | Labeled queries under `data/eval/` (question → relevant chunk/doc ids) |

## 4. Suggested sample content (illustrative)

Examples of appropriate sample themes (final files chosen at implementation):
- Product manual excerpt (warranty / specs)  
- Policy / FAQ style TXT  
- Simple invoice-like PDF for extraction schema demos  

Exact filenames are finalized when `data/samples/` is created — not required to invent proprietary content in Design Phase.

## 5. Train / validation / test policy (retrieval eval)

| Split | Rule |
|-------|------|
| Strategy | Fixed labeled query set for retrieval hit-rate @k |
| Holdout | Keep a small held-out query subset for final report |
| Leakage | Do not tune prompts/chunk sizes on the held-out query set after freezing |

**Leakage / honesty checklist:**
- [ ] No private customer data in public repo  
- [ ] Licenses attributed  
- [ ] Metrics only from real eval runs in `reports/EVALUATION_REPORT.md`  
- [ ] Limitations stated: sample corpus ≠ production plant deployment  

## 6. Storage & git policy

- Large binaries **not** committed  
- Tiny samples: yes — `data/samples/`  
- Download or assemble script: `scripts/prepare_sample_corpus.py` (or Makefile target)  

## 7. Synthetic / public note

This project uses a **public/sample** corpus. README and evaluation docs must state this clearly. Results demonstrate methodology, not operational guarantees for regulated document systems.

## 8. Ethics / safety

- No real PII  
- No unsafe claims of audit-ready compliance  
- Cite all third-party document sources  

## 9. Decisions locked

Public/sample corpus strategy, digital-PDF-first, eval labeled queries, and honesty constraints are final for Design Phase v1.
