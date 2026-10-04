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
    / "table3_replication.csv"
)


# ==================================================
# Load processed data
# ==================================================

df = pd.read_csv(PROCESSED_DATA)

print("=" * 75)
print("ECO6067 - Card & Krueger (1994)")
print("Replication of Table 3 - Employment Before and After")
print("=" * 75)


# ==================================================
# Construct New Jersey wage groups
# ==================================================

df["WAGE_GROUP"] = pd.Series(
    pd.NA,
    index=df.index,
    dtype="string"
)

df.loc[
    (df["STATE"] == 1)
    & (df["WAGE_ST"] == 4.25),
    "WAGE_GROUP"
] = "Low ($4.25)"

df.loc[
    (df["STATE"] == 1)
    & (df["WAGE_ST"] > 4.25)
    & (df["WAGE_ST"] < 5.00),
    "WAGE_GROUP"
] = "Mid ($4.26-$4.99)"

df.loc[
    (df["STATE"] == 1)
    & (df["WAGE_ST"] >= 5.00),
    "WAGE_GROUP"
] = "High ($5.00+)"


# ==================================================
# Check wage-group sample sizes
# ==================================================

print("\nNew Jersey wage-group counts:")
print(
    df.loc[df["STATE"] == 1, "WAGE_GROUP"]
    .value_counts(dropna=False)
)

# Expected from the original paper:
# Low  = 101
# Mid  = 140
# High = 73


# ==================================================
# Balanced-sample employment change
# ==================================================

df["CHANGE_FTE_BALANCED"] = (
    df["FTE_AFTER"] - df["FTE_BEFORE"]
)


# ==================================================
# Temporary closures set to zero
# ==================================================

# STATUS2:
# 2 = renovation closure
# 4 = highway-construction closure
# 5 = mall-fire closure
#
# These are temporary closures.

temporary_closure = df["STATUS2"].isin([2, 4, 5])

df["FTE_AFTER_TEMP0"] = df["FTE_AFTER"].copy()

df.loc[
    temporary_closure,
    "FTE_AFTER_TEMP0"
] = 0

df["CHANGE_FTE_TEMP0"] = (
    df["FTE_AFTER_TEMP0"]
    - df["FTE_BEFORE"]
)


# ==================================================
# Group masks
# ==================================================

masks = {

    "PA":
        df["STATE"] == 0,

    "NJ":
        df["STATE"] == 1,

    "NJ Low":
        (
            (df["STATE"] == 1)
            & (df["WAGE_GROUP"] == "Low ($4.25)")
        ),

    "NJ Mid":
        (
            (df["STATE"] == 1)
            & (df["WAGE_GROUP"] == "Mid ($4.26-$4.99)")
        ),

    "NJ High":
        (
            (df["STATE"] == 1)
            & (df["WAGE_GROUP"] == "High ($5.00+)")
        )
}


# ==================================================
# Helper functions
# ==================================================

def mean_se(series):

    values = series.dropna().astype(float)

    n = len(values)

    if n == 0:
        return np.nan, np.nan, 0

    mean = values.mean()

    if n > 1:
        se = (
            values.std(ddof=1)
            / np.sqrt(n)
        )
    else:
        se = np.nan

    return mean, se, n


def calculate_direct(variable):

    result = {}

    for name, mask in masks.items():

        mean, se, n = mean_se(
            df.loc[mask, variable]
        )

        result[name] = {
            "mean": mean,
            "se": se,
            "n": n
        }

    # NJ minus PA
    result["NJ - PA"] = {

        "mean":
            result["NJ"]["mean"]
            - result["PA"]["mean"],

        "se":
            np.sqrt(
                result["NJ"]["se"] ** 2
                + result["PA"]["se"] ** 2
            ),

        "n": np.nan
    }

    # Low minus high
    result["Low - High"] = {

        "mean":
            result["NJ Low"]["mean"]
            - result["NJ High"]["mean"],

        "se":
            np.sqrt(
                result["NJ Low"]["se"] ** 2
                + result["NJ High"]["se"] ** 2
            ),

        "n": np.nan
    }

    # Mid minus high
    result["Mid - High"] = {

        "mean":
            result["NJ Mid"]["mean"]
            - result["NJ High"]["mean"],

        "se":
            np.sqrt(
                result["NJ Mid"]["se"] ** 2
                + result["NJ High"]["se"] ** 2
            ),

        "n": np.nan
    }

    return result


# ==================================================
# Row 1: FTE before
# ==================================================

row1 = calculate_direct(
    "FTE_BEFORE"
)


# ==================================================
# Row 2: FTE after
# ==================================================

row2 = calculate_direct(
    "FTE_AFTER"
)


# ==================================================
# Row 3: Change in mean FTE
# ==================================================

# The point estimate is the difference between
# the wave-2 and wave-1 means using all available
# observations in each wave.

row3 = {}

for name in masks.keys():

    row3[name] = {

        "mean":
            row2[name]["mean"]
            - row1[name]["mean"],

        # The original paper reports SEs for this row,
        # but the exact historical calculation is not
        # uniquely recoverable from the supplied data
        # and table notes alone.
        #
        # We therefore reproduce the point estimates
        # directly and retain the original paper SE
        # separately as a benchmark below.
        "se": np.nan,

        "n": np.nan
    }


row3["NJ - PA"] = {

    "mean":
        row3["NJ"]["mean"]
        - row3["PA"]["mean"],

    "se": np.nan,

    "n": np.nan
}


row3["Low - High"] = {

    "mean":
        row3["NJ Low"]["mean"]
        - row3["NJ High"]["mean"],

    "se": np.nan,

    "n": np.nan
}


row3["Mid - High"] = {

    "mean":
        row3["NJ Mid"]["mean"]
        - row3["NJ High"]["mean"],

    "se": np.nan,

    "n": np.nan
}


# ==================================================
# Row 4: Balanced sample
# ==================================================

row4 = calculate_direct(
    "CHANGE_FTE_BALANCED"
)


# ==================================================
# Row 5: Temporary closures set to zero
# ==================================================

row5 = calculate_direct(
    "CHANGE_FTE_TEMP0"
)


# ==================================================
# Original Table 3 benchmarks
# ==================================================

columns_order = [
    "PA",
    "NJ",
    "NJ - PA",
    "NJ Low",
    "NJ Mid",
    "NJ High",
    "Low - High",
    "Mid - High"
]


original_means = {

    1: [
        23.33,
        20.44,
        -2.89,
        19.56,
        20.08,
        22.25,
        -2.69,
        -2.17
    ],

    2: [
        21.17,
        21.03,
        -0.14,
        20.88,
        20.96,
        20.21,
        0.67,
        0.75
    ],

    3: [
        -2.16,
        0.59,
        2.76,
        1.32,
        0.87,
        -2.04,
        3.36,
        2.91
    ],

    4: [
        -2.28,
        0.47,
        2.75,
        1.21,
        0.71,
        -2.16,
        3.36,
        2.87
    ],

    5: [
        -2.28,
        0.23,
        2.51,
        0.90,
        0.49,
        -2.39,
        3.29,
        2.88
    ]
}


original_se = {

    1: [
        1.35,
        0.51,
        1.44,
        0.77,
        0.84,
        1.14,
        1.37,
        1.41
    ],

    2: [
        0.94,
        0.52,
        1.07,
        1.01,
        0.76,
        1.03,
        1.44,
        1.27
    ],

    3: [
        1.25,
        0.54,
        1.36,
        0.95,
        0.84,
        1.14,
        1.48,
        1.41
    ],

    4: [
        1.25,
        0.48,
        1.34,
        0.82,
        0.69,
        1.01,
        1.30,
        1.22
    ],

    5: [
        1.25,
        0.49,
        1.35,
        0.87,
        0.69,
        1.02,
        1.34,
        1.23
    ]
}


row_labels = {

    1:
        "FTE employment before, all available observations",

    2:
        "FTE employment after, all available observations",

    3:
        "Change in mean FTE employment",

    4:
        "Change in mean FTE employment, balanced sample",

    5:
        "Change in mean FTE employment, temporary closures = 0"
}


rows = {
    1: row1,
    2: row2,
    3: row3,
    4: row4,
    5: row5
}


# ==================================================
# Build long-format comparison table
# ==================================================

results = []

for row_number, row_results in rows.items():

    for j, column in enumerate(columns_order):

        replication_mean = (
            row_results[column]["mean"]
        )

        replication_se = (
            row_results[column]["se"]
        )

        original_mean = (
            original_means[row_number][j]
        )

        original_standard_error = (
            original_se[row_number][j]
        )

        results.append({

            "Row":
                row_number,

            "Description":
                row_labels[row_number],

            "Column":
                column,

            "Replication_Mean":
                replication_mean,

            "Original_Mean":
                original_mean,

            "Mean_Difference":
                replication_mean
                - original_mean,

            "Replication_SE":
                replication_se,

            "Original_SE":
                original_standard_error,

            "N":
                row_results[column]["n"]
        })


table3 = pd.DataFrame(results)


# ==================================================
# Save Table 3
# ==================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

table3.to_csv(
    OUTPUT_FILE,
    index=False,
    float_format="%.6f"
)


# ==================================================
# Display replicated means
# ==================================================

display_table = (
    table3
    .pivot(
        index="Description",
        columns="Column",
        values="Replication_Mean"
    )
    .reindex(
        columns=columns_order
    )
)


print("\nReplicated Table 3 means:")
print(
    display_table
    .round(2)
    .to_string()
)


# ==================================================
# Display key DiD results
# ==================================================

print("\nKey difference-in-differences results:")

for row_number in [3, 4, 5]:

    value = table3.loc[
        (table3["Row"] == row_number)
        & (table3["Column"] == "NJ - PA"),
        "Replication_Mean"
    ].iloc[0]

    original = table3.loc[
        (table3["Row"] == row_number)
        & (table3["Column"] == "NJ - PA"),
        "Original_Mean"
    ].iloc[0]

    print(
        f"Row {row_number}: "
        f"Replication = {value:.2f}, "
        f"Original = {original:.2f}"
    )


print("\nTable 3 saved to:")
print(OUTPUT_FILE)

print(
    "\nTable 3 replication completed successfully."
)
