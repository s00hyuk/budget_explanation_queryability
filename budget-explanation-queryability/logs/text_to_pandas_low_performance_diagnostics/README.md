# Supplementary diagnostics: Text-to-Pandas low-performance cases

These files provide an alternative case-level diagnostic of the Text-to-Pandas Agent using a wider F1 threshold (F1 < 0.7, n=53) than the main paper Table 5-3A (F1 < 0.5, n=40).

## Files

- `primary_error_type_summary_f1_lt_07.csv` — 7 primary error types with mean F1 per type
- `error_flag_summary_f1_lt_07.csv` — overlapping diagnostic flags (single case can have multiple flags)
- `case_details_f1_lt_07.csv` — case-level details (53 rows) with primary type, flags, and free-form notes

## Relationship to paper Table 5-3A

The main paper Table 5-3A is based on `results/final/text_to_pandas_severe_failure_error_type_summary_f1_lt_05.csv` (n=40, F1<0.5, 3 categories), which restricts the analysis to severe failure cases (39/40 are F1=0) where automatic error classification is most reliable.

The files in this directory extend the analysis to all sub-success cases (F1<0.7, n=53), including 13 partial-success cases (0.5≤F1<0.7) whose primary error types are inherently more ambiguous due to mixed causes. These files are provided **for case-level inspection and supplementary review only** and are NOT the source of paper Table 5-3A.
