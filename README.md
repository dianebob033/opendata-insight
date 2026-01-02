# OpenData Insight

## Overview

Housing affordability in California is governed by income limits derived from Area Median Income (AMI).  
This project analyzes county-level income limits for a 4-person household to examine how low-income thresholds scale with AMI across regions.

The goal is to understand whether income limits meaningfully adapt to local income differences, or whether they impose structurally uniform constraints across counties.

## Key Questions

- How much does AMI vary across California counties?
- Do Extremely Low Income (ELI) and Low Income (LI) thresholds scale proportionally with AMI?
- Are high-AMI counties disproportionately restrictive for low-income households?

## Key Findings

- AMI varies significantly across counties, ranging from ~$83k to over $180k.
- Despite large AMI differences, the ELI-to-AMI ratio remains relatively stable (~0.33).
- This suggests that income limits are largely standardized rather than locally adaptive.
- In high-AMI counties (e.g., Santa Clara, San Francisco), low-income households may face disproportionate affordability pressure.
- 
## Visualizations

### AMI Distribution by County
![AMI Distribution](reports/figures/ami_distribution.png)

This histogram highlights the substantial income disparity across California counties.

### Income Limit Ratios vs AMI
![Ratios vs AMI](reports/figures/eli_li_ratio_scatter.png)

The scatter plot shows that ELI and LI ratios remain relatively constant across AMI levels, indicating policy-driven thresholds rather than market sensitivity.

## Design Decisions

- Focused on 4-person household limits to control for household size variability.
- Used ratio-based metrics (ELI/AMI, LI/AMI) to normalize cross-county comparisons.
- Separated raw and processed data to ensure reproducibility and auditability.
- Implemented the analysis as a script-based pipeline rather than a notebook.

## Data Source
- California Income Limits by County (2023)

## Project Structure
- data/raw: raw CSV files
- data/processed: cleaned data
- src: source code
- reports: generated outputs

## How to Run
```bash
pip install -r requirements.txt
python src/main.py

## Key Findings (V1)
- Significant variation in AMI across California counties.
- Extremely Low Income (ELI) limits are consistently a small fraction of AMI.
- The ratio between low-income limits and AMI is relatively stable across counties.

## Visualizations (V2)

### AMI Distribution
![AMI Distribution](reports/figures/ami_distribution.png)

### Ratios vs AMI
![Ratios vs AMI](reports/figures/eli_li_ratio_scatter.png)
