#!/usr/bin/env python3
"""
N-CMAPSS Complete Statistical Analysis - Final Report
This script performs comprehensive statistical analysis following your exact requirements
"""

import h5py
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("N-CMAPSS STATISTICAL ANALYSIS - COMPREHENSIVE REPORT")
print("="*80)

# Step 1: Load DS01 Development Data
print("\n1. LOADING DS01 DEVELOPMENT DATA...")
try:
    filename = 'N-CMAPSS_DS01-005.h5'
    
    with h5py.File(filename, 'r') as hdf:
        # Load all development data
        W_dev = np.array(hdf.get('W_dev'))
        X_s_dev = np.array(hdf.get('X_s_dev'))
        X_v_dev = np.array(hdf.get('X_v_dev'))
        T_dev = np.array(hdf.get('T_dev'))
        Y_dev = np.array(hdf.get('Y_dev'))
        A_dev = np.array(hdf.get('A_dev'))
        
        # Load variable names and clean them
        W_var = [str(x).replace("b'", "").replace("'", "") for x in np.array(hdf.get('W_var'))]
        X_s_var = [str(x).replace("b'", "").replace("'", "") for x in np.array(hdf.get('X_s_var'))]
        X_v_var = [str(x).replace("b'", "").replace("'", "") for x in np.array(hdf.get('X_v_var'))]
        T_var = [str(x).replace("b'", "").replace("'", "") for x in np.array(hdf.get('T_var'))]
        A_var = [str(x).replace("b'", "").replace("'", "") for x in np.array(hdf.get('A_var'))]
    
    print(f"✅ Data loaded successfully!")
    print(f"   W (Operating Conditions): {W_dev.shape}")
    print(f"   X_s (Physical Sensors): {X_s_dev.shape}")
    print(f"   X_v (Virtual Sensors): {X_v_dev.shape}")
    print(f"   T (Degradation): {T_dev.shape}")
    print(f"   Y (RUL): {Y_dev.shape}")
    print(f"   A (Auxiliary): {A_dev.shape}")
    
except Exception as e:
    print(f"❌ Error loading data: {e}")
    exit(1)

# Step 2: Build Clean DataFrame
print("\n2. BUILDING CLEAN DATAFRAME...")
try:
    # Combine all features except RUL (which we'll add separately)
    features = np.hstack([W_dev, X_s_dev, X_v_dev, T_dev, A_dev])
    
    # Create column names (excluding RUL for now)
    column_names = W_var + X_s_var + X_v_var + T_var + A_var
    
    # Create DataFrame
    df = pd.DataFrame(features, columns=column_names)
    
    # Add RUL as separate column
    df['RUL'] = Y_dev.flatten()
    
    print(f"✅ DataFrame created: {df.shape}")
    print(f"   Total features: {len(df.columns)}")
    print(f"   Operating conditions: {len(W_var)} ({W_var})")
    print(f"   Physical sensors: {len(X_s_var)} ({X_s_var[:3]}...)")
    print(f"   Virtual sensors: {len(X_v_var)} ({X_v_var[:3]}...)")
    print(f"   Degradation params: {len(T_var)} ({T_var[:3]}...)")
    print(f"   Auxiliary: {len(A_var)} ({A_var})")
    
except Exception as e:
    print(f"❌ Error creating DataFrame: {e}")
    exit(1)

# A) DESCRIPTIVE STATISTICS - THE "WHAT IS THIS DATA?" STEP
print("\n" + "="*80)
print("A) DESCRIPTIVE STATISTICS - COMPREHENSIVE ANALYSIS")
print("="*80)

print(f"\n📊 DATASET OVERVIEW:")
print(f"   Total timestamps: {len(df):,}")
print(f"   Unique engine units: {df['unit'].nunique()}")
print(f"   RUL range: {df['RUL'].min():.1f} to {df['RUL'].max():.1f} cycles")
print(f"   Mean RUL: {df['RUL'].mean():.1f} cycles")

# Check for missing values
missing = df.isnull().sum()
if missing.sum() > 0:
    print(f"⚠️  Missing values found: {missing.sum()}")
    print(missing[missing > 0])
else:
    print("✅ No missing values found!")

# Operating conditions summary
print(f"\n🛩️  OPERATING CONDITIONS SUMMARY:")
print(f"   Altitude range: {df['alt'].min():.0f} to {df['alt'].max():.0f} ft")
print(f"   Mach range: {df['Mach'].min():.2f} to {df['Mach'].max():.2f}")
print(f"   TRA range: {df['TRA'].min():.1f}% to {df['TRA'].max():.1f}%")
print(f"   T2 range: {df['T2'].min():.0f} to {df['T2'].max():.0f} °R")

# Data quality checks
print(f"\n🔍 DATA QUALITY CHECKS:")
pressure_cols = [col for col in df.columns if 'P' in col and col not in ['TRA', 'RUL']]
issues_found = 0
for col in pressure_cols[:5]:  # Check first 5 pressure columns
    neg_count = (df[col] < 0).sum()
    if neg_count > 0:
        print(f"⚠️  {col}: {neg_count} negative values found!")
        issues_found += 1

if issues_found == 0:
    print("✅ No negative pressure values found in checked columns")

# Detailed statistics for key sensor groups
print(f"\n📈 DETAILED STATISTICS BY SENSOR GROUP:")

# Operating conditions
print(f"\n   OPERATING CONDITIONS (W variables):")
w_stats = df[W_var].describe()
for var in W_var:
    stats_row = w_stats.loc[:, var]
    print(f"   {var:8s}: Mean={stats_row['mean']:8.1f}, Std={stats_row['std']:8.1f}, Min={stats_row['min']:8.1f}, Max={stats_row['max']:8.1f}")

# Key physical sensors
key_sensors = ['T50', 'Nf', 'Nc', 'P50', 'T24', 'T30']
available_key_sensors = [s for s in key_sensors if s in df.columns]
if available_key_sensors:
    print(f"\n   KEY PHYSICAL SENSORS:")
    sensor_stats = df[available_key_sensors].describe()
    for var in available_key_sensors:
        stats_row = sensor_stats.loc[:, var]
        print(f"   {var:8s}: Mean={stats_row['mean']:8.1f}, Std={stats_row['std']:8.1f}, Min={stats_row['min']:8.1f}, Max={stats_row['max']:8.1f}")

# B) CORRELATION WITH RUL - FIRST SIGNAL CHECK
print("\n" + "="*80)
print("B) CORRELATION WITH RUL - FIRST SIGNAL CHECK")
print("="*80)

# Pearson correlation (linear)
print(f"\n📊 PEARSON CORRELATION (Linear Relationship):")
pearson_corr = df.corr()['RUL'].abs().sort_values(ascending=False)
print(f"   Top 10 features by Pearson correlation with RUL:")
for i, (feature, corr) in enumerate(pearson_corr.head(10).items(), 1):
    if feature != 'RUL':  # Skip RUL itself
        print(f"   {i:2d}. {feature:15s}: {corr:.3f}")

# Spearman correlation (monotonic, more robust)
print(f"\n📊 SPEARMAN CORRELATION (Monotonic Relationship):")
spearman_corr = df.corr(method='spearman')['RUL'].abs().sort_values(ascending=False)
print(f"   Top 10 features by Spearman correlation with RUL:")
for i, (feature, corr) in enumerate(spearman_corr.head(10).items(), 1):
    if feature != 'RUL':  # Skip RUL itself
        print(f"   {i:2d}. {feature:15s}: {corr:.3f}")

# Degradation parameters (ground truth)
print(f"\n🔬 DEGRADATION PARAMETERS (Ground Truth - T variables):")
t_correlations = pearson_corr[T_var].sort_values(ascending=False)
for feature, corr in t_correlations.items():
    if not pd.isna(corr):
        print(f"   {feature:20s}: {corr:.3f}")

# C) CONDITION-AWARE STATISTICS - CRITICAL FOR N-CMAPSS
print("\n" + "="*80)
print("C) CONDITION-AWARE STATISTICS - CRITICAL FOR N-CMAPSS")
print("="*80)

# Create operating condition bins
df['alt_bin'] = pd.cut(df['alt'], bins=3, labels=['Low', 'Medium', 'High'])
df['Mach_bin'] = pd.cut(df['Mach'], bins=2, labels=['Low', 'High'])
df['TRA_bin'] = pd.cut(df['TRA'], bins=3, labels=['Low', 'Medium', 'High'])

print(f"\n🎯 SENSOR BEHAVIOR BY OPERATING CONDITIONS:")
print(f"   (Mean ± Std for key sensors across different flight conditions)")

key_sensors = ['T50', 'Nf', 'Nc', 'P50']
available_key_sensors = [s for s in key_sensors if s in df.columns]

for sensor in available_key_sensors:
    print(f"\n   📡 {sensor}:")
    condition_stats = df.groupby(['alt_bin', 'Mach_bin'])[sensor].agg(['mean', 'std'])
    for (alt, mach), stats_row in condition_stats.iterrows():
        mean_val = stats_row['mean']
        std_val = stats_row['std']
        print(f"      {alt:6s} Alt, {mach:4s} Mach: {mean_val:8.1f} ± {std_val:6.1f}")

# D) EARLY-LIFE VS LATE-LIFE COMPARISON
print("\n" + "="*80)
print("D) EARLY-LIFE VS LATE-LIFE COMPARISON")
print("="*80)

# Define RUL categories
df['lifecycle_stage'] = pd.cut(df['RUL'], 
                               bins=[0, 20, 50, 100, float('inf')],
                               labels=['Near_Failure', 'Late_Life', 'Mid_Life', 'Early_Life'])

print(f"\n📅 LIFECYCLE STAGE DISTRIBUTION:")
stage_counts = df['lifecycle_stage'].value_counts()
for stage, count in stage_counts.items():
    percentage = (count / len(df)) * 100
    print(f"   {stage:12s}: {count:8,} timestamps ({percentage:5.1f}%)")

print(f"\n🔍 SENSOR CHANGES ACROSS LIFECYCLE:")
print(f"   (Mean values by lifecycle stage)")

lifecycle_means = df.groupby('lifecycle_stage')[available_key_sensors].mean()
for stage in ['Early_Life', 'Mid_Life', 'Late_Life', 'Near_Failure']:
    if stage in lifecycle_means.index:
        print(f"\n   {stage:12s}:")
        for sensor in available_key_sensors:
            mean_val = lifecycle_means.loc[stage, sensor]
            print(f"      {sensor:4s}: {mean_val:8.1f}")

# Statistical significance test
print(f"\n📊 STATISTICAL SIGNIFICANCE (Early vs Near-Failure):")
early_life = df[df['lifecycle_stage'] == 'Early_Life']
near_failure = df[df['lifecycle_stage'] == 'Near_Failure']

if len(early_life) > 0 and len(near_failure) > 0:
    for sensor in available_key_sensors:
        if sensor in early_life.columns and sensor in near_failure.columns:
            statistic, p_value = stats.mannwhitneyu(early_life[sensor], near_failure[sensor])
            significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "ns"
            early_mean = early_life[sensor].mean()
            late_mean = near_failure[sensor].mean()
            effect_size = abs(early_mean - late_mean) / early_life[sensor].std()
            print(f"   {sensor:4s}: p={p_value:.2e} {significance} (effect size: {effect_size:.2f})")

print(f"\n   Significance levels: *** p<0.001, ** p<0.01, * p<0.05, ns = not significant")

# E) BETWEEN-ENGINE VS WITHIN-ENGINE VARIATION
print("\n" + "="*80)
print("E) BETWEEN-ENGINE VS WITHIN-ENGINE VARIATION")
print("="*80)

print(f"\n📊 VARIATION SOURCE ANALYSIS:")
print(f"   (Higher 'Between_Engine_Ratio' = more variation between different engines)")
print(f"   (Lower ratio = more variation within same engine over time - better for degradation tracking)")

variation_analysis = {}
for sensor in available_key_sensors:
    # Overall variance
    total_var = df[sensor].var()
    
    # Between-engine variance (variance of unit means)
    unit_means = df.groupby('unit')[sensor].mean()
    between_engine_var = unit_means.var()
    
    # Within-engine variance (average of within-unit variances)
    within_engine_var = df.groupby('unit')[sensor].var().mean()
    
    variation_analysis[sensor] = {
        'Total_Variance': total_var,
        'Between_Engine_Variance': between_engine_var,
        'Within_Engine_Variance': within_engine_var,
        'Between_Engine_Ratio': between_engine_var / total_var if total_var > 0 else 0
    }

# Create summary table
variation_df = pd.DataFrame(variation_analysis).T

print(f"\n   Results:")
for sensor in available_key_sensors:
    ratio = variation_df.loc[sensor, 'Between_Engine_Ratio']
    between_var = variation_df.loc[sensor, 'Between_Engine_Variance']
    within_var = variation_df.loc[sensor, 'Within_Engine_Variance']
    
    interpretation = "Good for degradation" if ratio < 0.3 else "Mixed" if ratio < 0.7 else "Engine-specific"
    
    print(f"   {sensor:4s}: Between/Total = {ratio:.3f} ({interpretation})")
    print(f"         Between-engine var: {between_var:8.1f}")
    print(f"         Within-engine var:  {within_var:8.1f}")

# F) BUILD STATISTICAL BASELINE MODEL
print("\n" + "="*80)
print("F) STATISTICAL BASELINE MODEL")
print("="*80)

# Select only numeric features for correlation analysis
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
numeric_cols = [col for col in numeric_cols if col != 'RUL']  # Exclude target variable

# Select features with highest RUL correlation (excluding T variables to avoid leakage)
predictive_cols = [col for col in numeric_cols if col not in T_var]
correlation_scores = df[predictive_cols].corrwith(df['RUL']).abs().sort_values(ascending=False)

print(f"\n🔍 TOP 10 PREDICTIVE FEATURES (excluding T variables):")
for i, (feature, corr) in enumerate(correlation_scores.head(10).items(), 1):
    print(f"   {i:2d}. {feature:20s}: {corr:.3f}")

# Use top 10 features for baseline
top_features = correlation_scores.head(10).index.tolist()
X = df[top_features]
y = df['RUL']

# Split by engine unit (important! not by rows)
unique_units = df['unit'].unique()
np.random.seed(42)
train_units = np.random.choice(unique_units, size=int(0.7 * len(unique_units)), replace=False)
test_units = [unit for unit in unique_units if unit not in train_units]

train_mask = df['unit'].isin(train_units)
test_mask = df['unit'].isin(test_units)

X_train, X_test = X[train_mask], X[test_mask]
y_train, y_test = y[train_mask], y[test_mask]

print(f"\n📊 TRAIN/TEST SPLIT:")
print(f"   Training units: {len(train_units)} ({len(X_train):,} samples)")
print(f"   Test units: {len(test_units)} ({len(X_test):,} samples)")

# Train baseline model
baseline_model = LinearRegression()
baseline_model.fit(X_train, y_train)

# Evaluate
y_pred = baseline_model.predict(X_test)

mae = np.mean(np.abs(y_test - y_pred))
rmse = np.sqrt(np.mean((y_test - y_pred)**2))

print(f"\n🎯 BASELINE MODEL PERFORMANCE:")
print(f"   MAE:  {mae:.2f} cycles")
print(f"   RMSE: {rmse:.2f} cycles")

# Compare with naive baseline (always predict mean)
naive_pred = np.full_like(y_test, y_train.mean())
naive_mae = np.mean(np.abs(y_test - naive_pred))
naive_rmse = np.sqrt(np.mean((y_test - naive_pred)**2))

print(f"\n📈 COMPARISON WITH NAIVE BASELINE:")
print(f"   Naive MAE:  {naive_mae:.2f} cycles")
print(f"   Naive RMSE: {naive_rmse:.2f} cycles")
print(f"   Improvement: {(naive_mae - mae)/naive_mae * 100:.1f}% MAE reduction")

# FINAL SUMMARY
print("\n" + "="*80)
print("🎯 STATISTICAL ANALYSIS SUMMARY")
print("="*80)

print(f"✅ Successfully analyzed {len(df):,} timestamps from {df['unit'].nunique()} engine units")
print(f"✅ Identified {len([f for f in correlation_scores.head(10).index if f not in T_var])} strong predictive features")
print(f"✅ Built baseline model with MAE: {mae:.2f} cycles")

# Count good sensors for degradation
good_sensors = len([s for s in available_key_sensors if variation_df.loc[s, 'Between_Engine_Ratio'] < 0.3])
print(f"✅ Key insight: {good_sensors} sensors show strong within-engine variation (good for degradation tracking)")

print(f"\n🔍 KEY FINDINGS:")
print(f"   • Highest RUL correlation: {correlation_scores.index[0]} ({correlation_scores.iloc[0]:.3f})")
print(f"   • Best degradation sensor: {min(variation_df.index, key=lambda x: variation_df.loc[x, 'Between_Engine_Ratio'])}")
print(f"   • Baseline improvement: {(naive_mae - mae)/naive_mae * 100:.1f}% over naive predictor")

print(f"\n🚀 NEXT STEPS FOR DEEP LEARNING:")
print(f"   1. Use condition-normalized features (z-scores within operating condition bins)")
print(f"   2. Focus on sensors with high within-engine variation: {[s for s in available_key_sensors if variation_df.loc[s, 'Between_Engine_Ratio'] < 0.3]}")
print(f"   3. Consider temporal modeling with LSTM/Transformer for sequence dependencies")
print(f"   4. This baseline (MAE: {mae:.2f}) gives us a target to beat!")

print("\n" + "="*80)
print("ANALYSIS COMPLETE - READY FOR DEEP LEARNING MODELING")
print("="*80)