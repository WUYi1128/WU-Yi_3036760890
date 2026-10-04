from pathlib import Path
import pandas as pd


# ==================================================
# Project paths
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA = PROJECT_ROOT / "data" / "raw" / "public.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DATA = PROCESSED_DIR / "analysis_sample.csv"


# ==================================================
# Load raw data
# ==================================================

df = pd.read_csv(RAW_DATA)

print("=" * 60)
print("ECO6067 - Card & Krueger (1994)")
print("Data Cleaning and Variable Construction")
print("=" * 60)

print(f"\nRaw dataset shape: {df.shape}")


# ==================================================
# Keep raw data unchanged
# ==================================================

analysis = df.copy()


# ==================================================
# Construct readable labels
# ==================================================

analysis["STATE_NAME"] = analysis["STATE"].map({
    0: "Pennsylvania",
    1: "New Jersey"
})

analysis["CHAIN_NAME"] = analysis["CHAIN"].map({
    1: "Burger King",
    2: "KFC",
    3: "Roy Rogers",
    4: "Wendy's"
})


# ==================================================
# Treatment indicator
# ==================================================

# New Jersey is the treatment group.
# Pennsylvania is the comparison group.

analysis["TREATMENT"] = analysis["STATE"]


# ==================================================
# Second-wave response indicator
# ==================================================

# STATUS2 = 1 means the restaurant answered
# the second-wave survey.

analysis["SECOND_WAVE_RESPONSE"] = (
    analysis["STATUS2"] == 1
).astype(int)


# ==================================================
# Construct employment measures
# ==================================================

# These variables retain the original components.
# A full-time-equivalent employment measure is
# constructed below and must be checked against
# the exact definition used in the original paper.

analysis["FTE_BEFORE"] = (
    analysis["EMPFT"]
    + analysis["NMGRS"]
    + 0.5 * analysis["EMPPT"]
)

analysis["FTE_AFTER"] = (
    analysis["EMPFT2"]
    + analysis["NMGRS2"]
    + 0.5 * analysis["EMPPT2"]
)


# ==================================================
# Employment change
# ==================================================

analysis["DELTA_FTE"] = (
    analysis["FTE_AFTER"] - analysis["FTE_BEFORE"]
)


# ==================================================
# Wage change
# ==================================================

analysis["DELTA_WAGE"] = (
    analysis["WAGE_ST2"] - analysis["WAGE_ST"]
)


# ==================================================
# Missing-value indicators
# ==================================================

analysis["FTE_BEFORE_MISSING"] = (
    analysis["FTE_BEFORE"].isna()
).astype(int)

analysis["FTE_AFTER_MISSING"] = (
    analysis["FTE_AFTER"].isna()
).astype(int)


# ==================================================
# Save processed data
# ==================================================

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

analysis.to_csv(
    PROCESSED_DATA,
    index=False
)


# ==================================================
# Validation checks
# ==================================================

print("\nProcessed dataset shape:")
print(analysis.shape)

print("\nTreatment group counts:")
print(
    analysis["STATE_NAME"]
    .value_counts(dropna=False)
)

print("\nSecond-wave response counts:")
print(
    analysis["SECOND_WAVE_RESPONSE"]
    .value_counts(dropna=False)
    .sort_index()
)

print("\nMissing FTE before:")
print(analysis["FTE_BEFORE"].isna().sum())

print("\nMissing FTE after:")
print(analysis["FTE_AFTER"].isna().sum())

print("\nSummary statistics for FTE measures:")
print(
    analysis[
        ["FTE_BEFORE", "FTE_AFTER", "DELTA_FTE"]
    ].describe()
)

print("\nProcessed data saved to:")
print(PROCESSED_DATA)

print("\nData cleaning completed successfully.")
