# N-CMAPSS Dataset: Comprehensive Technical Summary

## 1. Executive Overview
**Dataset Name:** N-CMAPSS (New Commercial Modular Aero-Propulsion System Simulation)
**Source:** NASA Ames Research Center (Arias et al.)
**Domain:** Prognostics and Health Management (PHM) for Aircraft Turbofan Engines
**Primary Goal:** Remaining Useful Life (RUL) Prediction under realistic flight conditions.

## 2. Dataset Significance
Unlike the legacy C-MAPSS dataset (2008) which simulated engines only during stable cruise conditions, **N-CMAPSS (2021)** introduces:
*   **Real Flight Envelopes:** Data covers complete flight cycles including ascent, cruise, and descent.
*   **Dynamic Conditions:** Engines operate under varying Altitude, Mach number, and Throttle settings.
*   **High Fidelity:** ~6.5 million timestamps sampled at 1Hz.
*   **Complex Failure Modes:** Includes single-component (HPT) and multi-component (HPT + LPT) degradation.

## 3. Data Structure & Organization
The data is distributed in **HDF5 (.h5)** format, facilitating efficient storage of large time-series matrices.

### 3.1 Hierarchy
Each dataset file (e.g., `N-CMAPSS_DS02.h5`) is split into:
*   **Development Set (`_dev`):** Training data (Run-to-failure trajectories).
*   **Test Set (`_test`):** Evaluation data (Trajectories truncated before failure).

### 3.2 Variable Groups (Feature Sets)
For every timestep $t$, the following vectors are provided:

| Variable | Name | Dim | Description | Examples |
| :--- | :--- | :--- | :--- | :--- |
| **W** | **Operating Conditions** | 4 | External environment & pilot controls | Altitude (`alt`), Mach (`Mach`), Throttle (`TRA`), Inlet Temp (`T2`) |
| **X_s** | **Physical Sensors** | 14 | Direct measurements from engine sensors | Fan Speed (`Nf`), Core Speed (`Nc`), Pressures (`P2`, `P30`), Temps (`T24`, `T50`) |
| **X_v** | **Virtual Sensors** | 14 | Model-based estimates of unmeasurable states | Stall Margins (`SmFan`, `SmHPC`), Flow Rates, Thermodynamic States |
| **T** | **Degradation Labels** | 10 | Ground truth health parameters (The "Damage") | Efficiency Modifiers (`fan_eff_mod`, `HPT_eff_mod`), Flow Modifiers |
| **Y** | **Target Variable** | 1 | **Remaining Useful Life (RUL)** | Number of flight cycles remaining until failure |
| **A** | **Auxiliary Data** | 4 | Metadata for tracking | Unit ID, Cycle Number, Flight Class, Health State |

## 4. Dataset Variants (DS01 - DS08)
The database is divided into subsets to test model generalization across different conditions:

| Dataset | Failure Mode | Operating Condition | Notes |
| :--- | :--- | :--- | :--- |
| **DS01** | HPT Efficiency Degradation | Flight Conditions A | Baseline dataset |
| **DS02** | HPT + LPT Degradation | Flight Conditions A | More complex multi-fault scenarios |
| **DS03** | HPT Efficiency | Flight Conditions B | Different flight envelope |
| **DS04-08**| Mixed / Various | Mixed | Tests robustness across fleets and conditions |

## 5. Technical Specifications for Research
*   **Sampling Rate:** 1 Hz (1 record per second).
*   **Sequence Length:** Variable per flight cycle (depends on flight duration).
*   **Total Volume:** Gigabytes of floating-point data (e.g., DS02 is ~2.3GB).
*   **Preprocessing Needs:**
    *   **Normalization:** Essential due to varying scales (e.g., Temperature vs. Pressure).
    *   **Windowing:** Sliding window approach (e.g., window size 30-50) is standard for CNN/LSTM inputs.
    *   **Condition Normalization:** Since sensor values depend heavily on operating conditions (`W`), models must learn to distinguish between "high temperature due to throttle" and "high temperature due to failure."

## 6. Research Potential
This dataset is currently the **state-of-the-art benchmark** for:
*   Deep Learning (CNN, LSTM, Transformers).
*   Domain Adaptation (Transfer learning between DS01 and DS02).
*   Physics-Informed Machine Learning (using `X_v` virtual sensors).
