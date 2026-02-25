"""Run A/B test summaries."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "data" / "synthetic_ab_test.csv"
FIG_DIR = PROJECT_DIR / "reports" / "figures"


def generate_synthetic_ab_data(n: int = 800, seed: int = 42) -> pd.DataFrame:
    """Generate a synthetic A/B test dataset."""
    rng = np.random.default_rng(seed)

    assigned = rng.choice(["A", "B"], size=n, p=[0.5, 0.5])

    # Drop-off differs slightly by assignment (e.g., message/channel differences)
    p_participate = np.where(assigned == "A", 0.72, 0.68)
    participated = rng.binomial(1, p_participate)

    # Noncompliance: not everyone assigned to B actually receives treatment;
    # some assigned to A may still receive it (spillover/mis-targeting).
    received_treatment = np.zeros(n, dtype=int)
    received_treatment[assigned == "B"] = rng.binomial(1, 0.85, size=(assigned == "B").sum())
    received_treatment[assigned == "A"] = rng.binomial(1, 0.05, size=(assigned == "A").sum())

    # Outcome model (simple): baseline + uplift if received treatment.
    # People who didn't participate have outcomes that are more likely to be missing.
    base_rate = 0.06
    uplift = 0.015
    purchase_prob = base_rate + uplift * received_treatment
    purchase = rng.binomial(1, np.clip(purchase_prob, 0, 1)).astype(float)

    # Attrition / missing outcomes: higher missingness among non-participants
    p_missing = np.where(participated == 1, 0.05, 0.25)
    missing = rng.binomial(1, p_missing).astype(bool)
    purchase[missing] = np.nan

    df = pd.DataFrame(
        {
            "user_id": np.arange(1, n + 1),
            "assigned_group": assigned,
            "participated": participated,
            "received_treatment": received_treatment,
            "purchase": purchase,
        }
    )
    return df


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
        print(f"Loaded CSV: {DATA_PATH}")
    else:
        df = generate_synthetic_ab_data()
        print("Generated synthetic data (CSV not found).")
    print(f"Rows: {len(df):,}")
    print(df.head(3))

    # Participation rate by assignment (drop-off after assignment)
    participation_rate = df.groupby("assigned_group")["participated"].mean().sort_index()
    print("\nParticipation rate by assigned group:")
    print(participation_rate)

    # Missing outcome rate by assignment (attrition / missing purchase values)
    missing_rate = df.groupby("assigned_group")["purchase"].apply(lambda s: s.isna().mean()).sort_index()
    print("\nMissing purchase rate by assigned group:")
    print(missing_rate)

    # ITT: purchase rate by assigned group (observed outcomes only)
    df_obs = df.dropna(subset=["purchase"])
    itt_rate = df_obs.groupby("assigned_group")["purchase"].mean().sort_index()
    print("\nITT purchase rate by assigned group (observed outcomes only):")
    print(itt_rate)

    # As-treated: purchase rate by whether treatment was actually received
    as_treated_rate = df_obs.groupby("received_treatment")["purchase"].mean().sort_index()
    print("\nAs-treated purchase rate (0=did not receive, 1=received):")
    print(as_treated_rate)

    # Figures (saved locally; .gitignore prevents committing images)
    plt.figure()
    participation_rate.plot(kind="bar")
    plt.ylim(0, 1)
    plt.ylabel("Participation rate")
    plt.title("Participation rate by assigned group")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "participation_rate_by_assignment.png", dpi=200)
    plt.close()

    plt.figure()
    itt_rate.plot(kind="bar")
    plt.ylim(0, max(0.1, float(itt_rate.max()) * 1.5))
    plt.ylabel("Observed purchase rate")
    plt.title("ITT: Purchase rate by assigned group (observed outcomes only)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "itt_purchase_rate_by_assignment.png", dpi=200)
    plt.close()

    plt.figure()
    as_treated_rate.plot(kind="bar")
    plt.ylim(0, max(0.1, float(as_treated_rate.max()) * 1.5))
    plt.ylabel("Observed purchase rate")
    plt.title("As-treated: Purchase rate by treatment received")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "purchase_rate_by_treatment_received.png", dpi=200)
    plt.close()

    print(f"\nSaved figures to: {FIG_DIR}")


if __name__ == "__main__":
    main()
