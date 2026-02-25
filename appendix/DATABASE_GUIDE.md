# N-CMAPSS Database - Complete Guide

## 📋 Table of Contents
1. [Overview](#overview)
2. [Database Purpose](#database-purpose)
3. [Data Structure](#data-structure)
4. [Detailed Explanation of Each Component](#detailed-explanation)
5. [How Data is Organized](#how-data-is-organized)
6. [Dataset Variants (DS01-DS08)](#dataset-variants)
7. [Practical Example](#practical-example)
8. [Key Concepts](#key-concepts)

---

## Overview

**Dataset Name:** N-CMAPSS (NASA Commercial Modular Aero-Propulsion System Simulation)

**File Format:** HDF5 (Hierarchical Data Format 5)

**Source:** NASA, created by Manuel Arias

**Total Data:** ~6.5 Million timestamps across all datasets

**Available Datasets:** 10 variants (DS01-DS08d)

### Available Dataset Files

| Dataset | File Size | File Name |
|---------|-----------|-----------|
| DS01 | 2,740 MB | N-CMAPSS_DS01-005.h5 |
| DS02 | 2,337 MB | N-CMAPSS_DS02-006.h5 |
| DS03 | 3,522 MB | N-CMAPSS_DS03-012.h5 |
| DS04 | 3,579 MB | N-CMAPSS_DS04.h5 |
| DS05 | 2,479 MB | N-CMAPSS_DS05.h5 |
| DS06 | 2,431 MB | N-CMAPSS_DS06.h5 |
| DS07 | 2,589 MB | N-CMAPSS_DS07.h5 |
| DS08a | 3,087 MB | N-CMAPSS_DS08a-009.h5 |
| DS08c | 2,301 MB | N-CMAPSS_DS08c-008.h5 |
| DS08d | 2,751 MB | N-CMAPSS_DS08d-010.h5 |

---

## Database Purpose

This database is designed for **Predictive Maintenance** and **Remaining Useful Life (RUL) Prediction** of aircraft turbofan engines.

### Real-World Application
- **Industry:** Commercial Aviation & Aerospace
- **Problem:** Predict when an engine will fail so maintenance can be scheduled before failure
- **Benefit:** Prevents catastrophic failures, saves costs, improves safety

### How It Works in Practice
1. Data is collected during engine operation (flight cycles)
2. Sensors record engine performance at thousands of timesteps
3. Engine parameters degrade gradually over its lifetime
4. Eventually, the engine reaches a failure point
5. The goal is to **predict failure before it happens** using time series data

---

## Data Structure

### File Organization (HDF5 Format)

Each file contains 17 datasets organized as:

```
N-CMAPSS_DSxx.h5
├── Development Set (Training Data)
│   ├── W_dev      - Operating conditions
│   ├── X_s_dev    - Physical sensor readings
│   ├── X_v_dev    - Virtual sensors
│   ├── T_dev      - Degradation parameters
│   ├── Y_dev      - Remaining Useful Life (RUL)
│   └── A_dev      - Auxiliary information
├── Test Set (Evaluation Data)
│   ├── W_test, X_s_test, X_v_test, T_test, Y_test, A_test
├── Variable Names (Metadata)
│   ├── W_var, X_s_var, X_v_var, T_var, A_var
```

### Size and Capacity (Example: DS02)

| Component | Dev Set | Test Set | Columns |
|-----------|---------|----------|---------|
| **W (Conditions)** | 5.26M rows | 1.25M rows | 4 |
| **X_s (Sensors)** | 5.26M rows | 1.25M rows | 14 |
| **X_v (Virtual)** | 5.26M rows | 1.25M rows | 14 |
| **T (Degradation)** | 5.26M rows | 1.25M rows | 10 |
| **Y (RUL)** | 5.26M rows | 1.25M rows | 1 |
| **A (Auxiliary)** | 5.26M rows | 1.25M rows | 4 |

**Total** = ~6.5 million timesteps

---

## Detailed Explanation

### 1. Operating Conditions (W) - 4 Variables

These describe the **external flight environment** at each timestep:

| Variable | Description | Units | Typical Range |
|----------|-------------|-------|----------------|
| `alt` | Flight altitude | Feet (ft) | 0 - 40,000 |
| `Mach` | Speed relative to sound | Mach number (ratio) | 0 - 0.8 |
| `TRA` | Throttle Resolver Angle | Percentage (%) | 0 - 100 |
| `T2` | Temperature at fan inlet | Rankine (°R) | 300 - 600 |

**What it means:** These 4 values describe how the engine is being operated at any given moment. Different flight conditions (takeoff vs. cruise) have different W values.

---

### 2. Physical Sensor Readings (X_s) - 14 Variables

These are **actual measurements** from sensors installed on the engine:

| Variable | Description |
|----------|-------------|
| `T24` | Temperature after fan (relative) |
| `T30` | Temperature after LPC (Low Pressure Compressor) |
| `T48` | Temperature after HPC (High Pressure Compressor) |
| `T50` | Temperature after HPT (High Pressure Turbine) |
| `P15` | Pressure before fan (relative) |
| `P2` | Pressure after fan |
| `P21` | Pressure after duct |
| `P24` | Pressure at engine inlet |
| `Ps30` | Static pressure after LPC |
| `P40` | Pressure after HPC |
| `P50` | Pressure after LPT |
| `Nf` | Fan speed (RPM) |
| `Nc` | Core engine speed (RPM) |
| `Wf` | Air flow rate (lbm/s) |

**What it means:** These are like the "vital signs" of the engine - temperatures and pressures at key points, plus speeds and flow rates. As the engine degrades, these values change.

---

### 3. Virtual Sensors (X_v) - 14 Variables

These are **calculated/derived** values that cannot be directly measured:

| Variable | Description |
|----------|-------------|
| `T40` | Temperature after HPC (estimated) |
| `P30` | Pressure in LPC discharge (estimated) |
| `P45` | Pressure in HPT discharge (estimated) |
| `W21` - `W32`, `W48`, `W50` | Various airflow rates (calculated) |
| `SmFan` | Fan surge margin (efficiency indicator) |
| `SmLPC` | LPC surge margin (efficiency indicator) |
| `SmHPC` | HPC surge margin (efficiency indicator) |
| `phi` | Engine operating point (calculated) |

**Why separate from X_s?**
- Some engine parameters can't be directly measured (too hot, too inaccessible)
- These are **estimated using physics equations** and the physical sensors
- Useful for understanding engine behavior
- Could be corrupted/inaccurate if based on unreliable X_s values

---

### 4. Degradation Parameters (T) - 10 Variables

These represent **engine wear/deterioration** over time:

| Variable | Description |
|----------|-------------|
| `fan_eff_mod` | Fan efficiency modifier (1.0 = healthy, <1.0 = degraded) |
| `fan_flow_mod` | Fan flow capacity modifier |
| `LPC_eff_mod` | Low Pressure Compressor efficiency modifier |
| `LPC_flow_mod` | LPC flow capacity modifier |
| `HPC_eff_mod` | High Pressure Compressor efficiency modifier |
| `HPC_flow_mod` | HPC flow capacity modifier |
| `HPT_eff_mod` | High Pressure Turbine efficiency modifier |
| `HPT_flow_mod` | HPT flow capacity modifier |
| `LPT_eff_mod` | Low Pressure Turbine efficiency modifier |
| `LPT_flow_mod` | LPT flow capacity modifier |

**What it means:**
- These are **"damage indexes"** that track how much each component has degraded
- Values start near 1.0 (healthy) and decrease as the engine ages
- Directly related to failure modes (e.g., HPT degradation, LPT degradation)
- These are the "truth labels" - they directly cause the engine to fail

**Example:** If HPT_eff_mod drops from 1.0 to 0.85, the High Pressure Turbine has lost 15% efficiency.

---

### 5. Remaining Useful Life (Y) - 1 Variable

**What it is:** The number of flight cycles remaining until engine failure

**Formula:** `Y = Cycles remaining at current timestep`

| Dataset | Min RUL | Max RUL | Mean RUL |
|---------|---------|---------|----------|
| DS02 | 0 cycles | 88 cycles | 37.3 cycles |

**What it means:**
- At the start of monitoring (first cycle), RUL is high (~88 cycles)
- As the engine operates, RUL decreases with each flight cycle
- When RUL reaches 0, the engine has failed = end of data
- This is the **target variable** for prediction models

**Examples:**
- Early operation: RUL = 88 cycles (88 flights remaining before failure)
- Mid-life: RUL = 40 cycles (40 flights remaining)
- End-of-life: RUL = 0 (engine has failed, operation stops)

---

### 6. Auxiliary Information (A) - 4 Variables

Metadata to organize and categorize the data:

| Variable | Description | Example |
|----------|-------------|---------|
| `unit` | Engine unit ID | 2, 5, 10, 16, 18, 20 |
| `cycle` | Flight cycle number | 1, 2, 3, ..., 89 |
| `Fc` | Flight class (1, 2, or 3) | 1 = short (1-3h), 2 = medium (3-5h), 3 = long (5-7h) |
| `hs` | Health state | 1 = healthy, 0 = degrading (varies by dataset) |

**DS02 Example:**
- Unit 2: 75 flight cycles, 853,142 timestep records
- Unit 5: 89 flight cycles, 1,033,420 timestep records
- Unit 10: 82 flight cycles, 952,711 timestep records
- etc.

---

## How Data is Organized

### Hierarchical Structure

```
UNIT --> CYCLE --> TIMESTEPS
```

**Example: Unit 5, Flight 1:**

During the first flight cycle of Unit 5, the engine is monitored and records many timesteps:

| Timestep | Unit | Cycle | W values | X_s values | X_v values | T values | Y value | Fc | hs |
|----------|------|-------|----------|------------|------------|----------|---------|----|----|
| 1 | 5 | 1 | [10000ft, 0.3M, 60%, 350°R] | [14 temps/pressures] | [14 virtual] | [10 degradation] | 88.0 | 1 | 1 |
| 2 | 5 | 1 | [10000ft, 0.3M, 60%, 350°R] | [14 temps/pressures] | [14 virtual] | [10 degradation] | 88.0 | 1 | 1 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| N | 5 | 1 | [10000ft, 0.3M, 60%, 350°R] | [14 temps/pressures] | [14 virtual] | [10 degradation] | 88.0 | 1 | 1 |

Each row is one timestep. Same unit, same cycle = same flight class and RUL.

**Then Flight 2 of Unit 5:**

| Timestep | Unit | Cycle | W values | X_s values | X_v values | T values | Y value | Fc | hs |
|----------|------|-------|----------|------------|------------|----------|---------|----|----|
| N+1 | 5 | 2 | [...] | [...] | [...] | [...] | 87.8 | 1 | 1 |
| ... | 5 | 2 | [...] | [...] | [...] | [...] | 87.8 | 1 | 1 |

Notice: Y decreased from 88.0 to 87.8 (1 fewer cycle remaining)

---

## Dataset Variants (DS01-DS08)

Different datasets represent different **operating conditions and failure modes**:

### What Varies Between Datasets?

1. **Different Engine Units:** Each dataset uses different engines
2. **Different Flight Conditions:** Different operating envelopes
3. **Different Failure Modes:** 
   - Some show HPT (High Pressure Turbine) degradation
   - Others show combined HPT + LPT degradation
   - Different wear patterns
4. **Different Degradation Patterns:** Wear profiles differ

### Why Multiple Datasets?

- **Generalization Testing:** Can your model work on engines it hasn't seen?
- **Robustness:** Does it work for different failure modes?
- **Transfer Learning:** How well can a model trained on DS01 predict DS02?

### Example Interpretation

- **DS01 vs DS02:** Different engine units, different flight conditions
- **DS03 vs DS04:** Different failure mode combinations
- Researchers use multiple datasets to validate model robustness

---

## Practical Example

### Scenario: Predicting Engine Unit 5's Failure

**Task:** Build a model to predict RUL using history of X_s + X_v + W + T

**Data Flow:**

```
FLIGHT 1:
  Timesteps 1-10000: W, X_s, X_v, T measurements, RUL = 88
  
FLIGHT 2:
  Timesteps 10001-20000: W, X_s, X_v, T measurements, RUL = 87
  
FLIGHT 3:
  Timesteps 20001-30000: W, X_s, X_v, T measurements, RUL = 86

... (many flights) ...

FLIGHT 88:
  Timesteps 1033350-1033420: W, X_s, X_v, T measurements, RUL = 1

FLIGHT 89:
  Timesteps 1033421-1033420: W, X_s, X_v, T measurements, RUL = 0
  [Last record before engine failure]
```

### Machine Learning Approach

**Training Phase (Development Set):**
```
INPUT: Historical sequence of [W, X_s, X_v, T] from Unit 2, 5, 10, 16, 18, 20
OUTPUT: RUL value
Learn patterns: How do sensors change as RUL decreases?
```

**Testing Phase (Test Set):**
```
INPUT: New sequence from previously unseen engine
OUTPUT: Predict RUL for each timestep
Evaluate: How accurate are predictions?
```

---

## Key Concepts

### Run-to-Failure Data

- Data collection **starts at healthy operation**
- Data collection **ends when engine fails** (RUL = 0)
- No missing middle section - captures complete degradation process
- Very valuable for predictive maintenance

### Time Series Nature

- **Sequential:** Timesteps follow a time order
- **Degradation is monotonic:** Engine can't "heal" - always gets worse
- **RUL always decreases:** 88 → 87 → 86 → ... → 0
- **Requires time series models:** LSTM, GRU, TCN, etc.

### Multivariate Time Series

- 32+ features per timestep (W + X_s + X_v + T)
- Multiple sensors provide redundant information
- Ensemble effects: correlation between different measurements

### Imbalanced Learning Challenge

- Early operation: Many timesteps with RUL = 60-88 (lots of data)
- Late operation: Few timesteps with RUL = 0-5 (data becomes critical)
- **Harder to learn final failure phase**
- Requires careful model design and sampling strategies

### Synthetic vs Real Data

- Data is **synthetically generated** using C-MAPSS simulator
- Not from real aircraft (for safety/privacy reasons)
- **Advantages:** Controlled experiments, known ground truth
- **Limitations:** May not capture all real-world complexities

---

## Summary Table

| Aspect | Details |
|--------|---------|
| **Domain** | Aerospace / Predictive Maintenance |
| **Problem** | Remaining Useful Life (RUL) Prediction |
| **Data Type** | Multivariate Time Series (Run-to-Failure) |
| **Format** | HDF5 Binary |
| **Scale** | ~6.5 million timesteps per database |
| **Features** | 38+ per timestep (4 operational + 14 sensor + 14 virtual + 10 degradation) |
| **Target** | RUL (0-88 cycles) |
| **Engines per Set** | 6-9 units |
| **Flights per Engine** | 63-89 cycles |
| **Data Split** | ~80% development / ~20% test |
| **Variants** | 10 (DS01-DS08d) |
| **Synthetic** | Yes (NASA C-MAPSS simulator) |
| **License** | NASA (Public) |

---

## Loading the Data in Python

```python
import h5py
import numpy as np

filename = 'N-CMAPSS_DS02-006.h5'

with h5py.File(filename, 'r') as hdf:
    # Development data
    W_dev = np.array(hdf.get('W_dev'))      # (5263447, 4)
    X_s_dev = np.array(hdf.get('X_s_dev')) # (5263447, 14)
    X_v_dev = np.array(hdf.get('X_v_dev')) # (5263447, 14)
    T_dev = np.array(hdf.get('T_dev'))     # (5263447, 10)
    Y_dev = np.array(hdf.get('Y_dev'))     # (5263447, 1)
    A_dev = np.array(hdf.get('A_dev'))     # (5263447, 4)
    
    # Variable names
    W_var = [str(x) for x in hdf.get('W_var')]
    X_s_var = [str(x) for x in hdf.get('X_s_var')]
    X_v_var = [str(x) for x in hdf.get('X_v_var')]
    T_var = [str(x) for x in hdf.get('T_var')]
    A_var = [str(x) for x in hdf.get('A_var')]

import pandas as pd

# Create dataframes
df_W = pd.DataFrame(W_dev, columns=W_var)
df_X_s = pd.DataFrame(X_s_dev, columns=X_s_var)
df_X_v = pd.DataFrame(X_v_dev, columns=X_v_var)
df_T = pd.DataFrame(T_dev, columns=T_var)
df_A = pd.DataFrame(A_dev, columns=A_var)
df_Y = pd.DataFrame(Y_dev, columns=['RUL'])

# Combine all
df = pd.concat([df_W, df_X_s, df_X_v, df_T, df_A, df_Y], axis=1)
```

---

## References

- **Source:** NASA Ames Research Center
- **Original Repository:** https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/
- **Creator:** Manuel Arias
- **Simulator:** Commercial Modular Aero-Propulsion System Simulation (C-MAPSS)
- **Example Notebook:** N-CMAPSS_Example_data_loading_and_exploration.ipynb

---

**Document Created:** February 19, 2026
**Dataset:** N-CMAPSS (NASA)
**Comprehensive Guide:** Every Detail Explained
