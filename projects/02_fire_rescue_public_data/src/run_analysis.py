"""Run Project 02 and save figures."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from utils import (
    COL_CATEGORY,
    add_time_features,
    apply_basic_qc,
    load_seoul_data,
    translate_categories,
)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "fire_rescue_seoul_2021.csv"
    out_dir = project_root / "reports" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    if not data_path.exists():
        raise FileNotFoundError(f"Missing data file: {data_path}")

    df = load_seoul_data(data_path)
    df = add_time_features(df)
    df = apply_basic_qc(df)

    # Translate categories for readable plots (Korean → English)
    df = translate_categories(df)

    # 1) Monthly volume
    monthly = df.groupby("month")["case_id"].count()
    plt.figure()
    monthly.plot()
    plt.title("Monthly rescue activity volume (Seoul, 2021)")
    plt.ylabel("Number of cases")
    plt.tight_layout()
    plt.savefig(out_dir / "monthly_volume.png", dpi=200)
    plt.close()

    # 2) Top categories
    top = df[COL_CATEGORY].value_counts().head(12).sort_values()
    plt.figure()
    top.plot(kind="barh")
    plt.title("Top incident categories (Seoul, 2021)")
    plt.xlabel("Number of cases")
    plt.tight_layout()
    plt.savefig(out_dir / "top_categories.png", dpi=200)
    plt.close()

    print(f"Saved figures to: {out_dir}")


if __name__ == "__main__":
    main()
