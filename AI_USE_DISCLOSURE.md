# AI Use Disclosure

## Overview

Artificial intelligence tools were used as supporting tools during this empirical replication project.

AI assistance was used for project planning, Python code structure, debugging, documentation, interpretation of replication differences, and preparation of the reproducibility workflow.

All final data choices, empirical specifications, validation checks, interpretation, and conclusions were reviewed against the original data, the published paper, the generated outputs, and explicit numerical validation tests.


## Where AI Was Used

### 1. Project Structure and Workflow

AI was used to help organise the project into a reproducible directory structure containing:

- raw data;
- processed data;
- analysis code;
- generated tables;
- generated figures;
- validation outputs;
- an independent extension;
- a master reproduction script.

AI also assisted in designing the sequential workflow implemented in `code/run_all.py`.


### 2. Python Coding Assistance

AI was used to assist with drafting and debugging Python scripts for:

- raw-data inspection;
- data cleaning and variable construction;
- replication of Table 2;
- replication of Table 3;
- replication of Table 4;
- replication of Figure 1;
- automated validation;
- the independent extension.

The code was not accepted without verification. Each stage was run locally, inspected, and compared with expected values before being retained.


### 3. Debugging and Reproducibility

AI assisted in resolving practical implementation issues, including:

- use of relative rather than machine-specific file paths;
- construction of the one-command reproduction workflow;
- GitHub repository organisation;
- Git and GitHub workflow questions;
- Python package requirements;
- interpretation of error messages;
- generation and storage of reproducible outputs.


### 4. Replication Interpretation

AI was used to help interpret differences between replicated and published values.

These interpretations were checked against the numerical outputs and the original study.

Examples include:

- the small difference between the replicated Table 3 main DiD estimate and the published rounded value;
- the difference in Table 4 specification (v);
- interpretation of the chain-level heterogeneous-treatment-effect extension.


### 5. Writing and Documentation

AI assisted with the structure and wording of:

- README documentation;
- code comments;
- reproducibility instructions;
- interpretation of results;
- the AI-use disclosure itself.

The final wording was reviewed to ensure that it accurately reflects the actual workflow and generated results.


## How AI Outputs Were Checked

AI-generated suggestions were checked in several ways.

### Raw Data Checks

The original dataset was inspected directly.

The raw dataset contains:

- 410 observations;
- 46 original variables.

State, chain, missing-value, and second-wave response counts were inspected before proceeding.


### Table 2 Validation

Replicated means for New Jersey and Pennsylvania were compared with the published Table 2 values.

Examples include:

- Wave 1 NJ FTE: 20.439 versus 20.44;
- Wave 1 PA FTE: 23.331 versus 23.33;
- Wave 2 NJ FTE: 21.027 versus 21.03;
- Wave 2 PA FTE: 21.166 versus 21.17.


### Table 3 Validation

The principal difference-in-differences estimates were checked against the published benchmarks.

The replicated values were approximately:

- main DiD: 2.754;
- balanced-sample DiD: 2.750;
- temporary-closure sensitivity result: 2.509.

These closely match the published values of approximately 2.76, 2.75, and 2.51.


### Table 4 Validation

The regression results were compared with the original reported coefficients.

Examples include:

- Model (i): 2.326 versus 2.33;
- Model (ii): 2.304 versus 2.30;
- Model (iii): 15.653 versus 15.65;
- Model (iv): 14.916 versus 14.92;
- Model (v): 11.979 versus 11.91.

The Table 4 estimation sample was also checked to contain 357 restaurants.


### Figure 1 Validation

The replicated wage distribution showed approximately 89.62% of observed New Jersey Wave 2 starting wages concentrated in the $5.05 wage range, consistent with the main pattern shown in the original figure.


### Automated Validation

A separate validation script was created to compare key replication outputs with benchmark values.

The final result was:

```text
Passed checks: 13/13
All core replication checks passed.
