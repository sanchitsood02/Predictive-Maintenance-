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
The analysis uses the **N-CMAPSS DS01** dataset (specifically `N-CMAPSS_DS01-005.h5`).

### ⚠️ Important Note on Data
The raw N-CMAPSS data files are extremely large (several GBs each) and **cannot be hosted directly on GitHub** due to file size limits.

### How to Get the Data
1.  **Download** the dataset from the official NASA repository:
    *   [NASA Open Data Portal - N-CMAPSS](https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data)
    *   Direct link to data description: [Prognostics Data Repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/)
2.  **Place the files** in the root directory of this project.
3.  Ensure the file names match what the scripts expect (e.g., `N-CMAPSS_DS01-005.h5`).

### Directory Structure
After downloading, your folder should look like this:
```
/
├── N-CMAPSS_DS01-005.h5   <-- Downloaded file
├── complete_statistical_analysis_final.py
├── README.md
└── ...
```
