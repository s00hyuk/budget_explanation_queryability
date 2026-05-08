#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reproduce summary tables from the saved per-question evaluation file.

This script does not call an LLM. It verifies and recomputes the official
5-method summary tables used in the paper from:
results/final/final_eval_long_5methods_perturbed_v1.csv
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
EVAL = ROOT / "results/final/final_eval_long_5methods_perturbed_v1.csv"
GOLD = ROOT / "data/goldset/query_logic_fullset_perturbed_v1.csv"
OUT = ROOT / "results/final"


def main():
    df = pd.read_csv(EVAL)
    assert df.shape[0] == 500, f"Expected 500 rows, got {df.shape[0]}"
    assert df["method"].nunique() == 5, "Expected 5 methods"
    assert df["id"].nunique() == 100, "Expected 100 question IDs"

    overall = df.groupby("method").agg(
        n=("id", "count"),
        precision=("precision", "mean"),
        recall=("recall", "mean"),
        f1=("f1", "mean"),
        f1_ge07=("f1", lambda x: (x >= 0.7).mean()),
    ).reset_index()
    for c in ["precision", "recall", "f1", "f1_ge07"]:
        overall[c] = (overall[c] * 100).round(2)

    type_summary = df.groupby(["method", "type"]).agg(
        n=("id", "count"),
        precision=("precision", "mean"),
        recall=("recall", "mean"),
        f1=("f1", "mean"),
    ).reset_index()
    for c in ["precision", "recall", "f1"]:
        type_summary[c] = (type_summary[c] * 100).round(2)

    gold = pd.read_csv(GOLD)[["id", "question_noise_level", "noise_type"]]
    merged = df.merge(gold, on="id", how="left")
    noise_summary = merged.groupby(["method", "question_noise_level"]).agg(
        n=("id", "count"),
        precision=("precision", "mean"),
        recall=("recall", "mean"),
        f1=("f1", "mean"),
    ).reset_index()
    for c in ["precision", "recall", "f1"]:
        noise_summary[c] = (noise_summary[c] * 100).round(2)

    overall.to_csv(OUT / "overall_summary_5methods_perturbed_v1_REPRODUCED.csv", index=False, encoding="utf-8-sig")
    type_summary.to_csv(OUT / "type_summary_5methods_perturbed_v1_REPRODUCED.csv", index=False, encoding="utf-8-sig")
    noise_summary.to_csv(OUT / "noise_level_summary_5methods_perturbed_v1_REPRODUCED.csv", index=False, encoding="utf-8-sig")
    print(overall.to_string(index=False))
    print("Saved reproduced summary files under results/final/")

if __name__ == "__main__":
    main()
