# OpenData Insight

## Overview
Analyze California county-level income limits (2023) and generate summary statistics and visualizations.

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
