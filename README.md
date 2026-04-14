# Predictive Maintenance for Aircraft Turbofan Engines  
## Remaining Useful Life Prediction using NASA C-MAPSS FD001

This repository contains my final-year project on **predictive maintenance**, where I explored how machine learning can be used to estimate the **Remaining Useful Life (RUL)** of aircraft turbofan engines using the **NASA C-MAPSS FD001 dataset**.

The main goal of the project was to see how well different machine learning approaches could learn patterns of engine degradation from sensor data and use those patterns to predict how many operating cycles an engine has left before failure. Since aircraft maintenance is a safety-critical and expensive area, this kind of work has strong practical value as well as academic relevance.

I developed this project as part of my undergraduate work in **Data Science and Artificial Intelligence**, with a focus on building something that was technically solid, clearly structured, and relevant to a real industrial problem.

---

## About the Project

In industries like aviation, maintenance decisions are extremely important. If maintenance is done too early, parts may be replaced before they actually need to be, which increases cost. If it is done too late, the risk of failure becomes much more serious. Predictive maintenance tries to solve this problem by using data to estimate the health of a system before it breaks down.

In this project, I used the NASA C-MAPSS turbofan engine dataset to study whether machine learning models could predict engine degradation over time and estimate the remaining life of an engine based on operational settings and sensor readings.

The project is mainly focused on **RUL prediction as a regression task**, but it also connects this idea to maintenance decision-making in a more practical sense.

---

## Aim

To investigate how effectively machine learning models can predict the Remaining Useful Life of aircraft turbofan engines using multivariate time-series sensor data.

---

## Objectives

- understand the structure of the NASA C-MAPSS FD001 dataset  
- preprocess the raw engine sensor data properly  
- calculate RUL targets for each engine trajectory  
- train and compare different machine learning models  
- evaluate model performance using suitable metrics  
- interpret the results in the context of predictive maintenance  

---

## Dataset

This project uses the **NASA C-MAPSS** dataset, which is a well-known benchmark in predictive maintenance research.

The repository currently focuses on the **FD001** subset, which contains:
- one operating condition
- one fault mode
- multiple engine run-to-failure trajectories

### Files included

- `train_FD001.txt` — training data containing full run-to-failure engine trajectories  
- `test_FD001.txt` — test data containing partial engine trajectories  
- `RUL_FD001.txt` — true remaining useful life values for the test engines  
- `Predictive_Maintainence_on_NASA_CMAPS_DATASET.ipynb` — the main notebook for the full analysis  

Each row in the dataset represents one engine cycle and includes:
- engine ID  
- cycle number  
- operational setting values  
- multiple sensor measurements  

---

## Method

The notebook follows a full machine learning workflow from raw data to model evaluation.

### 1. Data loading
The raw text files are loaded and organised into a usable tabular format with appropriate column names.

### 2. Data preparation
The data is cleaned, unnecessary columns are removed, and features that add little value are filtered out.

### 3. RUL calculation
For the training set, Remaining Useful Life is calculated by subtracting the current cycle from the maximum cycle reached by each engine.

### 4. Feature scaling
Normalisation is applied where needed so that the models can learn from the data more effectively.

### 5. Model training
The project explores multiple approaches, including:
- Random Forest  
- XGBoost  
- LSTM-based modelling  

### 6. Evaluation
The models are compared using common regression metrics such as:
- MAE  
- RMSE  
- R²  

Plots are also used to compare predicted and actual RUL values.

---

## Repository Structure

```text
.
├── Predictive_Maintainence_on_NASA_CMAPS_DATASET.ipynb
├── README.md
├── train_FD001.txt
├── test_FD001.txt
├── RUL_FD001.txt
├── data_attributes.png
├── data_dictionary_table.png
├── data_flowchart.png
└── normalization_diagram.png
Visual Assets

The repository also includes some supporting visuals that help explain the dataset and workflow more clearly:

data_flowchart.png — overview of the project pipeline
data_dictionary_table.png — explanation of the dataset columns
data_attributes.png — summary of key data attributes
normalization_diagram.png — illustration of the preprocessing and scaling stage

These were included to make the project easier to follow and to support the written dissertation.

Why this Project Matters

Predictive maintenance is one of the most useful real-world applications of machine learning because it connects data analysis directly to cost, safety, and decision-making. In aviation, being able to estimate engine health more accurately could help reduce downtime, avoid unnecessary maintenance, and improve operational planning.

From an academic point of view, this project also gave me the chance to work on:

multivariate time-series data
regression modelling
feature engineering
model comparison
applied machine learning in an industrial context
Running the Project

This project is notebook-based, so the easiest way to run it is through Jupyter Notebook or Google Colab.

Main libraries used
pip install numpy pandas matplotlib scikit-learn xgboost tensorflow keras
Steps
Clone the repository
Make sure the FD001 dataset files are in the same directory as the notebook
Open Predictive_Maintainence_on_NASA_CMAPS_DATASET.ipynb
Run the cells in order
Limitations

This project was developed within the scope of a final-year undergraduate dissertation, so it has some clear boundaries:

it focuses only on the FD001 subset
the work is mainly notebook-based rather than fully modularised
the results depend on the preprocessing and modelling choices used here
this is a benchmark-based academic project, not a production deployment system
Future Improvements

There are several ways this project could be extended in the future:

testing on FD002, FD003, and FD004
improving feature engineering and validation strategy
refactoring the notebook into cleaner Python modules
adding uncertainty estimation for more realistic maintenance support
comparing deep learning models more extensively
Conclusion

This project was an opportunity to apply machine learning to a meaningful industrial problem and explore how predictive models can be used in maintenance forecasting. While the work is academic in scope, it reflects the kind of thinking and workflow used in real predictive maintenance problems: understanding the data, building a reliable pipeline, comparing models, and interpreting results carefully.

Overall, the project helped me strengthen both my technical skills and my understanding of how data science can be applied to practical engineering challenges.

References
Saxena, A. and Goebel, K. (2008) Turbofan Engine Degradation Simulation Data Set. NASA Ames Prognostics Data Repository.
Saxena, A., Goebel, K., Simon, D. and Eklund, N. (2008) Damage Propagation Modeling for Aircraft Engine Run-to-Failure Simulation. PHM08.
Author

Sanchit Sood
Final-year undergraduate project in Data Science and Artificial Intelligence
