import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

def preprocess_pipeline(raw_csv_path, processed_dir, models_dir, plots_dir):
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(plots_dir, exist_ok=True)

    print("--- 1. LOADING RAW DATASET ---")
    df = pd.read_csv(raw_csv_path)
    print(f"Raw shape: {df.shape}")
    print("Initial missing values count:")
    print(df.isnull().sum()[df.isnull().sum() > 0])

    print("\n--- 2. MISSING VALUE IMPUTATION ---")
    # Median imputation for continuous variables with missing entries
    for col in ['resting_bp', 'cholesterol']:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"Imputed missing entries in '{col}' with median: {median_val}")

    print("\n--- 3. OUTLIER DETECTION & IQR CAPPING ---")
    # Numerical continuous columns where extreme physiological measurements could be anomalous
    continuous_cols = ['resting_bp', 'cholesterol', 'max_heart_rate', 'st_depression']
    for col in continuous_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        num_outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
        df[col] = np.clip(df[col], lower_bound, upper_bound)
        print(f"Column '{col}': {num_outliers} outliers capped to [{lower_bound:.1f}, {upper_bound:.1f}]")

    print("\n--- 4. EXPLORATORY DATA ANALYSIS (EDA) PLOTTING ---")
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    # Target distribution plot
    plt.figure(figsize=(6, 4))
    ax = sns.countplot(x='target', data=df, palette=['#10b981', '#ef4444'])
    plt.title('Target Variable Distribution (0: Healthy, 1: Cardiac Risk)', fontsize=12, fontweight='bold')
    plt.xlabel('Diagnosis Class')
    plt.ylabel('Patient Count')
    plt.xticks([0, 1], ['Healthy (0)', 'High Risk (1)'])
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height() - 40),
                    ha='center', va='center', color='white', fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'target_distribution.png'), dpi=300)
    plt.close()

    # Correlation Matrix Heatmap
    plt.figure(figsize=(11, 8))
    corr = df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm', vmin=-0.6, vmax=0.6,
                linewidths=0.5, cbar_kws={'shrink': 0.8})
    plt.title('Clinical Feature Correlation Heatmap', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'correlation_matrix.png'), dpi=300)
    plt.close()

    print("\n--- 5. STRATIFIED TRAIN / VALIDATION / TEST SPLITTING ---")
    X = df.drop(columns=['target'])
    y = df['target']
    feature_names = list(X.columns)

    # 70% Train, 30% Temp (which will be split 50/50 into 15% Val, 15% Test)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
    )

    print(f"Train set:      {X_train.shape[0]} samples ({X_train.shape[0]/len(df)*100:.1f}%) | Positives: {y_train.sum()} ({y_train.mean()*100:.1f}%)")
    print(f"Validation set: {X_val.shape[0]} samples ({X_val.shape[0]/len(df)*100:.1f}%) | Positives: {y_val.sum()} ({y_val.mean()*100:.1f}%)")
    print(f"Test set:       {X_test.shape[0]} samples ({X_test.shape[0]/len(df)*100:.1f}%) | Positives: {y_test.sum()} ({y_test.mean()*100:.1f}%)")

    print("\n--- 6. FEATURE STANDARDIZATION (FITTED ON TRAIN ONLY) ---")
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=feature_names, index=X_train.index)
    X_val_scaled = pd.DataFrame(scaler.transform(X_val), columns=feature_names, index=X_val.index)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=feature_names, index=X_test.index)

    # Save processed CSVs
    train_df = pd.concat([X_train_scaled, y_train], axis=1)
    val_df = pd.concat([X_val_scaled, y_val], axis=1)
    test_df = pd.concat([X_test_scaled, y_test], axis=1)

    train_df.to_csv(os.path.join(processed_dir, 'train_scaled.csv'), index=False)
    val_df.to_csv(os.path.join(processed_dir, 'val_scaled.csv'), index=False)
    test_df.to_csv(os.path.join(processed_dir, 'test_scaled.csv'), index=False)

    # Also save unscaled sets for interpretability in UI
    pd.concat([X_train, y_train], axis=1).to_csv(os.path.join(processed_dir, 'train_raw.csv'), index=False)
    pd.concat([X_test, y_test], axis=1).to_csv(os.path.join(processed_dir, 'test_raw.csv'), index=False)

    # Serialize scaler and feature names
    joblib.dump(scaler, os.path.join(models_dir, 'scaler.joblib'))
    joblib.dump(feature_names, os.path.join(models_dir, 'feature_names.joblib'))

    print("\n[SUCCESS] Preprocessing pipeline completed successfully. Data & Scaler saved.")
    return X_train_scaled, y_train, X_val_scaled, y_val, X_test_scaled, y_test, feature_names

if __name__ == '__main__':
    raw_path = '/home/endertrailer/ml/data/raw/heart_disease_clinical.csv'
    proc_dir = '/home/endertrailer/ml/data/processed'
    mod_dir = '/home/endertrailer/ml/models'
    plt_dir = '/home/endertrailer/ml/static/plots'
    preprocess_pipeline(raw_path, proc_dir, mod_dir, plt_dir)
