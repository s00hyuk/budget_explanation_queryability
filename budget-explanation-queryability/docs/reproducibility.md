# Reproducibility Guide

This document records the exact configuration used to produce the results in the paper. Anyone re-running the notebook with the same configuration on the same data should obtain numerically identical aggregate scores (modulo LLM provider variance, which we discuss below).

---

## 1. Determinism

| Component | Setting |
|---|---|
| `numpy` random seed | `42` |
| Python `random` seed | `42` |
| Bootstrap resampling | `numpy.random.default_rng(42)` |
| LLM `temperature` | `0` |
| LLM `top_p` | default (1.0) |
| Vector retriever `top_k` | `5` |
| Embedding model | `jhgan/ko-sroberta-multitask` (Korean-specific, frozen weights) |
| Embedding `normalize_embeddings` | `True` |
| Vector DB | ChromaDB, in-memory |

### Sources of residual non-determinism

- **LLM provider variance**: even with `temperature=0`, commercial LLM providers can show small response-text variation due to backend updates, GPU non-determinism, or batching. The aggregate F1 (averaged over 100 questions) is stable at ±0.5 percentage points across runs in our testing.
- **Sentence-transformers backend**: GPU vs CPU may produce embeddings that differ at the 1e-7 level; this does not change top-k retrieval results in our experiments.

---

## 2. LLM specifics

We used a single commercial LLM (model-name redacted for double-blind review) called via the OpenAI-compatible API with the following pattern:

```python
client.chat.completions.create(
    model=MODEL_NAME,
    messages=[...],
    temperature=0,
    seed=42,                # OpenAI deterministic seed (when supported)
    response_format={"type": "json_object"} if JSON_MODE else None,
)
```

### Retry logic

For LLM calls (Plan generation in Text-to-Pandas and answer generation in RAG):

```python
def llm_call_with_retry(prompt, max_retries=3, backoff=2):
    for attempt in range(max_retries):
        try:
            resp = client.chat.completions.create(...)
            return resp.choices[0].message.content
        except (RateLimitError, APIError) as e:
            time.sleep(backoff ** attempt)
    return ""  # logged as a parse_error / generation_failure
```

Calls that fail all retries are logged in `results/logs/` and counted as F1=0 for the corresponding question.

---

## 3. Evaluation protocol

See [`eval_protocol.md`](eval_protocol.md) for the full No-Oracle protocol. Key points:

- **Single shared evaluator** for all 5 methods. No per-method scoring tweaks.
- `gold` and `acceptable_answers` are **never** included in any method's input or prompt context.
- Three evaluation modes: `exact_value` (18 questions), `exact_set` (13 questions), `any_3_from_candidate_set` (69 questions).
- F1 is the harmonic mean of per-question precision and recall, averaged over n=100.

---

## 4. Statistical testing

Paired bootstrap with 10,000 resamples:

```python
def paired_bootstrap(scores_a, scores_b, n_iter=10_000, seed=42):
    rng = np.random.default_rng(seed)
    n = len(scores_a)
    diffs = []
    for _ in range(n_iter):
        idx = rng.integers(0, n, size=n)             # same indices for both
        diff = np.mean(scores_b[idx]) - np.mean(scores_a[idx])
        diffs.append(diff)
    return np.percentile(diffs, [2.5, 50, 97.5])
```

- **True paired**: same resampled indices applied to both methods (not independent bootstraps).
- **NaN mask**: questions where either method failed are excluded from the paired comparison for that pair (not from the overall F1).
- Significance reported at 95% CI: a difference is "significant" iff CI does not include 0. We do **not** claim equivalence when CI includes 0; see paper §4.5.

---

## 5. Versioning

| Asset | Version |
|---|---|
| Goldset | `query_logic_fullset_perturbed_v1.csv` |
| RDF graph | `budget_graph_v2.ttl` |
| Text-to-Pandas executor | v3 (with alias resolver patch) |
| RDF SPARQL executor | v3 |
| XLSX template executor | v4 |
| Manifest | `manifest_5methods_perturbed_v1.json` |

The `manifest.json` at the repo root records all asset paths, methods, and aggregate F1 scores. It is the authoritative reference if any file in this repository is updated post-publication.

---

## 6. Hardware

Experiments were conducted on Google Colab Pro (T4 GPU). The notebook runs end-to-end in approximately 30–45 minutes. CPU-only execution is possible but ~3× slower for the embedding step.

---

## 7. Known caveats

1. **`text_to_pandas_plan_diagnostics.csv`** in the FINAL ZIP shows `parse_error` for all rows — this is an artifact of an early diagnostic script that did not match the final plan format. The actual JSON plans are preserved in `data/predictions/final_comparison_5methods_perturbed_v1.csv` under the `text_to_pandas_plan` column. Re-analysis of plan-level error types should use that column.

2. **RDF executor not in notebook**: Cell 14 of the notebook expects the RDF predictions as an external input. To regenerate `data/predictions/rdf_predictions_perturbed_v1.csv`, run `src/rdf/rdf_executor.py` (added to this repository for reproducibility, derived from the v3 SPARQL templates).

3. **Single LLM**: results may differ with other providers or models. We document this as a limitation in paper §6.6.
