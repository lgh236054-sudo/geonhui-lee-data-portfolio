# Project 02 — Seoul 119 Rescue Activity (Public Data EDA)

Exploratory analysis of rescue-activity records in Seoul (2021). Focus: **cleaning decisions**, **feature engineering** (dispatch delay), and transparent descriptive reporting (no causal claims).

## Data source
- Korea Public Data Portal (data.go.kr) — National Fire Agency “Rescue Activity Status” (annual extract).
- The original dataset should be downloaded from the portal (see link below).

Suggested dataset page:
- https://www.data.go.kr/data/15062386/fileData.do

## Included (code-only)
- Notebook: `notebooks/02_fire_rescue_public_data.ipynb`
- Script: `src/run_analysis.py`
- Utilities: `src/utils.py`

> Note: This repository is intentionally **code-only** (no CSV committed).  
> To run locally, place your dataset (or a Seoul-only subset) at:
> `projects/02_fire_rescue_public_data/data/fire_rescue_seoul_2021.csv`

## Run locally
From the repository root:
```bash
pip install -r requirements.txt
python projects/02_fire_rescue_public_data/src/run_analysis.py
```

Outputs (figures) are saved locally to `projects/02_fire_rescue_public_data/reports/figures/` and are ignored by `.gitignore`.
