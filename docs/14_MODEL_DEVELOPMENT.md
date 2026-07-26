# 14 — Model Development

| Field | Value |
|-------|--------|
| Status | Ready (Design Phase) |
| Version | 1.0 |

## 1. Problem formulation

| Item | Value |
|------|--------|
| Tasks | Semantic retrieval; RAG generation with citations; structured extraction |
| Primary “models” | Embedding model + generative LLM adapter (config) |
| Primary retrieval metric | Hit-rate @k |
| Primary generation check | Citation coverage / faithfulness checklist |
| Positioning | Applied AI / LLM engineering — **not** Prompt Engineer |

## 2. Model candidates

| Component | Role | Library / approach | Keep in v1? |
|-----------|------|--------------------|-------------|
| Embeddings | Vectorize chunks/queries | sentence-transformers / HF | Yes |
| Generative LLM | Answer + extract | Configurable adapter (local or API) | Yes |
| Reranker | Optional second-stage | HF cross-encoder | Optional later |
| LangChain agents | — | — | **No — excluded as core** |
| Fine-tuned domain LLM | — | — | Not required for v1 |

## 3. Baseline plan

1. Establish embedding + fixed_tokens chunking baseline retrieval hit-rate @k  
2. Compare at least one alternate chunk strategy on the same labeled queries  
3. RAG ask must return citations; insufficient-context path tested  
4. Log comparisons to MLflow when running eval experiments  

## 4. Development procedure

| Step | Detail |
|------|--------|
| Config | `configs/default.yaml` + experiment overrides |
| Seed | Fixed seed for any stochastic sampling where applicable |
| Prompt templates | Versioned under `configs/prompts/` — product config, not a prompt gallery |
| Retrieval | top_k from config |
| Artifact | embedding model id, chunk strategy, prompt versions, eval JSON |

## 5. Configuration table (defaults — pin at implementation)

| Param | Value / search space |
|-------|----------------------|
| embedding_model | HF sentence-transformers model id (pin in YAML) |
| chunk_strategy | `fixed_tokens` default; compare `recursive` |
| chunk_size / overlap | config |
| top_k | 5 default |
| llm.model | config adapter setting |
| temperature | low for extract/ask demo stability |

Exact final values are those logged in MLflow / config for the selected demo run.

## 6. Experiment tracking

- Tool: MLflow  
- URI: `./mlruns`  
- Log: params (model ids, chunk strategy, top_k), metrics (hit-rate @k, citation coverage), tags (`corpus=sample`, `phase=design-impl`)  
- Reports: `reports/EVALUATION_REPORT.md`  

## 7. Selection rule

Select demo configuration when:
- [ ] Retrieval eval completed on labeled set  
- [ ] Ask responses include citations on demo queries  
- [ ] Faithfulness checklist documented  
- [ ] Limitations stated (sample corpus)  

## 8. Entrypoints

```bash
python -m docintel.evaluation.run --config configs/default.yaml
# optional
mlflow ui --backend-store-uri ./mlruns
```

## 9. Decisions locked

HF embeddings + thin custom RAG + configurable LLM adapter. No LangChain-heavy core. No Prompt-Engineer positioning. Metrics only after real runs.
