import numpy as np
import pandas as pd
import os

np.random.seed(42)
n = 1025

# Generate realistic clinical physiological features:
# age: 29 to 77
age = np.random.randint(29, 78, size=n)

# sex: 1 = Male (approx 68%), 0 = Female (32%)
sex = np.random.binomial(1, 0.68, size=n)

# cp: Chest Pain type [0: Typical Angina, 1: Atypical Angina, 2: Non-anginal, 3: Asymptomatic]
cp = np.random.choice([0, 1, 2, 3], size=n, p=[0.48, 0.17, 0.28, 0.07])

# trestbps: Resting Blood Pressure (mm Hg on admission) - mean 131, std 17
trestbps = np.clip(np.random.normal(131.6, 17.5, size=n).round(), 94, 200).astype(int)

# chol: Serum Cholesterol in mg/dl - mean 246, std 51
chol = np.clip(np.random.normal(246.2, 51.8, size=n).round(), 126, 564).astype(int)

# fbs: Fasting Blood Sugar > 120 mg/dl (1 = True, 0 = False)
fbs = np.random.binomial(1, 0.15, size=n)

# restecg: Resting Electrocardiographic results [0: Normal, 1: ST-T wave abnormality, 2: LV hypertrophy]
restecg = np.random.choice([0, 1, 2], size=n, p=[0.48, 0.50, 0.02])

# thalach: Maximum Heart Rate Achieved - physiological relation with age
base_thalach = 220 - age + np.random.normal(0, 14, size=n)
thalach = np.clip(base_thalach.round(), 71, 202).astype(int)

# exang: Exercise Induced Angina (1 = Yes, 0 = No)
exang = np.random.binomial(1, 0.32, size=n)

# oldpeak: ST depression induced by exercise relative to rest (0.0 to 6.2)
oldpeak = np.clip(np.random.exponential(scale=1.05, size=n), 0.0, 6.2).round(1)

# slope: Slope of peak exercise ST segment [0: Upsloping, 1: Flat, 2: Downsloping]
slope = np.random.choice([0, 1, 2], size=n, p=[0.21, 0.47, 0.32])

# ca: Number of major vessels colored by fluoroscopy (0 to 3)
ca = np.random.choice([0, 1, 2, 3], size=n, p=[0.58, 0.22, 0.13, 0.07])

# thal: Thalassemia [1: Normal, 2: Fixed Defect, 3: Reversible Defect]
thal = np.random.choice([1, 2, 3], size=n, p=[0.06, 0.54, 0.40])

# Logistic risk function incorporating well-established clinical cardiac risk indices
logit = (
    -2.8
    + 0.035 * (age - 50)
    + 0.45 * sex
    + 0.75 * cp
    + 0.015 * (trestbps - 130)
    + 0.005 * (chol - 240)
    + 0.30 * fbs
    + 0.25 * restecg
    - 0.038 * (thalach - 150)
    + 0.95 * exang
    + 0.65 * oldpeak
    + 0.55 * (slope == 2)
    + 0.85 * ca
    + 0.70 * (thal == 3)
)

prob = 1 / (1 + np.exp(-logit))
target = (prob > 0.50).astype(int)

# Introduce a small number of realistic missing values (NaN) to rigorously demonstrate cleaning
df = pd.DataFrame({
    'age': age,
    'sex': sex,
    'chest_pain_type': cp,
    'resting_bp': trestbps,
    'cholesterol': chol,
    'fasting_bs': fbs,
    'rest_ecg': restecg,
    'max_heart_rate': thalach,
    'exercise_angina': exang,
    'st_depression': oldpeak,
    'st_slope': slope,
    'num_major_vessels': ca,
    'thalassemia': thal,
    'target': target
})

# Insert 1.5% random missing values in resting_bp and cholesterol for demonstration of cleaning
missing_idx_bp = np.random.choice(n, size=15, replace=False)
missing_idx_chol = np.random.choice(n, size=18, replace=False)
df.loc[missing_idx_bp, 'resting_bp'] = np.nan
df.loc[missing_idx_chol, 'cholesterol'] = np.nan

# Insert 3 extreme outlier measurements to demonstrate robust outlier capping (IQR clipping)
outlier_idx = np.random.choice(n, size=3, replace=False)
df.loc[outlier_idx[0], 'resting_bp'] = 260
df.loc[outlier_idx[1], 'cholesterol'] = 680
df.loc[outlier_idx[2], 'cholesterol'] = 710

out_path = '/home/endertrailer/ml/data/raw/heart_disease_clinical.csv'
df.to_csv(out_path, index=False)
print(f"Generated raw clinical dataset at {out_path} with {df.shape[0]} rows and {df.shape[1]} columns.")
print(f"Target distribution: {df['target'].value_counts().to_dict()}")
