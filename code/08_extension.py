from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

TABLE_DIR = (
    PROJECT_ROOT
    / "outputs"
    / "tables"
)

FIGURE_DIR = (
    PROJECT_ROOT
    / "outputs"
    / "figures"
)

TABLE_FILE = (
    TABLE_DIR
    / "extension_chain_did.csv"
)

TEST_FILE = (
    TABLE_DIR
    / "extension_chain_heterogeneity_test.csv"
)

FIGURE_FILE = (
    FIGURE_DIR
    / "extension_chain_did.png"
)


# ==================================================
# Load processed data
# ==================================================

df = pd.read_csv(PROCESSED_DATA)

print("=" * 78)
print("ECO6067 - Independent Extension")
print("Heterogeneous Employment Effects Across Restaurant Chains")
print("=" * 78)


# ==================================================
# Research question
# ==================================================

print(
    "\nResearch question:"
    "\nDid the employment response to New Jersey's minimum-wage "
    "increase differ across restaurant chains?"
)


# ==================================================
# Construct balanced analysis sample
# ==================================================

# Use stores with observed FTE employment in both waves.
# This is consistent with the balanced-sample logic used
# in the core replication.

sample = df.dropna(
    subset=[
        "FTE_BEFORE",
        "FTE_AFTER",
        "STATE",
        "CHAIN"
    ]
).copy()


sample["DELTA_FTE_EXTENSION"] = (
    sample["FTE_AFTER"]
    - sample["FTE_BEFORE"]
)


# ==================================================
# Chain labels
# ==================================================

chain_names = {
    1: "Burger King",
    2: "KFC",
    3: "Roy Rogers",
    4: "Wendy's"
}

sample["CHAIN_NAME_EXTENSION"] = (
    sample["CHAIN"]
    .map(chain_names)
)


print(
    f"\nBalanced extension sample size: {len(sample)}"
)


# ==================================================
# Chain-specific DiD estimates
# ==================================================

results = []


for chain_code, chain_name in chain_names.items():

    chain_sample = sample[
        sample["CHAIN"] == chain_code
    ].copy()

    nj = chain_sample[
        chain_sample["STATE"] == 1
    ]

    pa = chain_sample[
        chain_sample["STATE"] == 0
    ]


    # --------------------------------------------------
    # Mean employment changes
    # --------------------------------------------------

    nj_change = (
        nj["DELTA_FTE_EXTENSION"].mean()
    )

    pa_change = (
        pa["DELTA_FTE_EXTENSION"].mean()
    )


    # --------------------------------------------------
    # Chain-specific difference-in-differences
    #
    # Since the dependent variable is already
    # After - Before, the coefficient on STATE is
    # exactly the NJ-minus-PA DiD for this chain.
    # --------------------------------------------------

    model = smf.ols(
        "DELTA_FTE_EXTENSION ~ STATE",
        data=chain_sample
    ).fit(
        cov_type="HC1"
    )


    did = (
        model.params["STATE"]
    )

    se = (
        model.bse["STATE"]
    )

    p_value = (
        model.pvalues["STATE"]
    )

    ci = (
        model.conf_int()
        .loc["STATE"]
    )


    results.append({

        "Chain":
            chain_name,

        "Chain_Code":
            chain_code,

        "N_Total":
            len(chain_sample),

        "N_NJ":
            len(nj),

        "N_PA":
            len(pa),

        "NJ_Mean_Change":
            nj_change,

        "PA_Mean_Change":
            pa_change,

        "Chain_DiD":
            did,

        "Robust_SE":
            se,

        "CI_Lower_95":
            ci.iloc[0],

        "CI_Upper_95":
            ci.iloc[1],

        "P_Value":
            p_value
    })


extension = pd.DataFrame(
    results
)


# ==================================================
# Pooled heterogeneity regression
# ==================================================

# Burger King (CHAIN = 1) is the reference chain.
#
# STATE is therefore the NJ effect for Burger King.
#
# STATE:C(CHAIN)[T.x] measures how the NJ effect for
# another chain differs from Burger King.

heterogeneity_model = smf.ols(
    "DELTA_FTE_EXTENSION ~ STATE * C(CHAIN)",
    data=sample
).fit(
    cov_type="HC1"
)


# ==================================================
# Joint test of interaction terms
# ==================================================

interaction_test = (
    heterogeneity_model.f_test(
        "STATE:C(CHAIN)[T.2] = 0, "
        "STATE:C(CHAIN)[T.3] = 0, "
        "STATE:C(CHAIN)[T.4] = 0"
    )
)


heterogeneity_p = float(
    np.asarray(
        interaction_test.pvalue
    ).item()
)


heterogeneity_f = float(
    np.asarray(
        interaction_test.fvalue
    ).item()
)


heterogeneity_summary = pd.DataFrame({

    "Test": [
        "Joint test of chain-by-NJ interactions"
    ],

    "F_Statistic": [
        heterogeneity_f
    ],

    "P_Value": [
        heterogeneity_p
    ],

    "Null_Hypothesis": [
        "The NJ employment effect is equal across restaurant chains"
    ]
})


# ==================================================
# Save tables
# ==================================================

TABLE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

FIGURE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


extension.to_csv(
    TABLE_FILE,
    index=False,
    float_format="%.6f"
)


heterogeneity_summary.to_csv(
    TEST_FILE,
    index=False,
    float_format="%.6f"
)


# ==================================================
# Display chain-specific results
# ==================================================

print(
    "\nChain-specific employment responses:"
)

display_columns = [
    "Chain",
    "N_NJ",
    "N_PA",
    "NJ_Mean_Change",
    "PA_Mean_Change",
    "Chain_DiD",
    "Robust_SE",
    "P_Value"
]

print(
    extension[
        display_columns
    ]
    .round(3)
    .to_string(index=False)
)


# ==================================================
# Display heterogeneity test
# ==================================================

print(
    "\nJoint heterogeneity test:"
)

print(
    f"F-statistic = "
    f"{heterogeneity_f:.3f}"
)

print(
    f"P-value = "
    f"{heterogeneity_p:.4f}"
)


if heterogeneity_p < 0.05:

    print(
        "Result: Evidence of statistically significant "
        "differences in the employment response across chains."
    )

else:

    print(
        "Result: The data do not provide strong evidence "
        "that the employment response differs across chains."
    )


# ==================================================
# Extension figure
# ==================================================

plot_data = extension.copy()

x = np.arange(
    len(plot_data)
)

estimates = (
    plot_data["Chain_DiD"]
    .to_numpy()
)

lower_error = (
    estimates
    - plot_data["CI_Lower_95"].to_numpy()
)

upper_error = (
    plot_data["CI_Upper_95"].to_numpy()
    - estimates
)


plt.figure(
    figsize=(9, 6)
)


plt.errorbar(
    x,
    estimates,
    yerr=[
        lower_error,
        upper_error
    ],
    fmt="o",
    capsize=5
)


plt.axhline(
    y=0,
    linewidth=1
)


plt.xticks(
    x,
    plot_data["Chain"]
)


plt.ylabel(
    "Difference-in-Differences in FTE Employment"
)


plt.xlabel(
    "Restaurant Chain"
)


plt.title(
    "Independent Extension: Chain-Specific Employment Effects"
)


plt.tight_layout()


plt.savefig(
    FIGURE_FILE,
    dpi=300,
    bbox_inches="tight"
)


plt.close()


# ==================================================
# Output paths
# ==================================================

print(
    "\nExtension results saved to:"
)

print(
    TABLE_FILE
)


print(
    "\nHeterogeneity test saved to:"
)

print(
    TEST_FILE
)


print(
    "\nExtension figure saved to:"
)

print(
    FIGURE_FILE
)


print(
    "\nIndependent extension completed successfully."
)
