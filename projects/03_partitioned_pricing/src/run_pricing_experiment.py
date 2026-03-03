"""
Project 03 — The "Partitioned Pricing" Experiment (Synthetic)

This script:
  1) Generates a deterministic synthetic dataset for a price-framing A/B test
  2) Saves the dataset to data/synthetic_pricing_data.csv
  3) Produces two figures in reports/figures/:
     - overall_pricing_effect.png (ATE-style summary)
     - interaction_effect_pricing.png (HTE crossover interaction)

Currency: GBP (£)
Results are synthetic and for portfolio demonstration only.
"""

from __future__ import annotations

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "synthetic_pricing_data.csv")
FIG_DIR = os.path.join(BASE_DIR, "reports", "figures")


def generate_data(n: int = 2000, seed: int = 123) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    tiers = ["Low-ticket (<£50)", "High-ticket (>£200)"]
    frames = ["Combined (Free shipping)", "Partitioned (+Shipping)"]

    product_tier = rng.choice(tiers, size=n, replace=True)
    pricing_frame = rng.choice(frames, size=n, replace=True)

    prob = np.zeros(n)
    for i in range(n):
        if product_tier[i] == "Low-ticket (<£50)":
            prob[i] = 0.08 if pricing_frame[i] == "Combined (Free shipping)" else 0.12
        else:
            prob[i] = 0.06 if pricing_frame[i] == "Combined (Free shipping)" else 0.02

    conversion = rng.binomial(1, prob, size=n)

    return pd.DataFrame({
        "user_id": np.arange(1, n + 1),
        "product_tier": product_tier,
        "pricing_frame": pricing_frame,
        "conversion": conversion
    })


def _ensure_dirs():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)


def main():
    _ensure_dirs()

    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        print("Loaded existing dataset.")
    else:
        df = generate_data()
        df.to_csv(DATA_PATH, index=False)
        print("Generated synthetic dataset.")

    print(f"Rows: {len(df):,}")

    # ---- ATE ----
    grouped = df.groupby("pricing_frame")["conversion"]
    means = grouped.mean()
    counts = grouped.count()

    se = np.sqrt(means * (1 - means) / counts)
    ci = 1.96 * se

    plt.figure(figsize=(7.5, 4.8))
    plt.bar(means.index, means, yerr=ci, capsize=6, edgecolor="black")
    plt.title("Overall Conversion by Pricing Frame (ATE)", loc="left")
    plt.ylabel("Conversion rate")
    plt.ylim(0, 0.15)

    for i, (m, n) in enumerate(zip(means.values, counts.values)):
        plt.text(i, m + 0.006, f"{m*100:.1f}%\n(n={int(n)})", ha="center")

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "overall_pricing_effect.png"), dpi=220)
    plt.close()

    # ---- HTE Interaction ----
    interaction = df.groupby(["product_tier", "pricing_frame"])["conversion"].mean().unstack()

    frames_order = ["Combined (Free shipping)", "Partitioned (+Shipping)"]
    x = [0, 1]

    low = "Low-ticket (<£50)"
    high = "High-ticket (>£200)"

    low_y = [interaction.loc[low, frames_order[0]], interaction.loc[low, frames_order[1]]]
    high_y = [interaction.loc[high, frames_order[0]], interaction.loc[high, frames_order[1]]]

    plt.figure(figsize=(8.2, 5.2))
    plt.plot(x, low_y, marker="o", linewidth=3, label=low)
    plt.plot(x, high_y, marker="s", linewidth=3, label=high)

    plt.title("HTE: Pricing Frame × Product Tier (Crossover)", loc="left")
    plt.ylabel("Conversion rate")
    plt.xticks(x, frames_order)
    plt.ylim(0, 0.15)
    plt.grid(axis="y", alpha=0.25)
    plt.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "interaction_effect_pricing.png"), dpi=220)
    plt.close()

    print("Figures saved.")


if __name__ == "__main__":
    main()
