# Data Card

## Overview

This directory contains the data assets for the *Budget Explanation Queryability Benchmark*. All data is derived from publicly available Korean government budget explanation documents (`예산설명서`).

---

## Files

| File | Size | Description |
|---|---|---|
| `budget_533.xlsx` | ~1.5 MB | Source data: 533 AI-related fiscal projects from Korea's 2026 government budget. Two sheets: `df_base` (project-level) and `df_subj` (implementing-agency-level). |
| `budget_graph_v2.ttl` | ~507 KB | RDF instance graph (Turtle format). Built from `budget_533.xlsx` using the BEDO v1.0 ontology (see `docs/BEDO_v1.0.md`). 533 `:Project` instances with 8 core classes. |
| `budget_projects_533.json` | ~1.6 MB | JSON serialization of the same 533 projects. Hierarchical dict-list structure preserving the project–program–unit-program hierarchy. |
| `goldset/query_logic_fullset.csv` | ~100 KB | 100 evaluation questions (original, no perturbation). |
| `goldset/query_logic_fullset_perturbed_v1.csv` | ~130 KB | Same 100 questions, perturbed at three difficulty levels (L1=30 / L2=50 / L3=20). |
| `goldset/perturbation_quality_check_v1.csv` | ~37 KB | `semantic_flags()` quality audit results: numeric, terminology, and entity preservation checks. |

---

## Goldset schema

Each row in `query_logic_fullset_perturbed_v1.csv` has the following columns:

| Column | Description |
|---|---|
| `id` | Unique question ID (e.g., `MH01`, `RV15`, `CF22`, `AGG007`, `SQA068`) |
| `type` | `MultiHop` / `Reverse` / `ComplexFilter` / `Aggregation` |
| `question` | Perturbed natural-language question (used as input to NL-input methods) |
| `question_original` | Original strict-form question |
| `question_noise_level` | `L1_strict` / `L2_realistic` / `L3_perturbed` |
| `noise_type` | e.g., `abbreviation`, `colloquial`, `omission`, `none` |
| `query_logic` | Pseudocode-like logic statement (used as input to RDF/XLSX methods) |
| `gold` | Reference answer string |
| `acceptable_answers` | Set of accepted answer candidates (No-Oracle: never used in generation) |
| `evaluation_mode` | `exact_value` / `exact_set` / `any_3_from_candidate_set` |
| `answer_limit` | Max number of items allowed in list-style answers |
| `question_pattern` | Internal pattern label (e.g., `agency_ministry_relation`) |

### Question-type distribution

| Type | n |
|---|---|
| MultiHop | 30 |
| Reverse | 30 |
| ComplexFilter | 25 |
| Aggregation | 15 |
| **Total** | **100** |

### Perturbation level distribution

| Level | n | Description |
|---|---|---|
| L1_strict | 30 | minimal variation, near-original phrasing |
| L2_realistic | 50 | natural user phrasing, partial abbreviations / colloquial wording |
| L3_perturbed | 20 | strong perturbation: heavy abbreviation, colloquial reformulation, reordering |

---

## License & Citation

The underlying budget documents are public Korean government documents. This goldset and its perturbations were curated by the authors. Please cite the accompanying paper if you use this data.

**No PII**: all entities in this dataset are public-sector organizations (ministries, agencies, programs). No personal information is included.

**Disclaimer**: this evaluation set was constructed by a single research team without external inter-annotator agreement. It should be interpreted as a domain-specific *queryability benchmark* for relative comparison among methods, not as a general-purpose RAG evaluation set. See the paper §4.2 and §6.6 for limitations.
