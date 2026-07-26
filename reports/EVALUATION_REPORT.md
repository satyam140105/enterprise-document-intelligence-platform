# Evaluation Report — Enterprise Document Intelligence Platform

**Status:** Released portfolio evaluation  
**Corpus:** Public/sample documents (`data/samples`)  
**Note:** sample/public corpus — methodology demo, not production plant deployment

## Metrics

| Metric | Value | Detail |
|--------|------:|--------|
| Retrieval hit-rate @5 | **1.000** | 5/5 queries |
| Citation coverage | **1.000** | 5/5 |
| Faithfulness checklist | **1.000** | 5/5 |

## Method

1. Embed query with the same sentence-transformers model used at ingest  
2. Cosine similarity over chunk vectors  
3. Hit if any retrieved `document_id` intersects labeled relevant set  
4. Citation coverage requires non-empty citations and answer markers  
5. Checklist verifies citations + non-empty grounded answers  

## Limitations

- Sample corpus — not a customer production archive  
- Default answers are **extractive** unless `LLM_API_KEY` is configured  
- Hit-rate depends on labeled eval set size and chunking choices  

## Artifacts

- `reports/metrics/eval_metrics.json`  
- MLflow experiment: `document-intelligence`  
