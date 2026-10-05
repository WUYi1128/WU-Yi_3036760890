# ECO6067 Empirical Replication Project

## Card & Krueger (1994): Minimum Wages and Employment

This repository contains my ECO6067 individual empirical replication project based on:

David Card and Alan B. Krueger (1994),  
"Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania",  
*American Economic Review*, 84(4), 772–793.

The project reconstructs the main analysis dataset, reproduces selected tables and figures from the original study, validates the replicated results numerically, and develops an independent extension examining whether employment responses differed across restaurant chains.

---

## Research Question

The original study asks whether New Jersey's increase in the minimum wage from \$4.25 to \$5.05 per hour in April 1992 reduced employment in the fast-food industry.

New Jersey is treated as the treatment group, while Pennsylvania serves as the comparison group because its minimum wage did not experience the same increase during the study period.

The main empirical framework is difference-in-differences.

```math
\widehat{\mathrm{DiD}}
=
\left(\bar{Y}_{NJ,post}-\bar{Y}_{NJ,pre}\right)
-
\left(\bar{Y}_{PA,post}-\bar{Y}_{PA,pre}\right)
```

A positive value means that employment changed more favourably in New Jersey than in Pennsylvania over the sample period.

---

## Main Employment Measure

The principal employment measure is full-time-equivalent employment.

Before the minimum-wage increase:

```math
FTE_{\text{before}}
=
EMPFT
+
NMGRS
+
0.5\,EMPPT
```

After the minimum-wage increase:

```math
FTE_{\text{after}}
=
EMPFT2
+
NMGRS2
+
0.5\,EMPPT2
```

Employment change for restaurant \(i\) is:

```math
\Delta FTE_i
=
FTE_{i,\text{after}}
-
FTE_{i,\text{before}}
```

---

## Main Replication Tasks

The project reproduces selected empirical results from:

- Table 2: descriptive statistics;
- Table 3: employment changes and difference-in-differences estimates;
- Table 4: reduced-form employment regressions;
- Figure 1: distribution of starting wage rates.

The project also includes:

- systematic raw-data inspection;
- construction of analysis variables;
- automated numerical validation;
- an independent empirical extension;
- a one-command reproducibility workflow.

---

## Repository Structure

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

---

## Data Access

The raw dataset used in this project was provided as part of the ECO6067 course materials.

Following course guidance, the course-provided dataset is **not included in this public GitHub repository**.

The row-level processed dataset generated from the course-provided data is also not publicly distributed.

To reproduce the analysis, an authorised user should obtain the course-provided dataset and place it locally at:

```text
data/raw/public.csv
```

The expected raw dataset contains:

- 410 restaurant-level observations;
- 46 original variables;
- observations from New Jersey and Pennsylvania;
- information from two survey waves.

The raw CSV should not be manually modified.

The project provides a description of the required variables in:

```text
data/raw/DATA_DICTIONARY.md
```

---

## Local-Only Files

The following files are required or generated during local reproduction but are intentionally excluded from the public repository:

```text
data/raw/public.csv
data/processed/analysis_sample.csv
```

`public.csv` is the course-provided raw dataset.

`analysis_sample.csv` is generated automatically by the data-processing script and contains row-level information derived from the course-provided data.

---

## Key Variables

| Variable | Description |
|---|---|
| `SHEET` | Original store or survey-sheet identifier |
| `CHAIN` | Restaurant chain identifier |
| `CO_OWNED` | Company-ownership indicator |
| `STATE` | State indicator: 1 = New Jersey, 0 = Pennsylvania |
| `SOUTHJ` | Indicator for southern New Jersey |
| `CENTRALJ` | Indicator for central New Jersey |
| `NORTHJ` | Indicator for northern New Jersey |
| `PA1` | Indicator for northeastern Philadelphia suburbs |
| `PA2` | Indicator for the Easton area of Pennsylvania |
| `EMPFT` | Number of full-time employees in Wave 1 |
| `EMPPT` | Number of part-time employees in Wave 1 |
| `NMGRS` | Number of managers and assistant managers in Wave 1 |
| `WAGE_ST` | Starting wage in Wave 1 |
| `HRSOPEN` | Hours open per day in Wave 1 |
| `STATUS2` | Second-wave survey status |
| `EMPFT2` | Number of full-time employees in Wave 2 |
| `EMPPT2` | Number of part-time employees in Wave 2 |
| `NMGRS2` | Number of managers and assistant managers in Wave 2 |
| `WAGE_ST2` | Starting wage in Wave 2 |
| `HRSOPEN2` | Hours open per day in Wave 2 |

See `data/raw/DATA_DICTIONARY.md` for further details.

---

# Reproduction Instructions

## 1. Clone the Repository

```bash
git clone <repository-url>
```

Enter the project directory:

```bash
cd WU-Yi_3036760890
```

---

## 2. Install Python Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## 3. Add the Course-Provided Dataset

Obtain the original ECO6067 course dataset and save it locally using the exact path:

```text
data/raw/public.csv
```

Do not rename or manually modify the file.

---

## 4. Run the Entire Project

From the repository root, execute:

```bash
python code/run_all.py
```

This command performs the complete replication workflow automatically.

The workflow runs:

```text
01_inspect_data.py
        ↓
02_clean_data.py
        ↓
03_replicate_table2.py
        ↓
04_replicate_table3.py
        ↓
05_replicate_table4.py
        ↓
06_replicate_figure1.py
        ↓
07_validation.py
        ↓
08_extension.py
```

No manual modification of the input data or analysis code is required.

---

# Core Replication Results

## Table 2

The project reproduces selected descriptive statistics reported in Table 2.

| Statistic | Replication | Original |
|---|---:|---:|
| Wave 1 NJ FTE | 20.439 | 20.44 |
| Wave 1 PA FTE | 23.331 | 23.33 |
| Wave 2 NJ FTE | 21.027 | 21.03 |
| Wave 2 PA FTE | 21.166 | 21.17 |

The replicated values are extremely close to the published values.

Output:

```text
outputs/tables/table2_replication.csv
```

---

## Table 3

The main difference-in-differences estimator is:

```math
\widehat{\mathrm{DiD}}
=
\overline{\Delta FTE}_{NJ}
-
\overline{\Delta FTE}_{PA}
```

Selected results are:

| Specification | Replication | Original |
|---|---:|---:|
| Main DiD | 2.754 | 2.76 |
| Balanced-sample DiD | 2.750 | 2.75 |
| Temporary-closure sensitivity | 2.509 | 2.51 |

The replicated estimates closely match the corresponding published values.

Output:

```text
outputs/tables/table3_replication.csv
```

---

## Table 4

The Table 4 regression replication uses an estimation sample of 357 restaurants.

Selected coefficient comparisons are:

| Model | Replication | Original |
|---|---:|---:|
| Model (i) | 2.326 | 2.33 |
| Model (ii) | 2.304 | 2.30 |
| Model (iii) | 15.653 | 15.65 |
| Model (iv) | 14.916 | 14.92 |
| Model (v) | 11.979 | 11.91 |

The first four estimates are extremely close to the published coefficients.

Model (v) shows a somewhat larger numerical difference, but it remains within the predefined replication tolerance.

Output:

```text
outputs/tables/table4_replication.csv
```

---

## Figure 1

The project reproduces the distribution of starting wage rates before and after the New Jersey minimum-wage increase.

The replicated distribution shows a strong concentration of New Jersey Wave 2 starting wages around \$5.05.

Approximately 89.62% of observed New Jersey Wave 2 starting wages are concentrated in the \$5.05 wage category.

Numerical output:

```text
outputs/tables/figure1_wage_distribution.csv
```

Figure output:

```text
outputs/figures/figure1_wage_distribution.png
```

---

# Automated Validation

The project contains a separate validation script:

```text
code/07_validation.py
```

It compares key replicated statistics with published benchmark values using explicitly defined numerical tolerances.

The validation covers:

- Table 2 descriptive statistics;
- Table 3 DiD estimates;
- Table 4 regression coefficients;
- the principal Figure 1 pattern.

The final validation result is:

```text
Passed checks: 13/13
All core replication checks passed.
```

The detailed validation results are saved in:

```text
outputs/tables/validation_summary.csv
```

---

# Independent Extension

## Research Question

The independent extension asks:

> Did the employment response to New Jersey's minimum-wage increase differ across restaurant chains?

The analysis is implemented in:

```text
code/08_extension.py
```

The balanced extension sample contains 384 restaurants.

For chain \(c\), the chain-specific difference-in-differences estimator is:

```math
\widehat{\mathrm{DiD}}_c
=
\overline{\Delta FTE}_{NJ,c}
-
\overline{\Delta FTE}_{PA,c}
```

The estimated results are:

| Chain | NJ Mean Change | PA Mean Change | Chain DiD |
|---|---:|---:|---:|
| Burger King | 1.345 | -3.045 | 4.390 |
| KFC | 0.698 | 2.292 | -1.594 |
| Roy Rogers | -1.438 | -3.926 | 2.488 |
| Wendy's | 0.994 | -2.423 | 3.417 |

The point estimates vary across restaurant chains.

However, a joint statistical test is required before concluding that these differences represent systematic heterogeneity.

---

## Joint Heterogeneity Test

The extension produces:

```text
F-statistic = 2.602
p-value = 0.0518
```

At the conventional 5% significance level, the null hypothesis of no systematic chain-level heterogeneity is not rejected.

Because the p-value is close to 0.05, the results provide suggestive but not conclusive evidence of heterogeneous employment responses across restaurant chains.

The interpretation should remain cautious because some chain-specific Pennsylvania comparison groups contain relatively few observations.

Extension outputs:

```text
outputs/tables/extension_chain_did.csv
outputs/tables/extension_chain_heterogeneity_test.csv
outputs/figures/extension_chain_did.png
```

---

# Generated Outputs

## Tables

The reproducibility workflow generates:

```text
outputs/tables/table2_replication.csv
outputs/tables/table3_replication.csv
outputs/tables/table4_replication.csv
outputs/tables/figure1_wage_distribution.csv
outputs/tables/validation_summary.csv
outputs/tables/extension_chain_did.csv
outputs/tables/extension_chain_heterogeneity_test.csv
```

These files contain aggregate empirical results rather than the course-provided row-level dataset.

---

## Figures

The workflow generates:

```text
outputs/figures/figure1_wage_distribution.png
outputs/figures/extension_chain_did.png
```

---

# Successful Reproduction Check

A successful execution should finish with all scripts running without errors and the validation stage reporting:

```text
Passed checks: 13/13
All core replication checks passed.
```

The complete project can therefore be reproduced from the required input dataset using one command:

```bash
python code/run_all.py
```

---

# Reproducibility Design

The project uses relative file paths rather than machine-specific absolute paths.

The intended workflow is:

```text
Course-provided raw dataset
          ↓
Raw-data inspection
          ↓
Variable construction and cleaning
          ↓
Core empirical replication
          ↓
Numerical validation
          ↓
Independent extension
          ↓
Final tables and figures
```

This structure separates each analytical stage and makes the project easier to inspect, debug, audit, and reproduce.

A reusable description of the workflow is provided in:

```text
skills/SKILL.md
```

---

# AI Use Disclosure

Artificial intelligence tools were used as supporting tools during parts of the project, including:

- project and repository organisation;
- Python code drafting and debugging;
- reproducibility workflow design;
- documentation;
- interpretation checks;
- report-writing assistance.

AI-generated suggestions were not accepted without verification.

The code and empirical outputs were checked through local execution, comparison with the original study, inspection of generated tables and figures, and automated numerical validation.

A detailed record of AI use and verification is available in:

```text
AI_USE_DISCLOSURE.md
```

---

# Data Availability Note

The original input dataset is not distributed through this public repository because it was provided as part of the ECO6067 course materials.

To reproduce the project, an authorised user should obtain the course-provided dataset and save it locally as:

```text
data/raw/public.csv
```

After the file is placed in that location, run:

```bash
python code/run_all.py
```

The workflow will reconstruct the required processed data and regenerate the principal tables, figures, validation results, and independent extension.

---

## Reference

Card, D., & Krueger, A. B. (1994). Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania. *American Economic Review*, 84(4), 772–793.
