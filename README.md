# N-CMAPSS Statistical Analysis & RUL Prediction

This repository contains statistical analysis and baseline models for the N-CMAPSS dataset (DS01), focused on Remaining Useful Life (RUL) prediction for turbofan engines.

## Key Files

- **`complete_statistical_analysis_final.py`**: The main script that performs:
  - Data loading and cleaning
  - Descriptive statistics
  - Correlation analysis (Pearson & Spearman)
  - Condition-aware analysis
  - Baseline Linear Regression model training (MAE: ~9.12 cycles)
- **`RESEARCH_SUPERVISOR_SUMMARY.md`**: A comprehensive summary of the dataset and analysis results.
- **`ABSTRACT_DRAFT.md`**: Draft abstract for the research paper.
- **`DATABASE_GUIDE.md`**: Guide to the N-CMAPSS dataset structure.

## Setup

1. Install dependencies:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn h5py
   ```
2. Run the analysis:
   ```bash
   python complete_statistical_analysis_final.py
   ```

## Dataset
The analysis uses the N-CMAPSS DS01 dataset. Due to size constraints, the raw `.h5` files are not included in this repository.
