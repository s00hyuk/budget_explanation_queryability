#!/usr/bin/env bash
set -euo pipefail
python src/validation/validate_artifacts.py
python src/evaluation/evaluate_saved_outputs.py
python src/bootstrap/paired_bootstrap.py
