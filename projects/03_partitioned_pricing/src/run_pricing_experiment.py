import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Paths (beginner-friendly)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "synthetic_pricing_data.csv")
FIG_DIR = os.path.join(BASE_DIR, "reports", "figures")


def generate_data(n=2000, seed=123):
    rng = np.random.default_rng(seed)

    tiers = ["Low-ticket (<£50)", "High-ticket (>£200)"]
    frames = ["Combined (Free shipping)", "Partitioned (+Shipping)"]

    product_tier = rng.choice(tiers, size=n)
    pricing_frame = rng.choice(frames, size=n)

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
        "conversion": conversion,
    })


def main():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)

    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        df = generate_data()
        df.to_csv(DATA_PATH, index=False)

    # ATE figure
    g = df.groupby("pricing_frame")["conversion"]
    means = g.mean()
    counts = g.count()
    se = np.sqrt(means * (1 - means) / counts)
    ci = 1.96 * se

    plt.figure(figsize=(7.5, 4.8))
    plt.bar(means.index, means, yerr=ci, capsize=6, edgecolor="black")
    plt.title("Overall conversion by pricing frame (ATE)", loc="left")
    plt.ylabel("Conversion rate")
    plt.ylim(0, 0.15)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "overall_pricing_effect.png"), dpi=220, bbox_inches="tight")
    plt.close()

    # Interaction figure
    interaction = df.groupby(["product_tier", "pricing_frame"])["conversion"].mean().unstack()
    frames = ["Combined (Free shipping)", "Partitioned (+Shipping)"]
    x = [0, 1]

    low = "Low-ticket (<£50)"
    high = "High-ticket (>£200)"

    low_y = [interaction.loc[low, frames[0]], interaction.loc[low, frames[1]]]
    high_y = [interaction.loc[high, frames[0]], interaction.loc[high, frames[1]]]

    plt.figure(figsize=(8.2, 5.2))
    plt.plot(x, low_y, marker="o", linewidth=3, label=low)
    plt.plot(x, high_y, marker="s", linewidth=3, label=high)
    plt.title("Pricing frame × product tier (HTE)", loc="left")
    plt.ylabel("Conversion rate")
    plt.xticks(x, frames)
    plt.ylim(0, 0.15)
    plt.grid(axis="y", alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "interaction_effect_pricing.png"), dpi=220, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()
