# Reusable Skill: Reproducing the Card & Krueger Empirical Analysis

## Purpose

This skill provides a reusable workflow for reproducing the main empirical tables and figures in this project from the raw input data.

The workflow is designed for the ECO6067 empirical replication project based on Card and Krueger (1994).

It covers:

- raw-data inspection;
- data cleaning and variable construction;
- replication of Tables 2, 3 and 4;
- replication of Figure 1;
- automated validation;
- the independent extension;
- generation of final tables and figures.


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
│
├── outputs/
│   ├── tables/
│   └── figures/
│
├── requirements.txt
└── README.md
