# ECO6067 Empirical Replication Project

## Card & Krueger (1994): Minimum Wages and Employment

This repository contains my empirical replication project for ECO6067.

The project replicates selected results from:

David Card and Alan B. Krueger (1994),  
"Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania",  
American Economic Review, 84(4), 772–793.

The original study examines the employment effects of New Jersey's minimum-wage increase from $4.25 to $5.05 per hour in April 1992. Pennsylvania, where the minimum wage remained unchanged, is used as the comparison group.

The project reproduces the main descriptive statistics, difference-in-differences results, regression specifications, and wage-distribution figure, and then develops an independent extension examining heterogeneous employment responses across restaurant chains.


## Research Question

The main replication question is:

**Did New Jersey's 1992 minimum-wage increase reduce employment in the fast-food industry relative to Pennsylvania?**

The independent extension asks:

**Did the employment response to the minimum-wage increase differ across restaurant chains?**


## Repository Structure

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
├── AI_USE_DISCLOSURE.md
├── requirements.txt
├── report.pdf
├── README.md
└── .gitignore


## Final Report

The final empirical replication report is available here:

[Final Report (PDF)](report.pdf)
