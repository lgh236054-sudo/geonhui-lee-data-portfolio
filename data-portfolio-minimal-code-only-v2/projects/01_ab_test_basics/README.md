# Project 01 — A/B Test Basics (assignment vs treatment)

A beginner-friendly A/B testing example showing how **drop-off** (assigned → participated), **noncompliance** (assigned ≠ received), and **missing outcomes** can change what “the effect” means.

## Included
- Notebook: `notebooks/01_ab_test_basics.ipynb`
- Script: `src/run_analysis.py`
- Data: **synthetic** (no proprietary data)

> Note: This repository is intentionally **code-only** (no CSV committed).  
> The script will generate a small synthetic dataset automatically if the CSV is missing.

## Run locally
From the repository root:
```bash
pip install -r requirements.txt
python projects/01_ab_test_basics/src/run_analysis.py
```

(Optional) The script saves figures to `projects/01_ab_test_basics/reports/figures/` — keep them locally and do not commit them (images are ignored by `.gitignore`).
