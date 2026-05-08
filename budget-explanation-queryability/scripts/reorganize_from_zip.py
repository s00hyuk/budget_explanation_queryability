#!/usr/bin/env python3
"""
reorganize_from_zip.py
======================

Rebuild the v2 GitHub layout from the FINAL ZIP artifact
(`5method_perturbed_v1_FINAL_*.zip`).

The FINAL ZIP has the structure:

    2026_AI_Budget_Projects/
    ├── data/{goldset,predictions,rdf}/...
    ├── results/{final,bootstrap}/...
    ├── logs/...
    ├── figures/...
    └── manifest_*.json

This script copies its contents into the v2 repository layout (data/raw/,
data/goldset/, data/rdf/, data/predictions/, results/, schema/, etc.).

Usage:
    python scripts/reorganize_from_zip.py /path/to/5method_perturbed_v1_FINAL_<timestamp>.zip

Run from the repository root.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


ZIP_INNER_ROOT = "2026_AI_Budget_Projects"

# (source_in_zip, dest_in_repo)
COPY_PLAN: list[tuple[str, str]] = [
    # Source data → data/raw/
    ("data/budget_533.xlsx", "data/raw/budget_533.xlsx"),
    ("data/예산현황_파싱_전체533건_교정.json",
     "data/raw/parsed_budget_533_corrected.json"),
    # RDF instance graph (schema lives separately at schema/bedo_v1.ttl)
    ("data/rdf/budget_graph_v2.ttl", "data/rdf/budget_graph_v2.ttl"),
    # Goldset
    ("data/goldset/query_logic_fullset.csv",
     "data/goldset/query_logic_fullset_original.csv"),
    ("data/goldset/query_logic_fullset_perturbed_v1.csv",
     "data/goldset/query_logic_fullset_perturbed_v1.csv"),
    ("data/goldset/perturbation_quality_check_v1.csv",
     "data/goldset/perturbation_quality_check_v1.csv"),
    # Predictions
    ("data/predictions/vector_predictions_perturbed_v1.csv",
     "data/predictions/vector_predictions_perturbed_v1.csv"),
    ("data/predictions/json_rag_predictions_perturbed_v1.csv",
     "data/predictions/json_rag_predictions_perturbed_v1.csv"),
    ("data/predictions/text_to_pandas_predictions_perturbed_v1.csv",
     "data/predictions/text_to_pandas_predictions_perturbed_v1.csv"),
    ("data/predictions/rdf_predictions_perturbed_v1.csv",
     "data/predictions/rdf_predictions_perturbed_v1.csv"),
    ("data/predictions/xlsx_predictions_perturbed_v1.csv",
     "data/predictions/xlsx_predictions_perturbed_v1.csv"),
    ("data/predictions/final_comparison_5methods_perturbed_v1.csv",
     "data/predictions/final_comparison_5methods_perturbed_v1.csv"),
    # Final summary tables (paper Tables 5-1, 5-3, 5-4)
    ("results/final/overall_summary_5methods_perturbed_v1.csv",
     "results/final/overall_summary_5methods_perturbed_v1.csv"),
    ("results/final/type_summary_5methods_perturbed_v1.csv",
     "results/final/type_summary_5methods_perturbed_v1.csv"),
    ("results/final/noise_level_summary_5methods_perturbed_v1.csv",
     "results/final/noise_level_summary_5methods_perturbed_v1.csv"),
    ("results/final/final_eval_long_5methods_perturbed_v1.csv",
     "results/final/final_eval_long_5methods_perturbed_v1.csv"),
    ("results/final/text_to_pandas_status_summary_v3.csv",
     "results/final/text_to_pandas_status_summary_v3.csv"),
    # Bootstrap (paper Table 5-2)
    ("results/bootstrap/paired_bootstrap_5methods_perturbed_v1_percent.csv",
     "results/bootstrap/paired_bootstrap_5methods_perturbed_v1_percent.csv"),
    ("results/bootstrap/paired_bootstrap_by_type_5methods_perturbed_v1_percent.csv",
     "results/bootstrap/paired_bootstrap_by_type_5methods_perturbed_v1_percent.csv"),
    # Figures
    ("figures/5method_perturbed_v1_results_en.png",
     "figures/5method_perturbed_v1_results_en.png"),
    # Logs
    ("logs/low_f1_plain_text_vector_rag.csv",
     "logs/low_f1_cases/low_f1_plain_text_vector_rag.csv"),
    ("logs/low_f1_text-to-pandas_agent.csv",
     "logs/low_f1_cases/low_f1_text-to-pandas_agent.csv"),
    ("logs/low_f1_rdf_template_sparql_v3.csv",
     "logs/low_f1_cases/low_f1_rdf_template_sparql_v3.csv"),
    ("logs/low_f1_xlsx_template_executor_v4.csv",
     "logs/low_f1_cases/low_f1_xlsx_template_executor_v4.csv"),
    ("logs/rdf_type_counts.csv", "logs/rdf_type_counts.csv"),
    ("logs/text_to_pandas_plan_diagnostics.csv",
     "logs/text_to_pandas_plan_diagnostics.csv"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("zip_path", type=Path,
                        help="Path to 5method_perturbed_v1_FINAL_*.zip")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(),
                        help="Target repository root (default: current dir)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print actions without copying")
    args = parser.parse_args()

    if not args.zip_path.exists():
        print(f"ERROR: ZIP not found: {args.zip_path}", file=sys.stderr)
        return 1

    repo_root = args.repo_root.resolve()
    print(f"Repo root: {repo_root}")
    print(f"ZIP file:  {args.zip_path}")

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        if not args.dry_run:
            print(f"Extracting ZIP to {tmpdir}...")
            with zipfile.ZipFile(args.zip_path, "r") as z:
                z.extractall(tmpdir)

        zip_root = tmpdir / ZIP_INNER_ROOT
        if not args.dry_run and not zip_root.exists():
            print(f"ERROR: expected inner root '{ZIP_INNER_ROOT}/' not found in ZIP",
                  file=sys.stderr)
            return 2

        copied, missing = 0, 0
        for src_rel, dst_rel in COPY_PLAN:
            src = zip_root / src_rel
            dst = repo_root / dst_rel

            if args.dry_run:
                print(f"[dry-run] {src_rel}  ->  {dst_rel}")
                copied += 1
                continue

            if not src.exists():
                print(f"  SKIP (missing in ZIP): {src_rel}")
                missing += 1
                continue

            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"  OK  {src_rel}  ->  {dst_rel}")
            copied += 1

    print(f"\nDone. {copied} files processed, {missing} missing.")
    if missing:
        print("Some files were missing from the ZIP — check the ZIP version.",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
