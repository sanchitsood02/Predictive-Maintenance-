# Remaining Useful Life (RUL) Prediction for Turbofan Engines (C-MAPSS FD001)

## Project Overview
This repository contains the practical implementation work for a final-year undergraduate dissertation in Data Science and Artificial Intelligence on predictive maintenance. The technical focus is on estimating **Remaining Useful Life (RUL)** for aircraft turbofan engines from multivariate sensor time series, using the **NASA C-MAPSS** benchmark data (FD001 in this repository).

The codebase is notebook-led and supports exploratory analysis, feature handling and normalisation, model training, and evaluation for both:
- **Regression**: predicting RUL as a continuous value.
- **Classification**: predicting maintenance-relevant warning labels under a time-to-failure horizon.

The repository also generates saved artefacts (plots, tables, and flow diagrams) to support reporting and interpretation in the dissertation.

## Dissertation Context
This repository is the **technical companion** to my final-year dissertation report. It provides the implementation backbone and experimental workflow that underpin the written thesis.

- The **dissertation report** contains the full academic narrative: literature context, methodological justification, experimental design, interpretation, and reflective discussion.
- This **repository** contains the reproducible implementation: data handling, modelling code, and outputs that can be inspected and re-run by a supervisor or examiner.

Where standard methods and benchmark datasets are used, the work is positioned as academically rigorous for an undergraduate dissertation through careful framing, comparative evaluation, and clear documentation of assumptions and limitations.

## Research Aim and Objectives
**Aim:**  
To investigate and evaluate practical machine learning approaches for estimating turbofan engine Remaining Useful Life from multivariate sensor trajectories, and to document an end-to-end pipeline that supports a dissertation-level analysis.

**Objectives:**
1. Prepare a clear representation of the dataset structure, attributes, and target definition (RUL).
2. Implement a reproducible preprocessing pipeline, including feature selection and normalisation decisions.
3. Train and evaluate baseline and comparative models for RUL prediction.
4. Assess performance using appropriate regression and classification metrics and visual diagnostics.
5. Record outputs (plots/tables/logs) in a way that can be referenced directly in the dissertation report.

## Research Question / Problem Statement
Given multivariate sensor measurements from multiple run-to-failure engine trajectories, **how accurately and reliably can Remaining Useful Life be estimated**, and how do different modelling choices (e.g., tree-based regressors versus sequence models) compare under a consistent preprocessing and evaluation setup?

## Repository Scope
**In scope**
- Implementation of an RUL prediction workflow using the C-MAPSS FD001 data included in this repository.
- Notebook-based experiments covering preprocessing, modelling, and evaluation.
- Saved outputs (figures/tables/flow diagrams) to support dissertation write-up.

**Out of scope**
- Production deployment, real-time inference systems, or industrial integration.
- Extensive hyperparameter optimisation beyond what is needed for dissertation-level comparison.
- Claims of generalisation beyond the chosen benchmark subset without additional experiments.

## Dataset / Data Source
This project uses the **NASA C-MAPSS turbofan engine run-to-failure simulation dataset**, a widely used benchmark for predictive maintenance research.

- Data are provided as space-separated text files, with multiple engine trajectories.
- Each row corresponds to a single operational cycle snapshot for one engine, with identifiers, operational settings, and sensor measurements.
- The repository includes FD001 training and test splits, and a separate file of true RUL values for the test engines.

Files in this repository:
- `train_FD001.txt` — training trajectories (run-to-failure).
- `test_FD001.txt` — truncated test trajectories (end before failure).
- `RUL_FD001.txt` — ground-truth remaining cycles for the final cycle of each test engine.
- Additional subsets (FD002–FD004) are also present as text files, but the notebook primarily works with FD001.

High-level preprocessing/framing decisions visible in the implementation include:
- Assigning column names to the raw files (identifiers, settings, sensors).
- Dropping empty/constant columns where applicable.
- Min–max normalisation for selected features (diagram saved as an artefact).

## Methodology Overview
At a high level, the technical pipeline implemented in the notebook covers:

1. **Data ingestion and schema definition**
   - Load raw text files for FD001.
   - Assign a consistent column schema (identifiers, settings, sensor measurements).

2. **Target construction (RUL)**
   - For training data, RUL is derived per engine as:  
     `RUL = max_cycle(engine) − time_in_cycles`
   - For test data, the provided `RUL_FD001.txt` file supplies the remaining cycles beyond the final observed test cycle.

3. **Preprocessing and feature handling**
   - Drop columns that are empty or constant in FD001.
   - Apply min–max scaling to selected features for sequence modelling (where applicable).

4. **Modelling**
   - Regression models for RUL prediction (e.g., Random Forest; optional XGBoost if installed).
   - A sequence model pathway (LSTM) is present in the notebook; it requires TensorFlow to be installed and is optional.
   - Classification evaluation is included using warning labels defined by a time-to-failure threshold, with confusion matrices and ROC curves.

5. **Evaluation and outputs**
   - Regression metrics such as MAE, RMSE, and R² appear in the notebook.
   - Classification diagnostics include confusion matrices and ROC/AUC curves.
   - Figures and tables are exported to an `outputs/` run directory for traceability.

## Repository Structure
The repository is intentionally small and centred on a single notebook:

```
.
├── Main.ipynb
├── Damage Propagation Modeling.pdf
├── readme.txt
├── train_FD001.txt
├── test_FD001.txt
├── RUL_FD001.txt
├── train_FD002.txt / test_FD002.txt / RUL_FD002.txt
├── train_FD003.txt / test_FD003.txt / RUL_FD003.txt
├── train_FD004.txt / test_FD004.txt / RUL_FD004.txt
└── outputs/
    └── run_YYYYMMDD_HHMMSS/
        ├── stdout.log
        ├── data_flowchart.png
        ├── data_dictionary_table.png
        ├── data_dictionary.csv
        ├── example_rows_table.png
        ├── example_rows_layout.csv
        ├── data_attributes.png
        ├── normalization_diagram.png
        └── run_location.txt
```

- `Main.ipynb` — primary implementation notebook: data preparation, modelling, evaluation, and artefact generation.
- `outputs/` — automatically generated run folders; each run stores figures/tables/logs for reproducible evidence.
- `readme.txt` — brief dataset description (FD001–FD004) and original reference information.
- `Damage Propagation Modeling.pdf` — source paper describing the simulation framework used to create the dataset (background reference).

## How to Run the Project
### Prerequisites
- Python 3.x environment with Jupyter support.
- Core scientific Python stack (at minimum): `numpy`, `pandas`, `matplotlib`, `seaborn`, `scikit-learn`, `tqdm`.
- Optional dependencies depending on which sections you execute:
  - **TensorFlow**: required only for the LSTM sections.
  - **xgboost**: required only for XGBoost sections.

### Running the notebook
1. Open `Main.ipynb` in Jupyter Notebook / JupyterLab.
2. Ensure the working directory is the repository root (so the `*_FD001.txt` files are accessible).
3. Run cells as needed:
   - If you only need the visual documentation artefacts (flowchart, data dictionary table, normalisation diagram), run the setup cell and the final visual/artefact cell.
   - If you want to reproduce modelling results, run the notebook from top to bottom, installing optional dependencies as required.

### Reproducible outputs
When executed, the notebook creates a new timestamped folder:
- `outputs/run_YYYYMMDD_HHMMSS/`

This folder stores exported PNGs/CSVs and a `stdout.log` capturing console output for traceability.

## Experimental Outputs
Depending on which sections are executed, expected artefacts include:
- **Documentation visuals (no heavy computation required)**
  - `data_flowchart.png` — dataset flow from files to row meaning and target definition.
  - `data_dictionary_table.png` — a table view of columns, groups (identifier/setting/sensor), and descriptions.
  - `example_rows_table.png` — an illustrative row/column layout for readability.
  - `normalization_diagram.png` — a flow diagram of the feature scaling pipeline.
  - `data_attributes.png` — grouped attribute overview.
  - CSV versions of tables (`data_dictionary.csv`, `example_rows_layout.csv`).

- **Modelling/evaluation artefacts (only if modelling sections are run)**
  - Diagnostic plots (e.g., predicted versus true RUL, ROC curves, confusion matrices).
  - Console logs and intermediate tables produced inside the notebook.

## Evaluation Approach
The notebook uses evaluation approaches that are appropriate for dissertation-level assessment of predictive maintenance models:

- **Regression (RUL prediction)**
  - Mean Absolute Error (MAE)
  - Root Mean Squared Error (RMSE)
  - Coefficient of determination (R²)
  - Visual comparison plots (predicted vs true RUL)

- **Classification (warning labels under a time-to-failure horizon)**
  - Confusion matrix-based assessment
  - ROC curve and AUC for threshold-independent comparison

The dissertation report discusses why these metrics are appropriate for the practical maintenance framing and how to interpret them.

## Key Findings Summary
This repository is designed so that findings can be verified by re-running the notebook. To avoid overstating results in the README, specific numeric outcomes are referenced in the dissertation report and in the notebook outputs.

- Comparative performance is evaluated across implemented models under consistent preprocessing.
- Visual diagnostics support interpretation beyond single-number metrics.

**Placeholder (to be completed from your report/notebook outputs):**
- Best-performing model under the chosen evaluation setup: **[insert model name]**
- Summary of observed trade-offs (accuracy vs stability vs interpretability): **[insert short summary]**
- Key plots/tables used in the dissertation: **[insert figure/table references]**

## How This Repository Supports the Thesis
This repository supports the dissertation directly in the following ways:

- **Rationale and objectives**: the repository encodes the problem framing as an executable workflow using a recognised benchmark dataset.
- **Technical implementation**: the notebook implements the full pipeline discussed in the report (data ingestion → preprocessing → modelling → evaluation).
- **Data analysis**: exported data dictionary, attribute overview, and flowchart provide evidence of dataset understanding and documentation quality.
- **Model development**: baseline and comparative models are implemented in code, enabling repeatable experiments.
- **Evaluation**: metrics and diagnostic plots operationalise the evaluation methodology described in the report.
- **Reflection and limitations**: the structure encourages transparent reporting of what was run, what was saved, and what assumptions were made; limitations are documented below and should be aligned with the report discussion.

## Originality and Academic Positioning
This work uses standard benchmark data and established modelling techniques, which is appropriate for an undergraduate dissertation. The originality is positioned honestly through:

- The dissertation-led framing of predictive maintenance as both a regression and decision-relevant classification problem.
- A consistent implementation and evaluation workflow that supports comparative analysis.
- The emphasis on reproducibility and evidence capture (saved plots/tables/logs per run).
- Interpretation and reflective discussion in the dissertation report, supported by the empirical outputs produced here.

## Limitations
This project is scoped to be credible for a final-year dissertation; accordingly, several limitations apply:

- **Benchmark scope**: results are primarily demonstrated on FD001; generalisation across other C-MAPSS subsets requires additional controlled experiments.
- **Notebook-centred implementation**: the workflow is readable for assessment but would benefit from further modularisation for long-term maintenance.
- **Compute and dependencies**: sequence modelling sections may require TensorFlow and additional compute; optional libraries (e.g., XGBoost) are not guaranteed to be installed by default.
- **Evaluation constraints**: without careful cross-validation and per-condition analysis, conclusions should remain bounded to the experimental design described in the report.

## Ethical and Academic Integrity Note
This repository is intended for academic study and assessment.

- The dataset is a publicly available research benchmark; references are provided below.
- The aim is transparency and reproducibility: outputs are saved per run and can be inspected alongside the dissertation narrative.
- Any third-party ideas or baseline implementations used for inspiration should be cited appropriately in the dissertation report. Where external links appear in the notebook, they are treated as references rather than claims of authorship.

## Future Improvements
Realistic extensions that would strengthen the work beyond the current dissertation scope include:

- Add a `requirements.txt` or environment file to make dependency installation fully reproducible.
- Refactor modelling code into small Python modules while keeping the notebook as the narrative driver.
- Extend experiments to FD002–FD004 with careful control of operational conditions and fault modes.
- Add ablation studies (feature subsets, window length for sequence models, scaling choices).
- Strengthen evaluation with systematic cross-validation and uncertainty/robustness analysis where appropriate.

## References / Acknowledgements
- A. Saxena, K. Goebel, D. Simon, and N. Eklund, “Damage Propagation Modeling for Aircraft Engine Run-to-Failure Simulation”, *Proceedings of PHM08*, Denver, CO, 2008. (C-MAPSS dataset source; see `readme.txt` and `Damage Propagation Modeling.pdf`.)
- Core libraries used in the implementation: NumPy, pandas, scikit-learn, matplotlib, seaborn, tqdm. Optional: TensorFlow/Keras, XGBoost.

## Suggested Evidence Mapping for Dissertation
| Dissertation Component | Supporting Repository Evidence |
|---|---|
| Rationale, scope, objectives | `README.md` (Project Overview, Scope, Methodology Overview), `Main.ipynb` narrative sections |
| Dataset understanding | `readme.txt`, `data_flowchart.png`, `data_dictionary_table.png`, `data_dictionary.csv` |
| Technical implementation | `Main.ipynb` code cells for preprocessing, modelling, and evaluation |
| Data preparation and normalisation | `normalization_diagram.png`, preprocessing steps in `Main.ipynb` |
| Experiments and outputs | `outputs/run_*/` folders with timestamped artefacts and `stdout.log` |
| Evaluation design and metrics | `Main.ipynb` metric calculations, plots, confusion matrices/ROC where executed |
| Reflection and limitations | Limitations section in this README + dissertation discussion aligned to observed behaviour/results |
| Presentation and documentation quality | Clear structure in `README.md` + exported visual artefacts and tables |

---

### Placeholder checklist (fill manually)
- `[insert model name]` in “Key Findings Summary” (based on your final reported results).
- `[insert short summary]` of the main observed trade-offs (from your evaluation chapter).
- `[insert figure/table references]` to point to the exact plots/tables you cite in the dissertation (e.g., “Figure 4.2: …”).
