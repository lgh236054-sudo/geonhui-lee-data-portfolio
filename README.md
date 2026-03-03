# Applied Data & Inference Portfolio - Code Repository

This repository contains the Python code, data generation pipelines, and analytical Jupyter notebooks for my portfolio projects. 

For full write-ups, visualisations, and behavioural/business interpretations, please visit my **[Notion Portfolio](https://bit.ly/GeonhuiLee_DataPortfolio)**.

---

## 📂 Projects

### **Project 01: The "Reserved Stock" Experiment (Handling Noncompliance)**
* **Path:** `projects/01_ab_test_basics/`
* **Focus:** Causal inference in field A/B tests with one-sided noncompliance.
* **Key Methods:** Synthetic data generation, Intention-to-Treat (ITT) vs. As-Treated analysis, selection bias evaluation.

### **Project 02: Seoul 119 Rescue Activity (Public Data EDA)**
* **Path:** `projects/02_fire_rescue_public_data/`
* **Focus:** Measurement construction and data quality control in large administrative event data.
* **Key Methods:** Data cleaning, temporal heatmaps, handling extreme outliers (clipping), descriptive statistics.

### **Project 03: The "Partitioned Pricing" Experiment (Heterogeneous Treatment Effects)**
* **Path:** `projects/03_partitioned_pricing/`
* **Focus:** Behavioural choice architecture and the danger of relying solely on average treatment effects (ATE).
* **Key Methods:** Synthetic A/B test simulation, Heterogeneous Treatment Effects (HTE), crossover interaction analysis.

---

## 🚀 How to Run

**1. Clone the repository and install dependencies:**
```bash
git clone [https://github.com/lgh236054-sudo/geonhui-lee-data-portfolio.git](https://github.com/lgh236054-sudo/geonhui-lee-data-portfolio.git)
cd geonhui-lee-data-portfolio
pip install -r requirements.txt
