# Reusable Skill: Reproducing the Card & Krueger Empirical Analysis

## Purpose

This document provides a reusable end-to-end workflow for reproducing the main empirical results in this ECO6067 replication project based on:

David Card and Alan B. Krueger (1994),  
"Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania",  
*American Economic Review*, 84(4), 772–793.

The workflow is designed so that, once the required input data are placed in the correct folder, the main data-processing steps, replicated tables, replicated figure, validation checks, and independent extension can be generated without manually editing the data or analysis code.

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

The original Card and Krueger study examines the employment effects of New Jersey's increase in the statutory minimum wage from $4.25 to $5.05 per hour in April 1992.

Pennsylvania did not experience the same minimum-wage increase and is therefore used as the comparison group.

The core empirical design is a difference-in-differences framework.

Let

\[
Y_{st}
\]

denote an employment outcome for state \(s\) and period \(t\). The basic difference-in-differences estimand is

\[
\widehat{\delta}_{DID}
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
\]

A positive value indicates that employment changed more favourably in New Jersey than in Pennsylvania over the sample period.

---

## Required Project Structure

The workflow assumes the following repository structure:

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
│   │   └── public.csv
│   └── processed/
│       └── analysis_sample.csv
│
├── outputs/
│   ├── tables/
│   │   ├── table2_replication.csv
│   │   ├── table3_replication.csv
│   │   ├── table4_replication.csv
│   │   ├── figure1_wage_distribution.csv
│   │   ├── validation_summary.csv
│   │   ├── extension_chain_did.csv
│   │   └── extension_chain_heterogeneity_test.csv
│   │
│   └── figures/
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
