import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set paths (Beginner friendly way)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "synthetic_ab_test.csv")
FIG_DIR = os.path.join(BASE_DIR, "reports", "figures")

def generate_data():
    # Set seed
    np.random.seed(42)
    n = 800
    
    # 1. Assign groups randomly
    assigned_group = np.random.choice(["A", "B"], size=n)
    
    # 2. Participation (Drop-off)
    participated = []
    for group in assigned_group:
        if group == "A":
            participated.append(np.random.binomial(1, 0.72))
        else:
            participated.append(np.random.binomial(1, 0.68))
            
    # 3. Treatment received (Noncompliance)
    received_treatment = []
    for i in range(n):
        group = assigned_group[i]
        if group == "B":
            # 85% open rate for assigned group
            received_treatment.append(np.random.binomial(1, 0.85))
        else:
            # 5% spillover for control group
            received_treatment.append(np.random.binomial(1, 0.05))
            
    # 4. Purchase outcome
    purchase = []
    for i in range(n):
        if received_treatment[i] == 1:
            prob = 0.06 + 0.015 # Uplift
        else:
            prob = 0.06
            
        bought = np.random.binomial(1, prob)
        
        # Make some data missing
        if participated[i] == 1:
            missing_prob = 0.05
        else:
            missing_prob = 0.25
            
        is_missing = np.random.binomial(1, missing_prob)
        
        if is_missing == 1:
            purchase.append(np.nan)
        else:
            purchase.append(bought)
            
    # Create DataFrame
    df = pd.DataFrame({
        "user_id": range(1, n + 1),
        "assigned_group": assigned_group,
        "participated": participated,
        "received_treatment": received_treatment,
        "purchase": purchase
    })
    
    return df

def main():
    # Make folder if not exists
    if not os.path.exists(FIG_DIR):
        os.makedirs(FIG_DIR)

    # Load or generate data
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        df = generate_data()
        
    df_obs = df.dropna(subset=['purchase'])

    # --- 1. Participation Check ---
    grouped_part = df.groupby('assigned_group')['participated']
    part_mean = grouped_part.mean()
    part_count = grouped_part.count()
    
    # Calculate Standard Error and 95% CI manually
    part_se = np.sqrt(part_mean * (1 - part_mean) / part_count)
    part_ci = 1.96 * part_se
    
    plt.figure(figsize=(7, 5))
    plt.bar(["Control (A)", "Reserved Stock (B)"], part_mean, yerr=part_ci, capsize=5, color="skyblue", edgecolor="black")
    plt.title("Participation Balance Check")
    plt.ylabel("Participation Rate")
    plt.ylim(0, 1.0)
    
    for i in range(len(part_mean)):
        plt.text(i, part_mean[i] + 0.02, f"{round(part_mean[i], 3)}\n(n={part_count[i]})", ha='center')
        
    plt.savefig(os.path.join(FIG_DIR, "participation_rate_by_assignment.png"))
    plt.close()

    # --- 2. ITT (Intention-to-Treat) ---
    grouped_itt = df_obs.groupby('assigned_group')['purchase']
    itt_mean = grouped_itt.mean()
    itt_count = grouped_itt.count()
    
    itt_se = np.sqrt(itt_mean * (1 - itt_mean) / itt_count)
    itt_ci = 1.96 * itt_se
    
    plt.figure(figsize=(7, 5))
    plt.bar(["Control (A)", "Reserved Stock (B)"], itt_mean, yerr=itt_ci, capsize=5, color="skyblue", edgecolor="black")
    plt.title("ITT: Purchase rate by assigned group")
    plt.ylabel("Observed Purchase Rate")
    plt.ylim(0, 0.12)
    
    for i in range(len(itt_mean)):
        plt.text(i, itt_mean[i] + 0.005, f"{round(itt_mean[i], 3)}\n(n={itt_count[i]})", ha='center')
        
    plt.savefig(os.path.join(FIG_DIR, "itt_purchase_rate_by_assignment.png"))
    plt.close()

    # --- 3. As-Treated ---
    grouped_at = df_obs.groupby('received_treatment')['purchase']
    at_mean = grouped_at.mean()
    at_count = grouped_at.count()
    
    at_se = np.sqrt(at_mean * (1 - at_mean) / at_count)
    at_ci = 1.96 * at_se
    
    plt.figure(figsize=(7, 5))
    plt.bar(["Not Treated", "Treated"], at_mean, yerr=at_ci, capsize=5, color="skyblue", edgecolor="black")
    plt.title("As-Treated: Purchase rate by treatment received")
    plt.ylabel("Observed Purchase Rate")
    plt.ylim(0, 0.12)
    
    for i in range(len(at_mean)):
        val = list(at_mean)[i]
        n_val = list(at_count)[i]
        plt.text(i, val + 0.005, f"{round(val, 3)}\n(n={n_val})", ha='center')
        
    plt.savefig(os.path.join(FIG_DIR, "purchase_rate_by_treatment_received.png"))
    plt.close()
    
    print("Done! Check the figures folder.")

if __name__ == "__main__":
    main()
