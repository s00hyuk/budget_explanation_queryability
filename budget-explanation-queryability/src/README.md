# `src/` Source Code

> **Where is the RAG / Pandas / RDF method implementation?**
> The full generation pipelines for all 5 methods live in [`notebooks/budget_5method_pipeline.ipynb`](../notebooks/budget_5method_pipeline.ipynb) (Cell 0 → Cell 20). The Python scripts under `src/` provide a lightweight *saved-output reproduction* path that recomputes the final reported tables and paired bootstrap results without calling any external LLM.

## Runnable reproduction code (saved-output path)

These modules reproduce the official paper score tables from saved per-question evaluation files. They do **not** call an LLM.

| Module | What it does |
|---|---|
| `validation/validate_artifacts.py` | Verifies all required artifacts exist and that official F1 values match |
| `evaluation/evaluate_saved_outputs.py` | Recomputes overall / type / noise-level summary tables from `final_eval_long_5methods_perturbed_v1.csv` |
| `bootstrap/paired_bootstrap.py` | Recomputes paired bootstrap CIs (10,000 resamples, seed=42) |
| `utils/normalization.py` | Shared text normalization utilities |

Run them in order via:

```bash
bash run_reproduce_saved_outputs.sh
```

This reproduces the paper Tables 5-1, 5-2, 5-3, 5-4 from saved data, with no external API calls.

---

## Method implementation reference

The five evaluated methods are implemented in `notebooks/budget_5method_pipeline.ipynb`:

| Method | Notebook cells |
|---|---|
| Plain Text Vector RAG | Cell 9, 10 (ChromaDB + ko-sroberta + LLM) |
| JSON Serialization Vector RAG | Cell 9b, 10b (same retriever, JSON-serialized chunks) |
| Text-to-Pandas Agent | Cell 11 (24-org alias resolver), Cell 12 (NL → JSON plan, plan executor) |
| RDF Template SPARQL v3 | external (see notebook §14 note) |
| XLSX Template Executor v4 | Cell 13 (parameterized table executor) |

For full reproduction from raw data, run the notebook in Colab. See [`docs/reproducibility.md`](../docs/reproducibility.md) for the determinism caveats — commercial LLM providers are not bit-level reproducible across runs.

### RDF executor note

Notebook Cell 14 expects RDF predictions as an external input — it does not generate them. To regenerate `data/predictions/rdf_predictions_perturbed_v1.csv`, a standalone RDF executor (running v3 SPARQL templates against `data/rdf/budget_graph_v2.ttl`) is needed. We will publish this as a follow-up commit.
