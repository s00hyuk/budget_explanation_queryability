#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate final 5-method artifact package."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
    "README.md",
    "requirements.txt",
    "FINAL_ARTIFACT_MANIFEST.md",
    "notebooks/budget_5method_pipeline.ipynb",
    "data/goldset/query_logic_fullset_perturbed_v1.csv",
    "data/predictions/final_comparison_5methods_perturbed_v1.csv",
    "results/final/final_eval_long_5methods_perturbed_v1.csv",
    "results/final/overall_summary_5methods_perturbed_v1.csv",
    "results/bootstrap/paired_bootstrap_5methods_perturbed_v1_percent.csv",
    "data/rdf/budget_graph_v2.ttl",
    "schema/bedo_v1.ttl",
    "logs/rdf_type_counts.csv",
    "logs/text_to_pandas_plan_diagnostics.csv",
]

EXPECTED_F1 = {
    "JSON Serialization Vector RAG": 14.83,
    "Plain Text Vector RAG": 33.77,
    "Text-to-Pandas Agent": 54.57,
    "RDF Template SPARQL v3": 58.40,
    "XLSX Template Executor v4": 65.40,
}


def main():
    rows=[]
    for rel in REQUIRED:
        p = ROOT/rel
        rows.append({"file": rel, "exists": p.exists(), "size_bytes": p.stat().st_size if p.exists() else 0})
    report = pd.DataFrame(rows)
    report.to_csv(ROOT/"artifact_completeness_report_clean.csv", index=False, encoding="utf-8-sig")
    if not report["exists"].all():
        print(report.to_string(index=False))
        raise SystemExit("Missing required artifacts")

    overall = pd.read_csv(ROOT/"results/final/overall_summary_5methods_perturbed_v1.csv")
    got = dict(zip(overall["method"], overall["f1"]))
    for method, expected in EXPECTED_F1.items():
        actual = round(float(got.get(method, -1)), 2)
        if actual != expected:
            raise SystemExit(f"F1 mismatch for {method}: expected {expected}, got {actual}")

    eval_long = pd.read_csv(ROOT/"results/final/final_eval_long_5methods_perturbed_v1.csv")
    assert eval_long.shape[0] == 500, eval_long.shape
    assert eval_long["id"].nunique() == 100
    assert eval_long["method"].nunique() == 5

    print("All required artifacts exist and official F1 values match.")
    print(report.to_string(index=False))

if __name__ == "__main__":
    main()
