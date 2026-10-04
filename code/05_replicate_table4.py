from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


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
    / "table4_replication.csv"
)


# ==================================================
# Load processed data
# ==================================================

df = pd.read_csv(PROCESSED_DATA)

print("=" * 75)
print("ECO6067 - Card & Krueger (1994)")
print("Replication of Table 4 - Reduced-Form Employment Models")
print("=" * 75)


# ==================================================
# Construct Table 4 employment change
# ==================================================

# Permanently closed stores have wave-2 employment = 0.

df["FTE_AFTER_T4"] = df["FTE_AFTER"].copy()

df.loc[
    df["STATUS2"] == 3,
    "FTE_AFTER_T4"
] = 0.0


df["DEMP"] = (
    df["FTE_AFTER_T4"]
    - df["FTE_BEFORE"]
)


# Wage change is used to identify stores
# with valid wage information in both waves.

df["DWAGE"] = (
    df["WAGE_ST2"]
    - df["WAGE_ST"]
)


# Permanent closure indicator.

df["CLOSED"] = (
    df["STATUS2"] == 3
).astype(int)


# ==================================================
# Construct the Table 4 estimation sample
# ==================================================

# Card and Krueger's supplied checking logic:
#
# 1. Employment change must be observed.
# 2. Permanently closed stores are retained.
# 3. Non-closed stores must have valid wage
#    information in both waves.

sample = df[
    df["DEMP"].notna()
].copy()

sample = sample[
    (sample["CLOSED"] == 1)
    |
    (
        (sample["CLOSED"] == 0)
        & sample["DWAGE"].notna()
    )
].copy()


# ==================================================
# Construct GAP
# ==================================================

sample["GAP"] = 0.0

gap_mask = (
    (sample["STATE"] == 1)
    & sample["WAGE_ST"].notna()
    & (sample["WAGE_ST"] > 0)
    & (sample["WAGE_ST"] < 5.05)
)

sample.loc[
    gap_mask,
    "GAP"
] = (
    5.05
    - sample.loc[gap_mask, "WAGE_ST"]
) / sample.loc[gap_mask, "WAGE_ST"]


# ==================================================
# Chain indicators
# ==================================================

# Wendy's is the omitted chain category.

sample["BK"] = (
    sample["CHAIN"] == 1
).astype(int)

sample["KFC"] = (
    sample["CHAIN"] == 2
).astype(int)

sample["ROYS"] = (
    sample["CHAIN"] == 3
).astype(int)


# ==================================================
# Validate estimation sample
# ==================================================

print("\nTable 4 estimation sample:")

print(
    f"Number of stores: {len(sample)}"
)

print(
    f"Mean employment change: "
    f"{sample['DEMP'].mean():.3f}"
)

print(
    f"SD employment change: "
    f"{sample['DEMP'].std(ddof=1):.3f}"
)

print(
    f"Mean GAP among NJ stores: "
    f"{sample.loc[sample['STATE'] == 1, 'GAP'].mean():.3f}"
)


# ==================================================
# Estimate the five published specifications
# ==================================================

# Model (i):
# Change in employment on New Jersey dummy.

model1 = smf.ols(
    "DEMP ~ STATE",
    data=sample
).fit()


# Model (ii):
# NJ dummy + chain + ownership controls.

model2 = smf.ols(
    "DEMP ~ STATE + BK + KFC + ROYS + CO_OWNED",
    data=sample
).fit()


# Model (iii):
# Initial wage GAP only.

model3 = smf.ols(
    "DEMP ~ GAP",
    data=sample
).fit()


# Model (iv):
# GAP + chain + ownership.

model4 = smf.ols(
    "DEMP ~ GAP + BK + KFC + ROYS + CO_OWNED",
    data=sample
).fit()


# Model (v):
# GAP + chain + ownership + region controls.
#
# North New Jersey is the omitted NJ region.
# The regional controls are therefore:
# CENTRALJ, SOUTHJ, PA1 and PA2.

model5 = smf.ols(
    "DEMP ~ GAP + BK + KFC + ROYS + "
    "CO_OWNED + CENTRALJ + SOUTHJ + PA1 + PA2",
    data=sample
).fit()


models = {
    "(i)": model1,
    "(ii)": model2,
    "(iii)": model3,
    "(iv)": model4,
    "(v)": model5
}


# ==================================================
# Joint F-test helper
# ==================================================

def joint_control_pvalue(model, variables):

    available = [
        variable
        for variable in variables
        if variable in model.params.index
    ]

    if len(available) == 0:
        return np.nan

    hypothesis = ", ".join(
        f"{variable} = 0"
        for variable in available
    )

    test = model.f_test(hypothesis)

    return float(
        np.asarray(test.pvalue).item()
    )


chain_ownership_controls = [
    "BK",
    "KFC",
    "ROYS",
    "CO_OWNED"
]

all_controls_model5 = [
    "BK",
    "KFC",
    "ROYS",
    "CO_OWNED",
    "CENTRALJ",
    "SOUTHJ",
    "PA1",
    "PA2"
]


p_control_2 = joint_control_pvalue(
    model2,
    chain_ownership_controls
)

p_control_4 = joint_control_pvalue(
    model4,
    chain_ownership_controls
)

p_control_5 = joint_control_pvalue(
    model5,
    all_controls_model5
)


# ==================================================
# Published Table 4 benchmarks
# ==================================================

original = {

    "(i)": {
        "variable": "STATE",
        "coefficient": 2.33,
        "se": 1.19,
        "ser": 8.79,
        "controls_p": np.nan,
        "chain_ownership": "No",
        "region": "No"
    },

    "(ii)": {
        "variable": "STATE",
        "coefficient": 2.30,
        "se": 1.20,
        "ser": 8.78,
        "controls_p": 0.34,
        "chain_ownership": "Yes",
        "region": "No"
    },

    "(iii)": {
        "variable": "GAP",
        "coefficient": 15.65,
        "se": 6.08,
        "ser": 8.76,
        "controls_p": np.nan,
        "chain_ownership": "No",
        "region": "No"
    },

    "(iv)": {
        "variable": "GAP",
        "coefficient": 14.92,
        "se": 6.21,
        "ser": 8.76,
        "controls_p": 0.44,
        "chain_ownership": "Yes",
        "region": "No"
    },

    "(v)": {
        "variable": "GAP",
        "coefficient": 11.91,
        "se": 7.39,
        "ser": 8.75,
        "controls_p": 0.40,
        "chain_ownership": "Yes",
        "region": "Yes"
    }
}


replication_pvalues = {
    "(i)": np.nan,
    "(ii)": p_control_2,
    "(iii)": np.nan,
    "(iv)": p_control_4,
    "(v)": p_control_5
}


# ==================================================
# Build comparison table
# ==================================================

records = []

for model_name, model in models.items():

    benchmark = original[model_name]

    variable = benchmark["variable"]

    replication_coefficient = (
        model.params[variable]
    )

    replication_se = (
        model.bse[variable]
    )

    replication_ser = np.sqrt(
        model.scale
    )

    replication_p = (
        replication_pvalues[model_name]
    )

    records.append({

        "Model":
            model_name,

        "Main_Variable":
            variable,

        "Replication_Coefficient":
            replication_coefficient,

        "Original_Coefficient":
            benchmark["coefficient"],

        "Coefficient_Difference":
            replication_coefficient
            - benchmark["coefficient"],

        "Replication_SE":
            replication_se,

        "Original_SE":
            benchmark["se"],

        "SE_Difference":
            replication_se
            - benchmark["se"],

        "Chain_and_Ownership_Controls":
            benchmark["chain_ownership"],

        "Region_Controls":
            benchmark["region"],

        "Replication_SER":
            replication_ser,

        "Original_SER":
            benchmark["ser"],

        "Replication_Control_P":
            replication_p,

        "Original_Control_P":
            benchmark["controls_p"],

        "N":
            int(model.nobs)
    })


table4 = pd.DataFrame(records)


# ==================================================
# Author-supplied check.sas diagnostic
# ==================================================

# The author-supplied checking script's Model (v)
# omits CO_OWNED even though the published table
# describes chain-and-ownership controls as included.
#
# We estimate this specification only as a diagnostic.

model5_checksas = smf.ols(
    "DEMP ~ GAP + BK + KFC + ROYS + "
    "CENTRALJ + SOUTHJ + PA1 + PA2",
    data=sample
).fit()


# ==================================================
# Save results
# ==================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

table4.to_csv(
    OUTPUT_FILE,
    index=False,
    float_format="%.6f"
)


# ==================================================
# Display results
# ==================================================

display_columns = [
    "Model",
    "Main_Variable",
    "Replication_Coefficient",
    "Original_Coefficient",
    "Replication_SE",
    "Original_SE",
    "Replication_SER",
    "Original_SER",
    "Replication_Control_P",
    "Original_Control_P",
    "N"
]

print("\nReplicated Table 4:")
print(
    table4[display_columns]
    .round(3)
    .to_string(index=False)
)


print(
    "\nAuthor check.sas Model (v) diagnostic:"
)

print(
    f"GAP coefficient = "
    f"{model5_checksas.params['GAP']:.2f}"
)

print(
    f"Standard error = "
    f"{model5_checksas.bse['GAP']:.2f}"
)


print("\nTable 4 saved to:")
print(OUTPUT_FILE)

print(
    "\nTable 4 replication completed successfully."
)
