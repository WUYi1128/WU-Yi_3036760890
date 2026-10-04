from pathlib import Path

import numpy as np
import pandas as pd


# ==================================================
# Project paths
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

TABLE_DIR = (
    PROJECT_ROOT
    / "outputs"
    / "tables"
)

OUTPUT_FILE = (
    TABLE_DIR
    / "validation_summary.csv"
)


# ==================================================
# Load replication outputs
# ==================================================

table2 = pd.read_csv(
    TABLE_DIR / "table2_replication.csv"
)

table3 = pd.read_csv(
    TABLE_DIR / "table3_replication.csv"
)

table4 = pd.read_csv(
    TABLE_DIR / "table4_replication.csv"
)

figure1 = pd.read_csv(
    TABLE_DIR / "figure1_wage_distribution.csv"
)


print("=" * 75)
print("ECO6067 - Replication Validation")
print("=" * 75)


# ==================================================
# Validation helper
# ==================================================

checks = []


def add_check(
    section,
    test,
    replication,
    benchmark,
    tolerance
):

    difference = replication - benchmark

    passed = (
        abs(difference)
        <= tolerance
    )

    checks.append({

        "Section":
            section,

        "Test":
            test,

        "Replication":
            replication,

        "Benchmark":
            benchmark,

        "Difference":
            difference,

        "Tolerance":
            tolerance,

        "Pass":
            passed
    })


# ==================================================
# Table 2 checks
# ==================================================

def table2_value(
    variable,
    column
):

    return float(
        table2.loc[
            table2["Variable"] == variable,
            column
        ].iloc[0]
    )


add_check(
    "Table 2",
    "Wave 1 NJ FTE",
    table2_value(
        "FTE employment",
        "Replication_NJ"
    ),
    20.44,
    0.02
)

# The first occurrence above is Wave 1.
# Select the second FTE employment row for Wave 2.

fte_rows = table2[
    table2["Variable"]
    == "FTE employment"
].reset_index(drop=True)

add_check(
    "Table 2",
    "Wave 1 PA FTE",
    float(
        fte_rows.loc[
            0,
            "Replication_PA"
        ]
    ),
    23.33,
    0.02
)

add_check(
    "Table 2",
    "Wave 2 NJ FTE",
    float(
        fte_rows.loc[
            1,
            "Replication_NJ"
        ]
    ),
    21.03,
    0.02
)

add_check(
    "Table 2",
    "Wave 2 PA FTE",
    float(
        fte_rows.loc[
            1,
            "Replication_PA"
        ]
    ),
    21.17,
    0.02
)


# ==================================================
# Table 3 checks
# ==================================================

def table3_value(
    row,
    column
):

    return float(
        table3.loc[
            (table3["Row"] == row)
            & (table3["Column"] == column),
            "Replication_Mean"
        ].iloc[0]
    )


add_check(
    "Table 3",
    "Main DiD",
    table3_value(
        3,
        "NJ - PA"
    ),
    2.76,
    0.02
)

add_check(
    "Table 3",
    "Balanced-sample DiD",
    table3_value(
        4,
        "NJ - PA"
    ),
    2.75,
    0.02
)

add_check(
    "Table 3",
    "Temporary-closure sensitivity",
    table3_value(
        5,
        "NJ - PA"
    ),
    2.51,
    0.02
)


# ==================================================
# Table 4 checks
# ==================================================

def table4_value(
    model,
    column
):

    return float(
        table4.loc[
            table4["Model"]
            == model,
            column
        ].iloc[0]
    )


add_check(
    "Table 4",
    "Model (i) NJ coefficient",
    table4_value(
        "(i)",
        "Replication_Coefficient"
    ),
    2.33,
    0.02
)

add_check(
    "Table 4",
    "Model (ii) NJ coefficient",
    table4_value(
        "(ii)",
        "Replication_Coefficient"
    ),
    2.30,
    0.02
)

add_check(
    "Table 4",
    "Model (iii) GAP coefficient",
    table4_value(
        "(iii)",
        "Replication_Coefficient"
    ),
    15.65,
    0.03
)

add_check(
    "Table 4",
    "Model (iv) GAP coefficient",
    table4_value(
        "(iv)",
        "Replication_Coefficient"
    ),
    14.92,
    0.03
)

# Model (v) is allowed a slightly larger tolerance
# because the published table description and the
# author-supplied checking specification differ
# regarding the ownership control.

add_check(
    "Table 4",
    "Model (v) GAP coefficient",
    table4_value(
        "(v)",
        "Replication_Coefficient"
    ),
    11.91,
    0.10
)


# ==================================================
# Figure 1 checks
# ==================================================

wave2_505 = figure1.loc[
    np.isclose(
        figure1["Wage_Range"],
        5.05
    )
].iloc[0]


add_check(
    "Figure 1",
    "Wave 2 NJ share near $5.05",
    float(
        wave2_505[
            "Wave2_NJ_Percent"
        ]
    ),
    89.62,
    0.05
)


# ==================================================
# Create validation summary
# ==================================================

validation = pd.DataFrame(
    checks
)


TABLE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

validation.to_csv(
    OUTPUT_FILE,
    index=False,
    float_format="%.6f"
)


# ==================================================
# Display results
# ==================================================

print("\nValidation results:")

print(
    validation
    .round(3)
    .to_string(index=False)
)


passed = int(
    validation["Pass"].sum()
)

total = len(
    validation
)


print(
    f"\nPassed checks: "
    f"{passed}/{total}"
)


if passed == total:

    print(
        "\nAll core replication checks passed."
    )

else:

    print(
        "\nWARNING: "
        "Some replication checks require review."
    )


print(
    "\nValidation summary saved to:"
)

print(
    OUTPUT_FILE
)

print(
    "\nValidation completed successfully."
)
