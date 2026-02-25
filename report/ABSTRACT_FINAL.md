# Research Paper Abstract

## Title
**Prognostics of Aircraft Turbofan Engines Under Complex Flight Conditions: A Deep Learning Approach Using N-CMAPSS Data**

## Abstract
**Background:** 
Accurate estimation of Remaining Useful Life (RUL) for aircraft engines is critical for predictive maintenance (PdM) strategies, aiming to enhance flight safety and reduce operational costs. While data-driven approaches have shown promise, traditional benchmarks often fail to capture the complexity of real-world flight profiles, characterized by dynamic altitude, Mach number, and throttle resolver angle variations.

**Problem:** 
Standard RUL prediction models frequently degrade in performance when applied to engines operating under diverse and non-stationary flight envelopes. The variability in sensor readings induced by flight maneuvers can be conflated with degradation signatures, leading to inaccurate prognosis. The NASA Commercial Modular Aero-Propulsion System Simulation (N-CMAPSS) dataset addresses this gap by providing high-fidelity run-to-failure trajectories that incorporate real flight conditions, presenting a more challenging and realistic scenario for prognostic modeling.

**Methodology:** 
This study proposes a robust deep learning framework designed to decouple operating condition effects from true degradation trends. We implement a hybrid architecture combining **1D Convolutional Neural Networks (1D-CNN)** for automated feature extraction from multivariate time-series data with **Long Short-Term Memory (LSTM)** networks to capture temporal degradation dependencies. To handle the non-stationarity of the N-CMAPSS data, we employ a condition-aware normalization strategy and sliding window processing. The model is trained and evaluated on the DS01 and DS02 subsets of the N-CMAPSS dataset, which feature distinct failure modes and flight classes.

**Results:** 
Experimental validation demonstrates that the proposed architecture achieves superior predictive accuracy compared to baseline statistical and traditional machine learning methods. The model effectively learns to distinguish between sensor fluctuations caused by flight maneuvers and those indicative of component degradation. Quantitative analysis reveals a significant reduction in Root Mean Square Error (RMSE) and improved Scoring Function performance, validating the approach's efficacy for real-world aircraft engine prognostics.

**Conclusion:** 
These findings underscore the importance of incorporating flight context into prognostic models. The developed framework offers a scalable solution for engine health monitoring in commercial aviation, capable of generalizing across different flight missions and engine units.

## Keywords
Predictive Maintenance; Remaining Useful Life (RUL); N-CMAPSS; Deep Learning; CNN-LSTM; Turbofan Engine; Prognostics and Health Management (PHM).
