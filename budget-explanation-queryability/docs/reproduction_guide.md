# Reproduction Guide

This package supports saved-output reproduction.

## Step 1. Install dependencies

```bash
pip install -r requirements.txt
```

## Step 2. Validate artifacts

```bash
python src/validation/validate_artifacts.py
```

Expected result: all required artifacts exist and official F1 values match.

## Step 3. Reproduce summary tables

```bash
python src/evaluation/evaluate_saved_outputs.py
```

## Step 4. Reproduce paired bootstrap

```bash
python src/bootstrap/paired_bootstrap.py
```

## Note on raw LLM regeneration

Raw LLM response regeneration is not part of the deterministic reproduction path. The official paper results are reproduced from saved predictions and saved per-question evaluation files.
