from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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

FIGURE_DIR = (
    PROJECT_ROOT
    / "outputs"
    / "figures"
)

TABLE_DIR = (
    PROJECT_ROOT
    / "outputs"
    / "tables"
)

FIGURE_FILE = (
    FIGURE_DIR
    / "figure1_wage_distribution.png"
)

DATA_FILE = (
    TABLE_DIR
    / "figure1_wage_distribution.csv"
)


# ==================================================
# Load processed data
# ==================================================

df = pd.read_csv(PROCESSED_DATA)

print("=" * 75)
print("ECO6067 - Card & Krueger (1994)")
print("Replication of Figure 1 - Distribution of Starting Wage Rates")
print("=" * 75)


# ==================================================
# Wage-range construction
# ==================================================

# Figure 1 groups starting wages into approximately
# ten-cent wage ranges beginning at $4.25.
#
# The final category collects wages of $5.55 or above.

wage_labels = np.round(
    np.arange(4.25, 5.56, 0.10),
    2
)

wage_edges = list(
    np.arange(4.25, 5.55 + 0.001, 0.10)
)

wage_edges.append(np.inf)


# ==================================================
# Distribution function
# ==================================================

def wage_distribution(data, wage_variable, state):

    wages = data.loc[
        data["STATE"] == state,
        wage_variable
    ].dropna()

    categories = pd.cut(
        wages,
        bins=wage_edges,
        labels=wage_labels,
        right=False,
        include_lowest=True
    )

    counts = (
        categories
        .value_counts(sort=False)
    )

    percentages = (
        counts / len(wages) * 100
    )

    return percentages, len(wages)


# ==================================================
# Wave 1 distributions
# ==================================================

wave1_nj, n_wave1_nj = wage_distribution(
    df,
    "WAGE_ST",
    1
)

wave1_pa, n_wave1_pa = wage_distribution(
    df,
    "WAGE_ST",
    0
)


# ==================================================
# Wave 2 distributions
# ==================================================

wave2_nj, n_wave2_nj = wage_distribution(
    df,
    "WAGE_ST2",
    1
)

wave2_pa, n_wave2_pa = wage_distribution(
    df,
    "WAGE_ST2",
    0
)


# ==================================================
# Save underlying Figure 1 data
# ==================================================

figure_data = pd.DataFrame({

    "Wage_Range":
        wage_labels,

    "Wave1_NJ_Percent":
        wave1_nj.to_numpy(),

    "Wave1_PA_Percent":
        wave1_pa.to_numpy(),

    "Wave2_NJ_Percent":
        wave2_nj.to_numpy(),

    "Wave2_PA_Percent":
        wave2_pa.to_numpy()
})


FIGURE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

TABLE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


figure_data.to_csv(
    DATA_FILE,
    index=False,
    float_format="%.6f"
)


# ==================================================
# Validation output
# ==================================================

print("\nNon-missing wage observations:")

print(
    f"Wave 1 - NJ: {n_wave1_nj}"
)

print(
    f"Wave 1 - PA: {n_wave1_pa}"
)

print(
    f"Wave 2 - NJ: {n_wave2_nj}"
)

print(
    f"Wave 2 - PA: {n_wave2_pa}"
)


print("\nWave 1 wage distribution (%):")

print(
    figure_data[
        [
            "Wage_Range",
            "Wave1_NJ_Percent",
            "Wave1_PA_Percent"
        ]
    ]
    .round(2)
    .to_string(index=False)
)


print("\nWave 2 wage distribution (%):")

print(
    figure_data[
        [
            "Wage_Range",
            "Wave2_NJ_Percent",
            "Wave2_PA_Percent"
        ]
    ]
    .round(2)
    .to_string(index=False)
)


# ==================================================
# Replicate Figure 1
# ==================================================

x = np.arange(
    len(wage_labels)
)

bar_width = 0.38


fig, axes = plt.subplots(
    2,
    1,
    figsize=(11, 10)
)


# --------------------------------------------------
# Panel A: February 1992
# --------------------------------------------------

axes[0].bar(
    x - bar_width / 2,
    wave1_nj.to_numpy(),
    width=bar_width,
    color="black",
    edgecolor="black",
    label="New Jersey"
)

axes[0].bar(
    x + bar_width / 2,
    wave1_pa.to_numpy(),
    width=bar_width,
    color="white",
    edgecolor="black",
    hatch="//",
    label="Pennsylvania"
)

axes[0].set_title(
    "February 1992"
)

axes[0].set_ylabel(
    "Percent of Stores"
)

axes[0].set_xlabel(
    "Wage Range"
)

axes[0].set_ylim(
    0,
    35
)

axes[0].set_xticks(x)

axes[0].set_xticklabels(
    [
        f"{value:.2f}"
        if value < 5.55
        else "5.55+"
        for value in wage_labels
    ],
    rotation=45
)

axes[0].legend()


# --------------------------------------------------
# Panel B: November 1992
# --------------------------------------------------

axes[1].bar(
    x - bar_width / 2,
    wave2_nj.to_numpy(),
    width=bar_width,
    color="black",
    edgecolor="black",
    label="New Jersey"
)

axes[1].bar(
    x + bar_width / 2,
    wave2_pa.to_numpy(),
    width=bar_width,
    color="white",
    edgecolor="black",
    hatch="//",
    label="Pennsylvania"
)

axes[1].set_title(
    "November 1992"
)

axes[1].set_ylabel(
    "Percent of Stores"
)

axes[1].set_xlabel(
    "Wage Range"
)

axes[1].set_ylim(
    0,
    90
)

axes[1].set_xticks(x)

axes[1].set_xticklabels(
    [
        f"{value:.2f}"
        if value < 5.55
        else "5.55+"
        for value in wage_labels
    ],
    rotation=45
)

axes[1].legend()


# ==================================================
# Overall title and layout
# ==================================================

fig.suptitle(
    "Figure 1. Distribution of Starting Wage Rates",
    fontsize=14
)

plt.tight_layout(
    rect=[0, 0, 1, 0.97]
)


# ==================================================
# Save Figure 1
# ==================================================

plt.savefig(
    FIGURE_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("\nFigure 1 data saved to:")
print(DATA_FILE)

print("\nFigure 1 saved to:")
print(FIGURE_FILE)

print(
    "\nFigure 1 replication completed successfully."
)
