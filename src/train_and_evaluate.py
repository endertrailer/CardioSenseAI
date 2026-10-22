import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    roc_curve, precision_recall_curve, classification_report
)
from sklearn.model_selection import StratifiedKFold, cross_val_score
import joblib

def train_and_benchmark(processed_dir, models_dir, plots_dir):
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(plots_dir, exist_ok=True)

    print("--- 1. LOADING PROCESSED DATASETS ---")
    train_df = pd.read_csv(os.path.join(processed_dir, 'train_scaled.csv'))
    val_df = pd.read_csv(os.path.join(processed_dir, 'val_scaled.csv'))
    test_df = pd.read_csv(os.path.join(processed_dir, 'test_scaled.csv'))

    X_train = train_df.drop(columns=['target'])
    y_train = train_df['target']

    X_val = val_df.drop(columns=['target'])
    y_val = val_df['target']

    X_test = test_df.drop(columns=['target'])
    y_test = test_df['target']

    feature_names = list(X_train.columns)

    print("--- 2. INITIALIZING CLASSROOM CURRICULUM CLASSIFIERS ---")
    # All models strictly from Lab Practicals (Practical 3: Linear/Logistic, Practical 4: k-NN, Practical 5: Decision Tree ID3/CART)
    models = {
        'Logistic Regression': LogisticRegression(C=1.0, max_iter=1000, random_state=42),
        'k-Nearest Neighbors (Uniform, k=5)': KNeighborsClassifier(n_neighbors=5, weights='uniform'),
        'k-Nearest Neighbors (Distance-Weighted, k=7)': KNeighborsClassifier(n_neighbors=7, weights='distance'),
        'Decision Tree (ID3 / Information Gain)': DecisionTreeClassifier(criterion='entropy', max_depth=6, min_samples_split=4, random_state=42),
        'Decision Tree (CART / Gini Impurity)': DecisionTreeClassifier(criterion='gini', max_depth=6, min_samples_split=4, random_state=42)
    }

    results = {}
    fitted_models = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    print("\n--- 3. MODEL TRAINING & CROSS-VALIDATION ---")
    for name, clf in models.items():
        print(f"\n>> Training {name}...")
        clf.fit(X_train, y_train)
        fitted_models[name] = clf

        # 5-fold CV on training data
        cv_scores = cross_val_score(clf, X_train, y_train, cv=cv, scoring='accuracy')
        cv_f1 = cross_val_score(clf, X_train, y_train, cv=cv, scoring='f1')

        # Evaluate on Test Set
        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)
        pr_auc = average_precision_score(y_test, y_prob)

        # Specificity: True Negative Rate
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0

        results[name] = {
            'Accuracy': round(acc * 100, 2),
            'Precision': round(prec * 100, 2),
            'Recall (Sensitivity)': round(rec * 100, 2),
            'Specificity': round(specificity * 100, 2),
            'F1-Score': round(f1 * 100, 2),
            'ROC-AUC': round(roc_auc, 4),
            'PR-AUC': round(pr_auc, 4),
            'CV_Accuracy_Mean': round(cv_scores.mean() * 100, 2),
            'CV_Accuracy_Std': round(cv_scores.std() * 100, 2),
            'CV_F1_Mean': round(cv_f1.mean() * 100, 2),
            'Confusion_Matrix': [[int(tn), int(fp)], [int(fn), int(tp)]]
        }

        print(f"   Accuracy: {results[name]['Accuracy']}% | Recall: {results[name]['Recall (Sensitivity)']}% | F1: {results[name]['F1-Score']}% | ROC-AUC: {results[name]['ROC-AUC']}")
        print(f"   5-Fold CV Mean: {results[name]['CV_Accuracy_Mean']}% (+/- {results[name]['CV_Accuracy_Std']}%)")

    # Determine Best Model based on F1-Score and ROC-AUC
    best_name = max(results.keys(), key=lambda k: (results[k]['F1-Score'], results[k]['ROC-AUC']))
    best_clf = fitted_models[best_name]
    print(f"\n>>> CHAMPION MODEL SELECTED: {best_name} (F1: {results[best_name]['F1-Score']}%, ROC-AUC: {results[best_name]['ROC-AUC']})")

    # Save Best Model and All Models
    joblib.dump(best_clf, os.path.join(models_dir, 'best_model.joblib'))
    joblib.dump(fitted_models, os.path.join(models_dir, 'all_models.joblib'))
    joblib.dump(results, os.path.join(models_dir, 'model_benchmark_results.joblib'))

    with open(os.path.join(models_dir, 'model_benchmark_results.json'), 'w') as f:
        json.dump(results, f, indent=4)

    print("\n--- 4. GENERATING PERFORMANCE VISUALIZATIONS ---")
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

    # Figure 1: ROC Curves Multi-Model
    plt.figure(figsize=(8, 6))
    colors = ['#2563eb', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899']
    for idx, (name, clf) in enumerate(fitted_models.items()):
        y_prob = clf.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        auc = results[name]['ROC-AUC']
        plt.plot(fpr, tpr, color=colors[idx], lw=2.2, label=f"{name} (AUC = {auc:.3f})")
    plt.plot([0, 1], [0, 1], 'k--', lw=1.5, label='Random Guessing (AUC = 0.500)')
    plt.xlabel('False Positive Rate (1 - Specificity)', fontsize=11)
    plt.ylabel('True Positive Rate (Sensitivity / Recall)', fontsize=11)
    plt.title('Receiver Operating Characteristic (ROC) Comparison', fontsize=13, fontweight='bold')
    plt.legend(loc='lower right', frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'roc_curves.png'), dpi=300)
    plt.close()

    # Figure 2: Precision-Recall Curves
    plt.figure(figsize=(8, 6))
    for idx, (name, clf) in enumerate(fitted_models.items()):
        y_prob = clf.predict_proba(X_test)[:, 1]
        prec, rec, _ = precision_recall_curve(y_test, y_prob)
        pr_auc = results[name]['PR-AUC']
        plt.plot(rec, prec, color=colors[idx], lw=2.2, label=f"{name} (PR-AUC = {pr_auc:.3f})")
    plt.xlabel('Recall (Sensitivity)', fontsize=11)
    plt.ylabel('Precision (Positive Predictive Value)', fontsize=11)
    plt.title('Precision-Recall Curves Across State-of-the-Art Models', fontsize=13, fontweight='bold')
    plt.legend(loc='lower left', frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'pr_curves.png'), dpi=300)
    plt.close()

    # Figure 3: Grouped Bar Chart of Core Metrics
    df_metrics = pd.DataFrame(results).T[['Accuracy', 'Precision', 'Recall (Sensitivity)', 'F1-Score']]
    ax = df_metrics.plot(kind='bar', figsize=(11, 6), colormap='viridis', edgecolor='black', width=0.75)
    plt.title('Model Performance Benchmark on Independent Clinical Test Set (N=154)', fontsize=13, fontweight='bold')
    plt.ylabel('Percentage (%)', fontsize=11)
    plt.ylim(70, 103)
    plt.xticks(rotation=15, ha='right', fontsize=10)
    plt.legend(loc='lower right', frameon=True)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'model_metrics_barchart.png'), dpi=300)
    plt.close()

    # Figure 4: Confusion Matrix Grid (5 models)
    fig, axes = plt.subplots(1, 5, figsize=(18, 3.8))
    for idx, (name, m_res) in enumerate(results.items()):
        cm = np.array(m_res['Confusion_Matrix'])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=axes[idx],
                    xticklabels=['Healthy', 'Risk'], yticklabels=['Healthy', 'Risk'])
        axes[idx].set_title(f"{name}\nAcc: {m_res['Accuracy']}%", fontsize=10, fontweight='bold')
        axes[idx].set_xlabel('Predicted')
        if idx == 0:
            axes[idx].set_ylabel('Actual')
        else:
            axes[idx].set_ylabel('')
    plt.suptitle('Confusion Matrix Comparison Across Models', fontsize=13, fontweight='bold', y=1.05)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'confusion_matrices.png'), dpi=300)
    plt.close()

    # Figure 5: Feature Importance (Decision Tree CART vs ID3 from Practical 5)
    cart_imp = fitted_models['Decision Tree (CART / Gini Impurity)'].feature_importances_
    id3_imp = fitted_models['Decision Tree (ID3 / Information Gain)'].feature_importances_
    imp_df = pd.DataFrame({
        'Feature': feature_names,
        'CART (Gini)': cart_imp,
        'ID3 (Entropy)': id3_imp
    }).sort_values(by='CART (Gini)', ascending=True)

    fig, ax = plt.subplots(figsize=(9, 6))
    y_pos = np.arange(len(imp_df))
    height = 0.35
    ax.barh(y_pos - height/2, imp_df['CART (Gini)'], height, label='Decision Tree (CART - Gini)', color='#2563eb')
    ax.barh(y_pos + height/2, imp_df['ID3 (Entropy)'], height, label='Decision Tree (ID3 - Entropy)', color='#10b981')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(imp_df['Feature'])
    ax.set_xlabel('Relative Feature Importance (Information Gain / Gini Index)')
    ax.set_title('Top Clinical Predictors via Decision Tree Analysis (Practical 5)', fontsize=13, fontweight='bold')
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'feature_importance.png'), dpi=300)
    plt.close()

    # Figure 6: Unsupervised K-Means Patient Risk Phenotype Clustering (Practical 6)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_train)
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(X_train['age'], X_train['max_heart_rate'], c=cluster_labels, cmap='viridis', alpha=0.7, s=40)
    plt.scatter(kmeans.cluster_centers_[:, feature_names.index('age')], 
                kmeans.cluster_centers_[:, feature_names.index('max_heart_rate')],
                c='red', marker='X', s=200, label='Cluster Centroids')
    plt.xlabel('Standardized Age', fontsize=11)
    plt.ylabel('Standardized Max Heart Rate', fontsize=11)
    plt.title('Unsupervised K-Means Patient Phenotype Clustering (Practical 6)', fontsize=13, fontweight='bold')
    plt.legend()
    plt.colorbar(scatter, label='K-Means Patient Cluster')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'kmeans_clustering.png'), dpi=300)
    plt.close()

    print("[SUCCESS] Training, evaluation, serialization, and high-res plotting completed!")
    return results

if __name__ == '__main__':
    proc_dir = '/home/endertrailer/ml/data/processed'
    mod_dir = '/home/endertrailer/ml/models'
    plt_dir = '/home/endertrailer/ml/static/plots'
    train_and_benchmark(proc_dir, mod_dir, plt_dir)
