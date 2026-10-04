from pathlib import Path

import numpy as np
import pandas as pd


# ==================================================
# Project paths
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "analysis_sample.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "outputs"
    / "tables"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "table2_replication.csv"
)


# ==================================================
# Load processed data
# ==================================================

df = pd.read_csv(PROCESSED_DATA)

print("=" * 70)
print("ECO6067 - Card & Krueger (1994)")
print("Replication of Table 2 - Means of Key Variables")
print("=" * 70)


# ==================================================
# Additional variables required for Table 2
# ==================================================

# Percentage of full-time employees.
# This definition reproduces the values in the paper:
# EMPFT / FTE * 100.

df["PCT_FULLTIME_W1"] = np.where(
    df["FTE_BEFORE"] > 0,
    100 * df["EMPFT"] / df["FTE_BEFORE"],
    np.nan
)

df["PCT_FULLTIME_W2"] = np.where(
    df["FTE_AFTER"] > 0,
    100 * df["EMPFT2"] / df["FTE_AFTER"],
    np.nan
)


# Price of a full meal:
# medium soda + small fries + entree.

df["FULL_MEAL_W1"] = (
    df["PSODA"]
    + df["PFRY"]
    + df["PENTREE"]
)

df["FULL_MEAL_W2"] = (
    df["PSODA2"]
    + df["PFRY2"]
    + df["PENTREE2"]
)


# ==================================================
# Percentage indicators
# ==================================================

# Store-chain percentages.

df["PCT_BK"] = 100 * df["CHAIN"].eq(1).astype(float)
df["PCT_KFC"] = 100 * df["CHAIN"].eq(2).astype(float)
df["PCT_ROY"] = 100 * df["CHAIN"].eq(3).astype(float)
df["PCT_WENDYS"] = 100 * df["CHAIN"].eq(4).astype(float)

df["PCT_COMPANY_OWNED"] = (
    100 * df["CO_OWNED"].eq(1).astype(float)
)


# Wave 1 exact minimum-wage indicator.

df["WAGE_425_W1"] = (
    100 * df["WAGE_ST"].eq(4.25).astype(float)
)


# Wave 2 exact wage indicators.
# Only completed second-wave interviews count as an
# observed wage at exactly $4.25 or $5.05.

df["WAGE_425_W2"] = (
    100
    * (
        df["STATUS2"].eq(1)
        & df["WAGE_ST2"].eq(4.25)
    ).astype(float)
)

df["WAGE_505_W2"] = (
    100
    * (
        df["STATUS2"].eq(1)
        & df["WAGE_ST2"].eq(5.05)
    ).astype(float)
)


# Recruiting-program percentages.

df["BONUS_W1_PCT"] = 100 * df["BONUS"]

df["BONUS_W2_PCT"] = 100 * df["SPECIAL2"]


# ==================================================
# Summary function
# ==================================================

def summarise_variable(variable):

    nj = (
        df.loc[df["STATE"] == 1, variable]
        .dropna()
    )

    pa = (
        df.loc[df["STATE"] == 0, variable]
        .dropna()
    )

    nj_mean = nj.mean()
    pa_mean = pa.mean()

    nj_se = (
        nj.std(ddof=1) / np.sqrt(len(nj))
        if len(nj) > 1
        else np.nan
    )

    pa_se = (
        pa.std(ddof=1) / np.sqrt(len(pa))
        if len(pa) > 1
        else np.nan
    )

    se_difference = np.sqrt(
        nj_se ** 2 + pa_se ** 2
    )

    if se_difference > 0:
        t_stat = (
            (nj_mean - pa_mean)
            / se_difference
        )
    else:
        t_stat = np.nan

    return {
        "NJ_mean": nj_mean,
        "NJ_SE": nj_se,
        "PA_mean": pa_mean,
        "PA_SE": pa_se,
        "t_stat": t_stat,
        "N_NJ": len(nj),
        "N_PA": len(pa)
    }


# ==================================================
# Original Table 2 values
# ==================================================

table_specification = [

    # --------------------------------------------------
    # Distribution of store types
    # --------------------------------------------------

    (
        "1. Store types",
        "Burger King (%)",
        "PCT_BK",
        41.1,
        44.3,
        -0.5
    ),

    (
        "1. Store types",
        "KFC (%)",
        "PCT_KFC",
        20.5,
        15.2,
        1.2
    ),

    (
        "1. Store types",
        "Roy Rogers (%)",
        "PCT_ROY",
        24.8,
        21.5,
        0.6
    ),

    (
        "1. Store types",
        "Wendy's (%)",
        "PCT_WENDYS",
        13.6,
        19.0,
        -1.1
    ),

    (
        "1. Store types",
        "Company-owned (%)",
        "PCT_COMPANY_OWNED",
        34.1,
        35.4,
        -0.2
    ),


    # --------------------------------------------------
    # Wave 1
    # --------------------------------------------------

    (
        "2. Wave 1",
        "FTE employment",
        "FTE_BEFORE",
        20.4,
        23.3,
        -2.0
    ),

    (
        "2. Wave 1",
        "Full-time employees (%)",
        "PCT_FULLTIME_W1",
        32.8,
        35.0,
        -0.7
    ),

    (
        "2. Wave 1",
        "Starting wage",
        "WAGE_ST",
        4.61,
        4.63,
        -0.4
    ),

    (
        "2. Wave 1",
        "Wage = $4.25 (%)",
        "WAGE_425_W1",
        30.5,
        32.9,
        -0.4
    ),

    (
        "2. Wave 1",
        "Price of full meal",
        "FULL_MEAL_W1",
        3.35,
        3.04,
        4.0
    ),

    (
        "2. Wave 1",
        "Hours open",
        "HRSOPEN",
        14.4,
        14.5,
        -0.3
    ),

    (
        "2. Wave 1",
        "Recruiting bonus (%)",
        "BONUS_W1_PCT",
        23.6,
        29.1,
        -1.0
    ),


    # --------------------------------------------------
    # Wave 2
    # --------------------------------------------------

    (
        "3. Wave 2",
        "FTE employment",
        "FTE_AFTER",
        21.0,
        21.2,
        -0.2
    ),

    (
        "3. Wave 2",
        "Full-time employees (%)",
        "PCT_FULLTIME_W2",
        35.9,
        30.4,
        1.8
    ),

    (
        "3. Wave 2",
        "Starting wage",
        "WAGE_ST2",
        5.08,
        4.62,
        10.8
    ),

    (
        "3. Wave 2",
        "Wage = $4.25 (%)",
        "WAGE_425_W2",
        0.0,
        25.3,
        np.nan
    ),

    (
        "3. Wave 2",
        "Wage = $5.05 (%)",
        "WAGE_505_W2",
        85.2,
        1.3,
        36.1
    ),

    (
        "3. Wave 2",
        "Price of full meal",
        "FULL_MEAL_W2",
        3.41,
        3.03,
        5.0
    ),

    (
        "3. Wave 2",
        "Hours open",
        "HRSOPEN2",
        14.4,
        14.7,
        -0.8
    ),

    (
        "3. Wave 2",
        "Recruiting bonus (%)",
        "BONUS_W2_PCT",
        20.3,
        23.4,
        -0.6
    )
]


# ==================================================
# Build replication table
# ==================================================

results = []

for (
    section,
    label,
    variable,
    original_nj,
    original_pa,
    original_t
) in table_specification:

    stats = summarise_variable(variable)

    results.append({

        "Section": section,
        "Variable": label,

        "Replication_NJ":
            stats["NJ_mean"],

        "Replication_NJ_SE":
            stats["NJ_SE"],

        "Replication_PA":
            stats["PA_mean"],

        "Replication_PA_SE":
            stats["PA_SE"],

        "Replication_t":
            stats["t_stat"],

        "N_NJ":
            stats["N_NJ"],

        "N_PA":
            stats["N_PA"],

        "Original_NJ":
            original_nj,

        "Original_PA":
            original_pa,

        "Original_t":
            original_t,

        "Difference_NJ":
            stats["NJ_mean"] - original_nj,

        "Difference_PA":
            stats["PA_mean"] - original_pa
    })


table2 = pd.DataFrame(results)


# ==================================================
# Save output
# ==================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

table2.to_csv(
    OUTPUT_FILE,
    index=False,
    float_format="%.6f"
)


# ==================================================
# Display results
# ==================================================

display_columns = [
    "Section",
    "Variable",
    "Replication_NJ",
    "Original_NJ",
    "Replication_PA",
    "Original_PA",
    "Replication_t",
    "Original_t"
]

print("\nReplication results:")
print(
    table2[display_columns]
    .round(2)
    .to_string(index=False)
)

print("\nTable 2 saved to:")
print(OUTPUT_FILE)

print(
    "\nTable 2 replication completed successfully."
)
