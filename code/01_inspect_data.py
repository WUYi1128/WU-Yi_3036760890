from pathlib import Path
import pandas as pd


# ==================================================
# Project paths
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA = PROJECT_ROOT / "data" / "raw" / "public.csv"


# ==================================================
# Load raw data
# ==================================================

df = pd.read_csv(RAW_DATA)


# ==================================================
# Basic dataset checks
# ==================================================

print("=" * 60)
print("ECO6067 - Card & Krueger (1994)")
print("Raw Data Inspection")
print("=" * 60)


print("\n1. Dataset shape")
print(df.shape)


print("\n2. Column names")
print(df.columns.tolist())


print("\n3. First five observations")
print(df.head())


print("\n4. State counts")
print(df["STATE"].value_counts(dropna=False).sort_index())


print("\n5. Restaurant chain counts")
print(df["CHAIN"].value_counts(dropna=False).sort_index())


print("\n6. Second-wave survey status")
print(df["STATUS2"].value_counts(dropna=False).sort_index())


# ==================================================
# Missing values in important variables
# ==================================================

key_vars = [
    "EMPFT",
    "EMPPT",
    "NMGRS",
    "WAGE_ST",
    "EMPFT2",
    "EMPPT2",
    "NMGRS2",
    "WAGE_ST2",
]

print("\n7. Missing values in key variables")
print(df[key_vars].isna().sum())


# ==================================================
# Basic descriptive statistics
# ==================================================

print("\n8. Descriptive statistics for key variables")
print(df[key_vars].describe())


print("\nData inspection completed successfully.")
