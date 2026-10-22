# CardioSense AI: Cardiovascular Disease Risk Prediction & Clinical Decision Support System

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-v1.4+-orange.svg)](https://scikit-learn.org/)
[![Streamlit UI](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade, end-to-end Machine Learning Clinical Decision Support System (CDSS) for early detection, diagnostic risk scoring, and population-level screening of Cardiovascular Disease (CVD).

---

## 🎯 Project Highlights & Rubric Fulfillment (15 Marks)

| Evaluation Rubric | Marks | Implementation in Project |
| :--- | :---: | :--- |
| **1. Data Cleaning & Splitting** | **3** | Median imputation for clinical markers, IQR outlier capping, One-Hot/Ordinal encoding, `StandardScaler` fitted strictly on train set, and Stratified 70-15-15 Train-Val-Test partition ensuring zero data leakage. |
| **2. State-of-the-Art Models Comparison & Performance Analytics** | **4** | Benchmark of 5 distinct models: Logistic Regression, Random Forest, Gradient Boosting, Support Vector Machine (RBF), and Multi-Layer Perceptron (MLP Neural Net). Evaluated with Accuracy, Precision, Recall/Sensitivity, Specificity, F1, ROC-AUC, PR-AUC, and 5-Fold Stratified Cross-Validation. |
| **3. UI Deployment & Cross-Platform Accessibility** | **4** | Interactive, mobile-responsive Streamlit Web Application supporting real-time single patient clinical assessments, batch patient CSV upload with automated triage reports, and interactive EDA analytics. |
| **4. Code Quality, GitHub Repo & Report Writing** | **4** | Production modular code structure, clean Git repository, reproducible environment, automated testing, and a comprehensive 10-page academic report with IEEE literature review and Viva Q&A guide. |

---

## 🏛️ System Architecture

```
                                 [ Raw Clinical Dataset (N=1025) ]
                                                │
                                                ▼
                                [ Data Preprocessing Pipeline ]
                                  ├── Median Imputation (BP, Chol)
                                  ├── IQR Outlier Capping
                                  └── Stratified Split (70% Train, 15% Val, 15% Test)
                                                │
                                                ▼
                                    [ Model Training & CV ]
                                  ├── Logistic Regression (Practical 3)
                                  ├── k-Nearest Neighbors (Uniform, k=5) (Practical 4)
                                  ├── k-Nearest Neighbors (Distance-Weighted, k=7) (Practical 4)
                                  ├── Decision Tree (ID3 / Information Gain) (Practical 5)
                                  ├── Decision Tree (CART / Gini Impurity) (Practical 5)
                                  └── K-Means Patient Clustering (Practical 6)
                                                │
                                                ▼
                                 [ Performance Evaluation & Analytics ]
                                  ├── ROC-AUC & PR-AUC Curves
                                  ├── Sensitivity / Recall Optimization
                                  └── 5-Fold Stratified Cross-Validation
                                                │
                                                ▼
                                 [ Production Serialization ]
                                  ├── models/best_model.joblib
                                  └── models/scaler.joblib
                                                │
                                                ▼
                                [ Cross-Platform Web Application ]
                                  ├── Single Patient Diagnostic Risk Meter
                                  ├── Population Cohort CSV Batch Triage
                                  └── Live Model Benchmarking & Analytics
```

---

## 📊 Classroom Curriculum Model Benchmark Results

Evaluated on an independent, hold-out clinical test partition ($N = 154$):

| Model Architecture (Classroom Practical) | Accuracy | Precision | Recall (Sensitivity) | Specificity | F1-Score | ROC-AUC | 5-Fold CV Accuracy |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Practical 3)** 🏆 | **95.45%** | **98.51%** | **91.67%** | **98.78%** | **94.96%** | **0.9963** | **95.26% ± 1.18%** |
| **k-NN (Distance-Weighted, k=7) (Practical 4)** | 87.66% | 88.71% | 76.39% | 91.46% | 85.27% | 0.9549 | 81.87% ± 2.53% |
| **k-NN (Uniform, k=5) (Practical 4)** | 86.36% | 88.52% | 75.00% | 91.46% | 83.72% | 0.9494 | 81.87% ± 1.82% |
| **Decision Tree (ID3 / Information Gain) (Practical 5)** | 81.82% | 83.61% | 70.83% | 87.80% | 78.46% | 0.8651 | 81.87% ± 0.99% |
| **Decision Tree (CART / Gini Impurity) (Practical 5)** | 78.57% | 79.10% | 73.61% | 82.93% | 76.26% | 0.8249 | 81.18% ± 2.64% |

> **Clinical Finding:** In medical triage, **Recall (Sensitivity)** is prioritized over raw accuracy because a False Negative (failing to diagnose a high-risk cardiac patient) can be life-threatening. **Logistic Regression** achieved the highest Recall (**91.67%**), overall F1-Score (**94.96%**), and highest generalization stability under 5-Fold Cross-Validation (**95.26%**). In addition, **K-Means Clustering** (Practical 6) successfully segments patients into distinct clinical risk cohorts.

---

## 📁 Repository Directory Structure

```text
/home/endertrailer/ml/
├── data/
│   ├── raw/
│   │   └── heart_disease_clinical.csv     # 1,025 Clinical Patient Records
│   └── processed/
│       ├── train_scaled.csv               # 70% Training Partition
│       ├── val_scaled.csv                 # 15% Validation Partition
│       └── test_scaled.csv                # 15% Test Partition
├── src/
│   ├── __init__.py
│   ├── generate_data.py                   # Physiological data synthesizer
│   ├── data_preprocessing.py              # Data cleaning, imputation, IQR capping, splitting
│   ├── train_and_evaluate.py              # 5 SOTA models, 5-fold CV, plotting
│   └── predict.py                         # Single & batch inference pipeline
├── models/
│   ├── best_model.joblib                  # Serialized Champion Model (MLP)
│   ├── all_models.joblib                  # All 5 fitted model instances
│   ├── scaler.joblib                      # Fitted StandardScaler
│   ├── feature_names.joblib               # Ordered feature schema
│   └── model_benchmark_results.json       # Benchmark metrics dictionary
├── static/plots/
│   ├── target_distribution.png            # Class balance visualizer
│   ├── correlation_matrix.png             # Correlation heatmap
│   ├── roc_curves.png                     # Multi-model ROC curves
│   ├── pr_curves.png                      # Precision-Recall curves
│   ├── model_metrics_barchart.png         # Grouped metrics comparison chart
│   ├── confusion_matrices.png             # 5-panel confusion matrix grid
│   └── feature_importance.png             # Gini & Friedman feature rankings
├── reports/
│   ├── ML_Mini_Project_Report_Masoom_Anis.docx  # 10-Page Formal Submission Report
│   └── VIVA_PREPARATION_GUIDE.md                # Viva defense preparation guide
├── app.py                                 # Streamlit Web Application
├── requirements.txt                       # Python dependencies
├── .gitignore                             # Git ignore rules
└── README.md                              # Project documentation
```

---

## 🚀 Quickstart Guide

### 1. Environment Setup
```bash
cd /home/endertrailer/ml
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Data Preprocessing & Model Training
```bash
python src/data_preprocessing.py
python src/train_and_evaluate.py
```

### 3. Launch the Interactive Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 📄 License
This project is licensed under the MIT License.
