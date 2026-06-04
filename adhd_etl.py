import pandas as pd
import os

# --- File paths ---
csv_folder = r"C:\Users\bryce\Desktop\Data Projects\Medical Projects\01 - ADHD in America\csv"

files = {
    "prevalence_historical":  "adhd_prevalence_historical.csv",
    "income_insurance":       "adhd_by_income_insurance.csv",
    "treatment_by_age":       "Treatment of ADHD by Age.csv",
    "treatment_by_sex":       "Treatment of ADHD by Sex.csv",
    "conditions_by_age":      "Other Concerns and Conditions with ADHD by Age.csv",
    "conditions_by_sex":      "Other Concerns and Conditions with ADHD by Sex.csv",
}

# --- Load all CSVs into a dictionary of dataframes ---
dfs = {}
for key, filename in files.items():
    path = os.path.join(csv_folder, filename)
    dfs[key] = pd.read_csv(path)
    print(f"\n=== {key} ===")
    print(dfs[key].head())
    print(f"Shape: {dfs[key].shape}")

    # --- Clean prevalence_historical ---
df_prev = dfs["prevalence_historical"].copy()
df_prev = df_prev.sort_values("year").reset_index(drop=True)
df_prev.columns = df_prev.columns.str.strip().str.lower().str.replace(" ", "_")
print("\n--- prevalence_historical cleaned ---")
print(df_prev)

# --- Clean treatment tables ---
df_treat_age = dfs["treatment_by_age"].copy()
df_treat_age.columns = ["treatment_type", "overall", "age_3_5", "age_6_11", "age_12_17"]

df_treat_sex = dfs["treatment_by_sex"].copy()
df_treat_sex.columns = ["treatment_type", "overall", "boys", "girls"]

print("\n--- treatment_by_age cleaned ---")
print(df_treat_age)

print("\n--- treatment_by_sex cleaned ---")
print(df_treat_sex)

# --- Clean conditions tables ---
df_cond_age = dfs["conditions_by_age"].copy()
df_cond_age.columns = df_cond_age.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("/", "_")

df_cond_sex = dfs["conditions_by_sex"].copy()
df_cond_sex.columns = df_cond_sex.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("/", "_")

print("\n--- conditions_by_age cleaned ---")
print(df_cond_age)

# --- Clean income/insurance ---
df_income = dfs["income_insurance"].copy()
df_income.columns = df_income.columns.str.strip().str.lower().str.replace(" ", "_")
print("\n--- income_insurance cleaned ---")
print(df_income)

import sqlite3

# --- Database path ---
db_path = r"C:\Users\bryce\Desktop\Data Projects\Medical Projects\01 - ADHD in America\adhd_america.db"

conn = sqlite3.connect(db_path)

# --- Fix remaining column name issue ---
df_cond_age.columns = df_cond_age.columns.str.replace("-", "_")
df_cond_sex.columns = df_cond_sex.columns.str.replace("-", "_")

treatment_labels = {
    "Currently taking ADHD medication": "Taking Medication",
    "Received behavioral treatment for ADHD (in the past 12 months)": "Behavioral Treatment Only",
    "Received behavioral treatment for ADHD or any treatment/counseling from a mental health provider (in the past 12 months)": "Any Treatment or Counseling"
}

df_treat_age["treatment_type"] = df_treat_age["treatment_type"].replace(treatment_labels)
df_treat_sex["treatment_type"] = df_treat_sex["treatment_type"].replace(treatment_labels)

# Add sort column for age group ordering
age_order = {"5-11": 1, "12-17": 2, "5-17": 3}
df_income["age_sort"] = df_income["age_group"].map(age_order)

# --- Write all tables to SQLite ---
df_prev.to_sql("prevalence_historical", conn, if_exists="replace", index=False)
df_income.to_sql("income_insurance", conn, if_exists="replace", index=False)
df_treat_age.to_sql("treatment_by_age", conn, if_exists="replace", index=False)
df_treat_sex.to_sql("treatment_by_sex", conn, if_exists="replace", index=False)
df_cond_age.to_sql("conditions_by_age", conn, if_exists="replace", index=False)
df_cond_sex.to_sql("conditions_by_sex", conn, if_exists="replace", index=False)

conn.close()

print("\nAll tables written to adhd_america.db successfully")