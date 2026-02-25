#!/usr/bin/env python3
"""
N-CMAPSS Statistical Analysis - Simplified Version (No Matplotlib)
This script runs the statistical analysis workflow for understanding the dataset
"""

import h5py
import numpy as np
import pandas as pd
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("=== N-CMAPSS Statistical Analysis Starting ===")

# Step 1: Load DS01 Development Data
print("\n1. Loading DS01 development data...")
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
        
        # Load variable names
        W_var = [str(x) for x in np.array(hdf.get('W_var'))]
        X_s_var = [str(x) for x in np.array(hdf.get('X_s_var'))]
        X_v_var = [str(x) for x in np.array(hdf.get('X_v_var'))]
        T_var = [str(x) for x in np.array(hdf.get('T_var'))]
        A_var = [str(x) for x in np.array(hdf.get('A_var'))]
    
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
print("\n2. Building clean DataFrame...")
try:
    # Combine all features into one DataFrame
    features = np.hstack([W_dev, X_s_dev, X_v_dev, T_dev, A_dev])
    
    # Create column names
    column_names = W_var + X_s_var + X_v_var + T_var + A_var + ['RUL']
    
    # Create DataFrame
    df = pd.DataFrame(features, columns=column_names)
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

# Step 3: Descriptive Statistics
print("\n3. Descriptive Statistics...")
try:
    print("\n=== BASIC STATISTICS ===")
    print(f"Total timestamps: {len(df):,}")
    print(f"Unique engine units: {df['unit'].nunique()}")
    print(f"RUL range: {df['RUL'].min():.1f} to {df['RUL'].max():.1f} cycles")
    print(f"Mean RUL: {df['RUL'].mean():.1f} cycles")
    
    # Check for missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(f"⚠️  Missing values found: {missing.sum()}")
        print(missing[missing > 0])
    else:
        print("✅ No missing values found!")
    
    # Data quality checks
    print("\n=== DATA QUALITY CHECKS ===")
    
    # Check for negative pressures (should not exist)
    pressure_cols = [col for col in df.columns if 'P' in col and col not in ['TRA', 'RUL']]
    issues_found = 0
    for col in pressure_cols[:5]:  # Check first 5 pressure columns
        neg_count = (df[col] < 0).sum()
        if neg_count > 0:
            print(f"⚠️  {col}: {neg_count} negative values found!")
            issues_found += 1
    
    if issues_found == 0:
        print("✅ No negative pressure values found in checked columns")
    
    # Operating conditions summary
    print(f"\n=== OPERATING CONDITIONS SUMMARY ===")
    print(f"Altitude range: {df['alt'].min():.0f} to {df['alt'].max():.0f} ft")
    print(f"Mach range: {df['Mach'].min():.2f} to {df['Mach'].max():.2f}")
    print(f"TRA range: {df['TRA'].min():.1f}% to {df['TRA'].max():.1f}%")
    print(f"T2 range: {df['T2'].min():.0f} to {df['T2'].max():.0f} °R")
    
except Exception as e:
    print(f"❌ Error in descriptive statistics: {e}")

# Step 4: Correlation Analysis
print("\n4. Correlation Analysis with RUL...")
try:
    # Pearson correlation (linear)
    pearson_corr = df.corr()['RUL'].abs().sort_values(ascending=False)
    
    print(f"\n=== TOP 10 FEATURES BY PEARSON CORRELATION WITH RUL ===")
    for i, (feature, corr) in enumerate(pearson_corr.head(10).items(), 1):
        print(f"{i:2d}. {feature:15s}: {corr:.3f}")
    
    # Spearman correlation (monotonic, more robust)
    spearman_corr = df.corr(method='spearman')['RUL'].abs().sort_values(ascending=False)
    
    print(f"\n=== TOP 10 FEATURES BY SPEARMAN CORRELATION WITH RUL ===")
    for i, (feature, corr) in enumerate(spearman_corr.head(10).items(), 1):
        print(f"{i:2d}. {feature:15s}: {corr:.3f}")
    
    # Identify degradation parameters (T variables) - these are ground truth
    print(f"\n=== DEGRADATION PARAMETERS (GROUND TRUTH) ===")
    t_correlations = pearson_corr[T_var].sort_values(ascending=False)
    for feature, corr in t_correlations.items():
        print(f"   {feature:20s}: {corr:.3f}")
    
except Exception as e:
    print(f"❌ Error in correlation analysis: {e}")

# Step 5: Condition-Aware Analysis
print("\n5. Condition-Aware Statistics...")
try:
    # Create operating condition bins
    df['alt_bin'] = pd.cut(df['alt'], bins=3, labels=['Low', 'Medium', 'High'])
    df['Mach_bin'] = pd.cut(df['Mach'], bins=2, labels=['Low', 'High'])
    df['TRA_bin'] = pd.cut(df['TRA'], bins=3, labels=['Low', 'Medium', 'High'])
    
    # Analyze key sensors within condition bins
    key_sensors = ['T50', 'Nf', 'Nc', 'P50']
    
    print(f"\n=== SENSOR BEHAVIOR BY OPERATING CONDITIONS ===")
    print("(Mean ± Std for key sensors)")
    
    for sensor in key_sensors:
        print(f"\n{sensor}:")
        condition_stats = df.groupby(['alt_bin', 'Mach_bin'])[sensor].agg(['mean', 'std'])
        for (alt, mach), stats_row in condition_stats.iterrows():
            mean_val = stats_row['mean']
            std_val = stats_row['std']
            print(f"  {alt:6s} Alt, {mach:4s} Mach: {mean_val:8.1f} ± {std_val:6.1f}")
    
except Exception as e:
    print(f"❌ Error in condition-aware analysis: {e}")

# Step 6: Lifecycle Comparison
print("\n6. Early-Life vs Late-Life Comparison...")
try:
    # Define RUL categories
    df['lifecycle_stage'] = pd.cut(df['RUL'], 
                                   bins=[0, 20, 50, 100, float('inf')],
                                   labels=['Near_Failure', 'Late_Life', 'Mid_Life', 'Early_Life'])
    
    print(f"\n=== LIFECYCLE STAGE DISTRIBUTION ===")
    stage_counts = df['lifecycle_stage'].value_counts()
    for stage, count in stage_counts.items():
        percentage = (count / len(df)) * 100
        print(f"{stage:12s}: {count:8,} timestamps ({percentage:5.1f}%)")
    
    # Compare key sensors across lifecycle stages
    key_sensors = ['T50', 'Nf', 'Nc', 'P50']
    
    print(f"\n=== SENSOR CHANGES ACROSS LIFECYCLE ===")
    print("(Mean values by stage)")
    
    lifecycle_means = df.groupby('lifecycle_stage')[key_sensors].mean()
    for stage in ['Early_Life', 'Mid_Life', 'Late_Life', 'Near_Failure']:
        if stage in lifecycle_means.index:
            print(f"\n{stage:12s}:")
            for sensor in key_sensors:
                mean_val = lifecycle_means.loc[stage, sensor]
                print(f"  {sensor:4s}: {mean_val:8.1f}")
    
    # Statistical significance test (Mann-Whitney U test)
    print(f"\n=== STATISTICAL SIGNIFICANCE (Early vs Near-Failure) ===")
    early_life = df[df['lifecycle_stage'] == 'Early_Life']
    near_failure = df[df['lifecycle_stage'] == 'Near_Failure']
    
    if len(early_life) > 0 and len(near_failure) > 0:
        for sensor in key_sensors:
            statistic, p_value = stats.mannwhitneyu(early_life[sensor], near_failure[sensor])
            significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "ns"
            effect_size = abs(early_life[sensor].mean() - near_failure[sensor].mean()) / early_life[sensor].std()
            print(f"{sensor:4s}: p={p_value:.2e} {significance} (effect size: {effect_size:.2f})")
    
except Exception as e:
    print(f"❌ Error in lifecycle comparison: {e}")

# Step 7: Variation Source Analysis
print("\n7. Between-Engine vs Within-Engine Variation...")
try:
    # Calculate variation sources for key sensors
    variation_analysis = {}
    
    for sensor in key_sensors:
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
    
    print(f"\n=== VARIATION SOURCE ANALYSIS ===")
    print("(Higher 'Between_Engine_Ratio' means more variation between different engines)")
    print("(Lower ratio means more variation within same engine over time - better for degradation tracking)")
    print()
    
    for sensor in key_sensors:
        ratio = variation_df.loc[sensor, 'Between_Engine_Ratio']
        between_var = variation_df.loc[sensor, 'Between_Engine_Variance']
        within_var = variation_df.loc[sensor, 'Within_Engine_Variance']
        
        interpretation = "Good for degradation" if ratio < 0.3 else "Mixed" if ratio < 0.7 else "Engine-specific"
        
        print(f"{sensor:4s}: Between/Total = {ratio:.3f} ({interpretation})")
        print(f"      Between-engine var: {between_var:8.1f}")
        print(f"      Within-engine var:  {within_var:8.1f}")
        print()
    
except Exception as e:
    print(f"❌ Error in variation analysis: {e}")

# Step 8: Simple Baseline Model
print("\n8. Building Statistical Baseline Model...")
try:
    # Select features with highest RUL correlation (excluding T variables to avoid leakage)
    feature_cols = [col for col in df.columns if col not in ['RUL'] + T_var]
    correlation_scores = df[feature_cols].corrwith(df['RUL']).abs().sort_values(ascending=False)
    
    # Use top 10 features for baseline
    top_features = correlation_scores.head(10).index.tolist()
    X = df[top_features]
    y = df['RUL']
    
    print(f"\n=== TOP 10 PREDICTIVE FEATURES (excluding T variables) ===")
    for i, (feature, corr) in enumerate(correlation_scores.head(10).items(), 1):
        print(f"{i:2d}. {feature:15s}: {corr:.3f}")
    
    # Split by engine unit (important! not by rows)
    unique_units = df['unit'].unique()
    np.random.seed(42)
    train_units = np.random.choice(unique_units, size=int(0.7 * len(unique_units)), replace=False)
    test_units = [unit for unit in unique_units if unit not in train_units]
    
    train_mask = df['unit'].isin(train_units)
    test_mask = df['unit'].isin(test_units)
    
    X_train, X_test = X[train_mask], X[test_mask]
    y_train, y_test = y[train_mask], y[test_mask]
    
    print(f"\n=== TRAIN/TEST SPLIT ===")
    print(f"Training units: {len(train_units)} ({len(X_train):,} samples)")
    print(f"Test units: {len(test_units)} ({len(X_test):,} samples)")
    
    # Train baseline model
    from sklearn.linear_model import LinearRegression
    baseline_model = LinearRegression()
    baseline_model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = baseline_model.predict(X_test)
    
    mae = np.mean(np.abs(y_test - y_pred))
    rmse = np.sqrt(np.mean((y_test - y_pred)**2))
    
    print(f"\n=== BASELINE MODEL PERFORMANCE ===")
    print(f"MAE:  {mae:.2f} cycles")
    print(f"RMSE: {rmse:.2f} cycles")
    
    # Compare with naive baseline (always predict mean)
    naive_pred = np.full_like(y_test, y_train.mean())
    naive_mae = np.mean(np.abs(y_test - naive_pred))
    naive_rmse = np.sqrt(np.mean((y_test - naive_pred)**2))
    
    print(f"\n=== COMPARISON WITH NAIVE BASELINE ===")
    print(f"Naive MAE:  {naive_mae:.2f} cycles")
    print(f"Naive RMSE: {naive_rmse:.2f} cycles")
    print(f"Improvement: {(naive_mae - mae)/naive_mae * 100:.1f}% MAE reduction")
    
except Exception as e:
    print(f"❌ Error in baseline model: {e}")

# Final Summary
print("\n" + "="*60)
print("STATISTICAL ANALYSIS SUMMARY")
print("="*60)
print(f"✅ Successfully analyzed {len(df):,} timestamps from {df['unit'].nunique()} engine units")
print(f"✅ Identified {len([f for f in correlation_scores.head(10).index if f not in T_var])} strong predictive features")
print(f"✅ Built baseline model with MAE: {mae:.2f} cycles")
print(f"✅ Key insight: {len([s for s in key_sensors if variation_df.loc[s, 'Between_Engine_Ratio'] < 0.3])} sensors show strong within-engine variation")
print("\nNext steps for deep learning:")
print("1. Use condition-normalized features")
print("2. Focus on sensors with high within-engine variation")
print("3. Consider temporal modeling with LSTM/Transformer")
print("4. This baseline gives us a target to beat!")
print("="*60)