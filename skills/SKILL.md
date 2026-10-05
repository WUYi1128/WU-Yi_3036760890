# Reusable Skill: Reproducing the Card & Krueger Empirical Analysis

## Purpose

This document provides a reusable end-to-end workflow for reproducing the main empirical results in this ECO6067 replication project based on:

David Card and Alan B. Krueger (1994),  
"Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania",  
*American Economic Review*, 84(4), 772–793.

The workflow is designed so that, once the required course-provided input dataset is placed in the correct local folder, the main data-processing steps, replicated tables, replicated figure, validation checks, and independent extension can be generated without manually editing the data or analysis code.

The workflow covers:

- inspection of the raw dataset;
- construction of analysis variables;
- cleaning and processing of the data;
- replication of Table 2;
- replication of Table 3;
- replication of Table 4;
- replication of Figure 1;
- automated numerical validation;
- an independent extension examining heterogeneous employment effects across restaurant chains;
- generation of final tables and figures.

---

## Research Context

The original Card and Krueger study examines the employment effects of New Jersey's increase in the statutory minimum wage from \$4.25 to \$5.05 per hour in April 1992.

Pennsylvania did not experience the same minimum-wage increase and is therefore used as the comparison group.

The core empirical design is a difference-in-differences framework.

Let \(Y_{st}\) denote an employment outcome for state \(s\) and period \(t\). The basic difference-in-differences estimand is

$$
\widehat{\mathrm{DiD}}
=
\left(
\bar{Y}_{NJ,post}
-
\bar{Y}_{NJ,pre}
\right)
-
\left(
\bar{Y}_{PA,post}
-
\bar{Y}_{PA,pre}
\right).
$$

A positive value indicates that employment changed more favourably in New Jersey than in Pennsylvania over the sample period.

The project primarily uses full-time-equivalent employment. The constructed FTE measure follows the replication workflow:

$$
FTE
=
EMPFT
+
NMgrs
+
0.5 \times EMPPT,
$$

with the corresponding second-wave measure

$$
FTE_2
=
EMPFT2
+
NMgrs2
+
0.5 \times EMPPT2.
$$

The employment change for restaurant \(i\) is therefore

$$
\Delta FTE_i
=
FTE_{i,2}
-
FTE_{i,1}.
$$

---

## Required Repository Structure

The public GitHub repository should have the following structure:

```text
WU-Yi_3036760890/
│
├── code/
│   ├── 01_inspect_data.py
│   ├── 02_clean_data.py
│   ├── 03_replicate_table2.py
│   ├── 04_replicate_table3.py
│   ├── 05_replicate_table4.py
│   ├── 06_replicate_figure1.py
│   ├── 07_validation.py
│   ├── 08_extension.py
│   └── run_all.py
│
├── data/
│   ├── raw/
│   │   ├── README.md
│   │   └── DATA_DICTIONARY.md
│   │
│   └── processed/
│       └── README.md
│
├── outputs/
│   ├── tables/
│   │   ├── README.md
│   │   ├── table2_replication.csv
│   │   ├── table3_replication.csv
│   │   ├── table4_replication.csv
│   │   ├── figure1_wage_distribution.csv
│   │   ├── validation_summary.csv
│   │   ├── extension_chain_did.csv
│   │   └── extension_chain_heterogeneity_test.csv
│   │
│   └── figures/
│       ├── README.md
│       ├── figure1_wage_distribution.png
│       └── extension_chain_did.png
│
├── skills/
│   └── SKILL.md
│
├── AI_USE_DISCLOSURE.md
├── README.md
├── requirements.txt
└── .gitignore
```

### Local-only input and processed data

Two files are required during local execution but are intentionally excluded from the public GitHub repository:

```text
data/raw/public.csv
data/processed/analysis_sample.csv
```

`public.csv` is the course-provided dataset.

`analysis_sample.csv` is generated from that dataset by the processing workflow.

Because the source dataset was supplied as part of the ECO6067 course materials, neither the raw restaurant-level dataset nor its row-level processed derivative is distributed through the public GitHub repository.

---

## Required Input

Before running the workflow locally, obtain the course-provided Card and Krueger dataset and place it at:

```text
data/raw/public.csv
```

The filename and folder location should not be changed because the Python scripts use this expected relative path.

The expected raw dataset contains:

- 410 restaurant-level observations;
- 46 original variables;
- first-wave and second-wave survey information.

No manual modification of the raw CSV file is required.

---

## Key Raw Variables

Important variables used in the workflow include:

| Variable | Interpretation |
|---|---|
| `SHEET` | Original store or survey-sheet identifier |
| `CHAIN` | Restaurant chain identifier |
| `CO_OWNED` | Indicator for company ownership |
| `STATE` | State indicator: 1 = New Jersey, 0 = Pennsylvania |
| `EMPFT` | Number of full-time employees in Wave 1 |
| `EMPPT` | Number of part-time employees in Wave 1 |
| `NMGRS` | Number of managers and assistant managers in Wave 1 |
| `WAGE_ST` | Starting wage in Wave 1 |
| `HRSOPEN` | Hours open per day in Wave 1 |
| `EMPFT2` | Number of full-time employees in Wave 2 |
| `EMPPT2` | Number of part-time employees in Wave 2 |
| `NMGRS2` | Number of managers and assistant managers in Wave 2 |
| `WAGE_ST2` | Starting wage in Wave 2 |
| `HRSOPEN2` | Hours open per day in Wave 2 |
| `STATUS2` | Second-wave survey status |

A more detailed variable description is provided in:

```text
data/raw/DATA_DICTIONARY.md
```

---

## Reproduction Workflow

### Step 1: Install Python dependencies

From the repository root, install the required Python packages:

```bash
pip install -r requirements.txt
```

---

### Step 2: Add the course-provided dataset

Place the dataset at:

```text
data/raw/public.csv
```

Do not rename the file.

Do not commit this file to the public GitHub repository.

---

### Step 3: Run the complete workflow

From the repository root, execute:

```bash
python code/run_all.py
```

The master script executes the component scripts in sequence.

---

## Workflow Components

### `01_inspect_data.py`

Performs the initial inspection of the course-provided raw dataset.

Checks include:

- dataset dimensions;
- variable names;
- first observations;
- state counts;
- restaurant-chain counts;
- second-wave response status;
- missing values in key variables;
- descriptive statistics.

This stage provides a transparent check of the original input before any transformation occurs.

---

### `02_clean_data.py`

Constructs the variables required for the empirical analysis.

Important constructed measures include:

$$
FTE_{before}
=
EMPFT
+
NMGRS
+
0.5 \times EMPPT,
$$

and

$$
FTE_{after}
=
EMPFT2
+
NMGRS2
+
0.5 \times EMPPT2.
$$

Employment change is calculated as

$$
\Delta FTE
=
FTE_{after}
-
FTE_{before}.
$$

The script also creates variables needed for the state comparison, balanced sample, wage-gap specifications, and later replication stages.

The processed dataset is written locally to:

```text
data/processed/analysis_sample.csv
```

This file is generated automatically and is not distributed in the public repository.

---

### `03_replicate_table2.py`

Replicates selected descriptive statistics from Table 2 of Card and Krueger (1994).

The script calculates key means separately for New Jersey and Pennsylvania and compares the results with the published values.

The output is saved to:

```text
outputs/tables/table2_replication.csv
```

---

### `04_replicate_table3.py`

Replicates the main employment-change and difference-in-differences results associated with Table 3.

The central quantity is

$$
\widehat{\mathrm{DiD}}
=
\overline{\Delta FTE}_{NJ}
-
\overline{\Delta FTE}_{PA}.
$$

The script also examines:

- the main sample;
- the balanced sample;
- a temporary-closure sensitivity sample.

The output is saved to:

```text
outputs/tables/table3_replication.csv
```

---

### `05_replicate_table4.py`

Replicates selected reduced-form employment regressions corresponding to Table 4.

The specifications use employment change as the dependent variable and reproduce the principal state- and wage-gap-based coefficients from the original analysis.

The output is saved to:

```text
outputs/tables/table4_replication.csv
```

The estimation sample contains 357 restaurants after applying the required sample restrictions and non-missing-variable conditions.

---

### `06_replicate_figure1.py`

Replicates the distribution of starting wage rates shown in Figure 1.

The script calculates wage distributions for:

- New Jersey, Wave 1;
- Pennsylvania, Wave 1;
- New Jersey, Wave 2;
- Pennsylvania, Wave 2.

The numerical data are saved to:

```text
outputs/tables/figure1_wage_distribution.csv
```

The figure is saved to:

```text
outputs/figures/figure1_wage_distribution.png
```

A central feature of the replicated figure is the concentration of New Jersey Wave 2 starting wages around the new \$5.05 minimum wage.

---

### `07_validation.py`

Performs automated numerical validation of the core replication results.

The script compares replicated values with benchmark values from the original study using explicitly defined numerical tolerances.

The checks cover selected results from:

- Table 2;
- Table 3;
- Table 4;
- Figure 1.

The validated workflow reports:

```text
Passed checks: 13/13
All core replication checks passed.
```

The complete validation table is saved to:

```text
outputs/tables/validation_summary.csv
```

This step ensures that the reproduced results are not accepted merely because they appear visually similar to the original study.

---

## Independent Extension

The independent extension asks:

> Did the employment response to New Jersey's minimum-wage increase differ across restaurant chains?

The extension is implemented in:

```text
code/08_extension.py
```

For each restaurant chain \(c\), the chain-specific difference-in-differences estimate is

$$
\widehat{\mathrm{DiD}}_c
=
\overline{\Delta FTE}_{NJ,c}
-
\overline{\Delta FTE}_{PA,c}.
$$

The extension considers:

- Burger King;
- KFC;
- Roy Rogers;
- Wendy's.

The analysis reports chain-specific employment responses and conducts a joint heterogeneity test.

The numerical outputs are saved to:

```text
outputs/tables/extension_chain_did.csv
outputs/tables/extension_chain_heterogeneity_test.csv
```

The corresponding figure is saved to:

```text
outputs/figures/extension_chain_did.png
```

The heterogeneity test produces:

```text
F-statistic = 2.602
p-value = 0.0518
```

At the conventional 5% significance level, this does not provide sufficiently strong evidence to reject the null hypothesis of no systematic differences across restaurant chains.

Because the p-value is close to 0.05 and some chain-specific comparison groups are relatively small, the result should be interpreted cautiously rather than as conclusive evidence of heterogeneous treatment effects.

---

## Expected Outputs

After successful execution, the main reproducible outputs are:

### Tables

```text
outputs/tables/table2_replication.csv
outputs/tables/table3_replication.csv
outputs/tables/table4_replication.csv
outputs/tables/figure1_wage_distribution.csv
outputs/tables/validation_summary.csv
outputs/tables/extension_chain_did.csv
outputs/tables/extension_chain_heterogeneity_test.csv
```

### Figures

```text
outputs/figures/figure1_wage_distribution.png
outputs/figures/extension_chain_did.png
```

---

## Validation Standard

A successful reproduction should satisfy three conditions.

First, the component scripts should execute without errors.

Second, the key replicated statistics should fall within the numerical tolerances specified in `07_validation.py`.

Third, the validation script should report:

```text
Passed checks: 13/13
All core replication checks passed.
```

Small numerical differences from the published paper can arise from rounding, sample implementation, or specification details. These differences should be documented rather than manually altering results to force exact agreement.

---

## Reproducibility Principle

The workflow is intended to satisfy the following reproducibility condition:

> Once an authorised user places the required course-provided input file at `data/raw/public.csv`, the principal tables, figures, validation results, and independent extension can be regenerated through a single master command without manually editing either the input data or the analysis code.

The command is:

```bash
python code/run_all.py
```

This makes the workflow portable across machines because the analysis scripts use project-relative paths rather than user-specific absolute file paths.

---

## Data-Access Policy

The raw course-provided dataset is intentionally excluded from the public GitHub repository.

The row-level processed dataset is also excluded because it is directly derived from the course-provided input data.

The repository instead provides:

- complete analysis code;
- input-location instructions;
- a data dictionary;
- aggregate replication outputs;
- aggregate extension outputs;
- validation results;
- reproducibility documentation.

An authorised user can reproduce the project by obtaining the course-provided dataset and placing it at:

```text
data/raw/public.csv
```

No manual alteration of the dataset is required.

---

## Reuse

This workflow can be reused as a general empirical-replication template by replacing:

1. the raw-data inspection stage;
2. the variable-construction rules;
3. the target empirical tables or figures;
4. the benchmark validation values;
5. the independent extension.

The general structure remains:

```text
Raw input
    ↓
Data inspection
    ↓
Variable construction and cleaning
    ↓
Core replication
    ↓
Numerical validation
    ↓
Independent extension
    ↓
Final tables and figures
```

This separation between data preparation, replication, validation, and extension makes the workflow easier to audit, debug, and reproduce.
