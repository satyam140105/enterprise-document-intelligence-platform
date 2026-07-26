# 15 — Model Evaluation

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Hiring signal | Honest metrics + methodology > flashy scores |
| Version | 1.0 |

## 1. Evaluation principles

1. Labeled query set for retrieval (see doc 11)  
2. Always report **baseline chunk strategy** vs alternative when compared  
3. Separate tuning queries vs held-out queries when practical  
4. Require citations on ask; score citation coverage  
5. Document limitations (sample corpus; not production plant deployment)  
6. Do not invent metric numbers in docs — write them to reports after eval  

## 2. Metrics

### Retrieval
| Metric | Why |
|--------|-----|
| Hit-rate @k | **Primary** — relevant doc/chunk appears in top-k |
| MRR / nDCG | Optional secondary if labels support ranking |

### Generation / grounding
| Metric / check | Why |
|----------------|-----|
| Citation coverage | Share of answers with usable citations |
| Faithfulness checklist | Manual/heuristic checks that claims map to snippets |
| Insufficient-context behavior | Correct refusal / hedging when retrieval empty |

### Extraction
| Check | Why |
|-------|-----|
| Schema validity | Output matches schema keys/types |
| Evidence presence | Field-level snippets when available |

**Primary metric:** retrieval hit-rate @k  
**Secondary:** citation coverage + faithfulness checklist  

## 3. Threshold / gate policy

| Item | Value |
|------|--------|
| Hit-rate target | Document after first real eval — no invented bar in Design Phase docs |
| Demo gate | Demo queries must show citations; checklist completed |
| Applied on | Offline eval + qualitative demo script |

## 4. Evaluation report outputs

| Artifact | Path |
|----------|------|
| Narrative + tables | `reports/EVALUATION_REPORT.md` |
| Metrics JSON | `reports/metrics/metrics.json` |
| Figures | `reports/figures/` (optional) |

## 5. Required eval artifacts

- [ ] Hit-rate @k table for chosen configuration  
- [ ] Citation coverage summary for ask eval set  
- [ ] Faithfulness checklist results (pass/fail per demo question)  
- [ ] Limitations section  

## 6. Faithfulness checklist (template)

For each demo question:
1. Does the answer include at least one citation?  
2. Does each major claim map to a cited snippet?  
3. If retrieval is empty, does the system avoid fabricating specifics?  

## 7. Acceptance bars (link doc 26)

| Check | Pass rule |
|-------|-----------|
| Eval harness runnable | Must (after implementation) |
| Hit-rate computed from real run | Must — in `reports/EVALUATION_REPORT.md` |
| Citations present on demo asks | Must |
| Limitations documented | Must |
| Invented scores in docs | Forbidden |

## 8. Known limitations

1. Sample/public corpus only — not a plant or regulated DMS deployment.  
2. OCR quality varies; digital-first path is the reliability baseline.  
3. Generative answers can still err; citations and checklist reduce but do not eliminate risk.  

## 9. Metrics placeholder policy

All numeric hit-rate / coverage values **must** come from an actual evaluation run and appear in `reports/EVALUATION_REPORT.md`. Documentation must not hardcode fabricated scores.
