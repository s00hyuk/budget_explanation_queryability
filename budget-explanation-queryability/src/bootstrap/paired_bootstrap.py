#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reproduce paired bootstrap confidence intervals from saved per-question F1.

Paired bootstrap resamples the same question IDs for both methods. This is the
proper test because all methods are evaluated on the same 100 questions.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
EVAL = ROOT / "results/final/final_eval_long_5methods_perturbed_v1.csv"
OUT = ROOT / "results/bootstrap"

COMPARISONS = [
    ("Plain Text Vector RAG", "JSON Serialization Vector RAG", "JSON − Vector (3단계 vs 1단계 표현)"),
    ("Plain Text Vector RAG", "Text-to-Pandas Agent", "Text-to-Pandas − Vector"),
    ("Plain Text Vector RAG", "RDF Template SPARQL v3", "RDF − Vector"),
    ("Plain Text Vector RAG", "XLSX Template Executor v4", "XLSX − Vector"),
    ("JSON Serialization Vector RAG", "Text-to-Pandas Agent", "Text-to-Pandas − JSON"),
    ("JSON Serialization Vector RAG", "XLSX Template Executor v4", "XLSX − JSON"),
    ("Text-to-Pandas Agent", "XLSX Template Executor v4", "XLSX − Text-to-Pandas (쿼리 자동생성 손실)"),
    ("Text-to-Pandas Agent", "RDF Template SPARQL v3", "RDF − Text-to-Pandas"),
    ("RDF Template SPARQL v3", "XLSX Template Executor v4", "XLSX − RDF (구조별 상한선)"),
]


def paired_bootstrap(a, b, n_boot=10000, seed=42):
    rng = np.random.default_rng(seed)
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    mask = ~(np.isnan(a) | np.isnan(b))
    a = a[mask]
    b = b[mask]
    n = len(a)
    obs = np.mean(b - a)
    diffs = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, size=n)
        diffs[i] = np.mean(b[idx] - a[idx])
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p_two = 2 * min(np.mean(diffs <= 0), np.mean(diffs >= 0))
    return obs, lo, hi, min(float(p_two), 1.0), n


def main():
    df = pd.read_csv(EVAL)
    wide = df.pivot_table(index="id", columns="method", values="f1", aggfunc="first")
    rows = []
    for a, b, label in COMPARISONS:
        obs, lo, hi, p_two, n = paired_bootstrap(wide[a].values, wide[b].values)
        rows.append({
            "comparison": label,
            "method_a": a,
            "method_b": b,
            "mean_f1_a": round(wide[a].mean() * 100, 2),
            "mean_f1_b": round(wide[b].mean() * 100, 2),
            "mean_diff_pct": round(obs * 100, 2),
            "ci_low_pct": round(lo * 100, 2),
            "ci_high_pct": round(hi * 100, 2),
            "p_two_sided": round(p_two, 4),
            "n": n,
            "significant_95": "Yes" if lo > 0 else "No",
        })
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "paired_bootstrap_5methods_perturbed_v1_percent_REPRODUCED.csv", index=False, encoding="utf-8-sig")
    print(out.to_string(index=False))
    print("Saved reproduced bootstrap file under results/bootstrap/")

if __name__ == "__main__":
    main()
