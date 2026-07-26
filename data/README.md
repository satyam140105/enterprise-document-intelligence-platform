# Dataset placement — Enterprise Document Intelligence Platform

## Sample corpus (committed)

| File | Theme |
|------|--------|
| `data/samples/warranty_policy.txt` | Warranty / policy ID |
| `data/samples/expense_policy.txt` | HR expense policy |
| `data/samples/technical_faq.txt` | Technical FAQ |

## Eval set

`data/eval/queries.json` — labeled questions with `relevant_filenames`.

## Rebuild index

```bash
set PYTHONPATH=src
python scripts/build_index_and_eval.py
```

Index files under `data/processed/index/` are gitignored / regenerable.

## License / honesty

Portfolio sample documents authored for demo. Not customer data. Not a production plant archive.
