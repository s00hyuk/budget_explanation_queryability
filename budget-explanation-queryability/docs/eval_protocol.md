# Evaluation Protocol

## 1. No-Oracle Principle

A central design principle of this benchmark is the **No-Oracle protocol**: the gold answer fields (`gold`, `acceptable_answers`) are **never** exposed to any method's input, prompt, or generation context. They are used only at scoring time.

**Implementation guarantee:**
- The goldset CSV is loaded once at notebook startup
- Each method's pipeline is given only `id`, `question` (or `query_logic` for RDF/XLSX), and the source data files
- The evaluator is a single shared function, applied identically to all 5 methods after all predictions are collected
- No method has the opportunity to see gold answers during prediction

This is verified by code inspection: `gold` and `acceptable_answers` columns are read only inside `evaluate_predictions()` (Cell 15 of the notebook).

---

## 2. Evaluation Modes

The benchmark uses three evaluation modes, applied per-question based on the question's expected answer structure.

### 2.1 `exact_value` (n=18)

Used when the answer is a single value (typically a count, sum, or percentage).

```
score = 1.0 if extract_number(prediction) == extract_number(gold) else 0.0
```

`extract_number()` handles unit normalization (백만원 / 만원 / 억원 / 개) and Korean numeral parsing.

### 2.2 `exact_set` (n=13)

Used when the answer is a set of items where all items must be retrieved.

```
P = |pred_set ∩ gold_set| / |pred_set|
R = |pred_set ∩ gold_set| / |gold_set|
F1 = 2PR / (P + R)
```

Item-level set comparison after string normalization (NFKC + alias expansion).

### 2.3 `any_3_from_candidate_set` (n=69)

Used when the answer is a list-style answer drawn from a larger candidate set, allowing the method to return any subset up to `answer_limit` items.

```
truncated_pred = pred_items[:answer_limit]
P = |truncated_pred ∩ candidate_set| / |truncated_pred|
R = |truncated_pred ∩ candidate_set| / min(|candidate_set|, answer_limit)
F1 = 2PR / (P + R)
```

This mode is appropriate when there are many valid answers (e.g., "list ministries that supervise programs in field X") and we don't penalize the method for picking different valid items.

---

## 3. Normalization Pipeline

Before any comparison, both `prediction` and `gold` strings pass through:

1. **NFKC normalization** — Unicode canonical equivalence
2. **Whitespace collapse** — multiple spaces → single space
3. **Alias expansion** — 24 ministry/agency aliases mapped to canonical forms (e.g., `과기부` → `과학기술 정보통신부`, `IITP` → `정보통신기획평가원`, `NIA` → `한국지능정보사회진흥원`)
4. **Unit normalization** — `백만원` / `억원` / `만원` / `원` parsed and converted to a common base when in numeric mode
5. **Punctuation handling** — `·` / `,` / `/` separators in list-style answers normalized to whitespace
6. **DROP_TOKENS** — common filler words removed (note: `"원"` was removed from DROP_TOKENS in v3 to avoid false-positive matching of `"기관"` ↔ `"기"` after token drop)

---

## 4. Reporting

We report:

- **Per-question F1** (n=100 vector for each method)
- **Overall mean F1** (paper Table 5-1)
- **Per-type F1** (MultiHop / Reverse / ComplexFilter / Aggregation; paper Table 5-3)
- **Per-noise-level F1** (L1 / L2 / L3; paper Table 5-4)
- **Per-evaluation-mode F1** (paper Table 5-3B)
- **F1 ≥ 0.7 ratio** as a complementary metric (proportion of questions answered substantially correctly)

For statistical comparison: paired bootstrap with 95% CI; see [`reproducibility.md`](reproducibility.md) §4.

---

## 5. Answerability Audit

Before running the experiments, we performed an answerability audit on the 100-question evaluation set:

- `gold` column: 0 missing values
- `acceptable_answers` column: 0 missing values
- `evaluation_mode` column: 0 missing values
- All 100 questions verified as having at least one answer in the source data

After running all 5 methods, we identified the **F1=0 across all methods** intersection: 8 questions, classified as a "challenging subset" rather than as unanswerable. These 8 questions involve combinations of complex conditions, strong natural-language perturbation, and non-standard aggregation criteria, and are flagged in the paper §4.2.4 as priority targets for future evaluation-set improvement.
