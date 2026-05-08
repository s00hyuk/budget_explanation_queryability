# Final Artifact Manifest

Package: `budget-explanation-queryability`  
Release: `v1.0-paper-submission`  
Paper version: `v3.18`  
Benchmark version: `perturbed_v1`  
Generated: 2026-05-08

## Official experiment

Main reported experiment: **5-method perturbed benchmark**.

## Goldset

- `data/goldset/query_logic_fullset_perturbed_v1.csv`
  - Rows: 100
  - Noise levels: {'L2_realistic': 50, 'L1_strict': 30, 'L3_perturbed': 20}
- `data/goldset/perturbation_quality_check_v1.csv`
  - Automatic perturbation quality checks.

## Prediction files

- `data/predictions/vector_predictions_perturbed_v1.csv`
- `data/predictions/json_rag_predictions_perturbed_v1.csv`
- `data/predictions/text_to_pandas_predictions_perturbed_v1.csv`
- `data/predictions/rdf_predictions_perturbed_v1.csv`
- `data/predictions/xlsx_predictions_perturbed_v1.csv`
- `data/predictions/final_comparison_5methods_perturbed_v1.csv`

## Official evaluation files

- `results/final/final_eval_long_5methods_perturbed_v1.csv`
- `results/final/overall_summary_5methods_perturbed_v1.csv`
- `results/final/type_summary_5methods_perturbed_v1.csv`
- `results/final/noise_level_summary_5methods_perturbed_v1.csv`
- `results/final/evaluation_mode_summary_5methods_perturbed_v1.csv` (paper Table 5-3B)
- `results/final/text_to_pandas_severe_failure_error_type_summary_f1_lt_05.csv` (paper Table 5-3A; severe failure subset, F1<0.5, n=40)
- `results/final/evaluation_mode_summary_5methods_perturbed_v1.csv` (paper Table 5-3B)

## Supplementary diagnostics (NOT used as main paper Table sources)

- `results/final/stage1_diagnostic_artifact_index.csv` (artifact role index: official vs supplementary)
- `logs/text_to_pandas_severe_failure_cases_f1_lt_05.csv` (case-level support for Table 5-3A, n=40)
- `logs/text_to_pandas_low_performance_diagnostics/primary_error_type_summary_f1_lt_07.csv` (wider threshold, n=53)
- `logs/text_to_pandas_low_performance_diagnostics/error_flag_summary_f1_lt_07.csv` (overlapping flags)
- `logs/text_to_pandas_low_performance_diagnostics/case_details_f1_lt_07.csv` (case-level details with notes)
- `logs/text_to_pandas_low_performance_diagnostics/README.md` (relationship to main Table 5-3A)

## Strategy documentation

- `docs/paper_v3_18_table_5_3A_5_3B_strategy.md` (Table 5-3A/5-3B strategic decisions: severe-failure subset rationale, interpretation guardrails)

Official overall F1:

| method                        |    f1 |
|:------------------------------|------:|
| JSON Serialization Vector RAG | 14.83 |
| Plain Text Vector RAG         | 33.77 |
| RDF Template SPARQL v3        | 58.4  |
| Text-to-Pandas Agent          | 54.57 |
| XLSX Template Executor v4     | 65.4  |

## Bootstrap

- `results/bootstrap/paired_bootstrap_5methods_perturbed_v1_percent.csv`
- `results/bootstrap/paired_bootstrap_by_type_5methods_perturbed_v1_percent.csv`

Bootstrap design: paired bootstrap over the same 100 question IDs, 10,000 resamples, seed=42.

## RDF

- `schema/bedo_v1.ttl`: ontology schema.
- `data/rdf/budget_graph_v2.ttl`: instance-level graph.
- `logs/rdf_type_counts.csv`: RDF class counts.

## Reproduction entry points

- `src/validation/validate_artifacts.py`
- `src/evaluation/evaluate_saved_outputs.py`
- `src/bootstrap/paired_bootstrap.py`

## Excluded from clean package

Intermediate nested ZIP files from iterative experiments were intentionally excluded to avoid version ambiguity.
