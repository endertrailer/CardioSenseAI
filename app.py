import os
import streamlit as st
import pandas as pd
import numpy as np
import json
from src.predict import HeartDiseasePredictor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Page Configuration for Cross-Platform Desktop & Mobile Responsiveness
st.set_page_config(
    page_title="CardioSense AI - Clinical Decision Support System",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Medical Aesthetic Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0.1rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
    }
    .risk-high {
        background-color: #fee2e2;
        border-left: 5px solid #ef4444;
        padding: 15px;
        border-radius: 6px;
        color: #991b1b;
        font-weight: 600;
    }
    .risk-low {
        background-color: #d1fae5;
        border-left: 5px solid #10b981;
        padding: 15px;
        border-radius: 6px;
        color: #065f46;
        font-weight: 600;
    }
    .risk-moderate {
        background-color: #fef3c7;
        border-left: 5px solid #f59e0b;
        padding: 15px;
        border-radius: 6px;
        color: #92400e;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_predictor():
    return HeartDiseasePredictor()

@st.cache_data
def load_benchmark_results():
    path = os.path.join(BASE_DIR, 'models', 'model_benchmark_results.json')
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

predictor = load_predictor()
benchmarks = load_benchmark_results()

# Sidebar Navigation and System Info
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/heart-with-pulse.png", width=70)
    st.markdown("### CardioSense AI")
    st.caption("Clinical Decision Support & Cardiac Risk Prediction Engine")
    st.markdown("---")
    
    selected_model = st.selectbox(
        "⚡ Active Prediction Model:",
        options=list(predictor.all_models.keys()),
        index=0  # Default: Logistic Regression (Champion)
    )
    st.info(f"Active: **{selected_model}**")

# Header Section
st.markdown('<div class="main-title">❤️ Cardiovascular Disease Risk Intelligence System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">State-of-the-Art Machine Learning for Early Coronary Artery Disease Detection & Clinical Decision Support</div>', unsafe_allow_html=True)

# Main Navigation Tabs
tabs = st.tabs([
    "🩺 Patient Assessment",
    "📁 Batch Screening",
    "📊 Exploratory Data Analytics",
    "🏆 Model Benchmarks"
])

# -------------------------------------------------------------
# TAB 1: SINGLE PATIENT CLINICAL RISK ASSESSMENT
# -------------------------------------------------------------
with tabs[0]:
    st.subheader("Interactive Patient Clinical Diagnostics")
    st.markdown("Input the patient's physiological markers and cardiovascular test results below to evaluate coronary heart disease risk:")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("##### 👤 Demographic & Vital Signs")
        age = st.slider("Patient Age (Years)", min_value=25, max_value=85, value=54, step=1)
        sex_label = st.radio("Biological Sex", options=["Male", "Female"], horizontal=True)
        sex = 1 if sex_label == "Male" else 0
        trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=85, max_value=220, value=135, step=1,
                                   help="Systolic blood pressure measured upon hospital admission.")
        chol = st.number_input("Serum Cholesterol (mg/dl)", min_value=110, max_value=550, value=242, step=1,
                               help="Total serum cholesterol measured via fasting lipid profile.")

    with col2:
        st.markdown("##### 🫀 Symptoms & Stress Test")
        cp_map = {
            "0: Typical Angina": 0,
            "1: Atypical Angina": 1,
            "2: Non-Anginal Pain": 2,
            "3: Asymptomatic": 3
        }
        cp_sel = st.selectbox("Chest Pain Classification (cp)", options=list(cp_map.keys()), index=0)
        cp = cp_map[cp_sel]

        thalach = st.slider("Maximum Heart Rate Achieved (thalach)", min_value=70, max_value=210, value=148, step=1,
                            help="Peak heart rate recorded during Bruce protocol treadmill stress testing.")
        exang_label = st.radio("Exercise-Induced Angina (exang)", options=["No", "Yes"], horizontal=True)
        exang = 1 if exang_label == "Yes" else 0
        oldpeak = st.slider("ST Depression Induced by Exercise (oldpeak)", min_value=0.0, max_value=6.0, value=1.4, step=0.1,
                            help="Electrocardiographic ST depression relative to resting baseline.")

    with col3:
        st.markdown("##### 🔬 Diagnostic Tests & Fluoroscopy")
        fbs_label = st.radio("Fasting Blood Sugar > 120 mg/dl (fbs)", options=["No (Normal)", "Yes (> 120 mg/dl)"], horizontal=True)
        fbs = 1 if "Yes" in fbs_label else 0

        restecg_map = {
            "0: Normal": 0,
            "1: ST-T Wave Abnormality": 1,
            "2: Left Ventricular Hypertrophy": 2
        }
        restecg_sel = st.selectbox("Resting ECG Results (restecg)", options=list(restecg_map.keys()), index=0)
        restecg = restecg_map[restecg_sel]

        slope_map = {"0: Upsloping": 0, "1: Flat": 1, "2: Downsloping": 2}
        slope_sel = st.selectbox("Peak Exercise ST Segment Slope", options=list(slope_map.keys()), index=1)
        slope = slope_map[slope_sel]

        ca = st.selectbox("Major Vessels Colored by Fluoroscopy (0 - 3)", options=[0, 1, 2, 3], index=1,
                          help="Number of major coronary blood vessels visualized through radioactive dye angiography.")
        thal_map = {"1: Normal": 1, "2: Fixed Defect": 2, "3: Reversible Defect": 3}
        thal_sel = st.selectbox("Thalassemia Blood Disorder Scan", options=list(thal_map.keys()), index=1)
        thal = thal_map[thal_sel]

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Analyze Cardiac Risk Assessment", type="primary", use_container_width=True):
        patient_dict = {
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
            'thalassemia': thal
        }

        res = predictor.predict_single(patient_dict, model_name=selected_model)

        st.markdown("---")
        st.markdown("### 📋 Diagnostic Decision Report")

        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric("Predicted Diagnostic State", res['prediction_label'])
        with m_col2:
            st.metric("Cardiovascular Risk Score", f"{res['probability']}%")
        with m_col3:
            st.metric("Evaluator Model", selected_model)

        # Risk Banner
        if res['prediction'] == 1:
            st.markdown(f"""
            <div class="risk-high">
                ⚠️ <strong>HIGH RISK CARDIAC ALERT:</strong> Patient exhibits physiological indicators highly correlated with Coronary Artery Disease (CAD).<br>
                <strong>Clinical Action Plan:</strong> {res['clinical_recommendation']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="risk-low">
                ✅ <strong>NORMAL / LOW RISK PROFILE:</strong> Baseline cardiac parameters within healthy diagnostic thresholds.<br>
                <strong>Clinical Guidance:</strong> {res['clinical_recommendation']}
            </div>
            """, unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 2: BATCH SCREENING (CSV UPLOAD)
# -------------------------------------------------------------
with tabs[1]:
    st.subheader("Population-Level Batch Triage & Screening")
    st.markdown("Upload a patient cohort CSV file to perform rapid multi-patient inference and risk stratification:")

    # Provide sample download
    raw_csv = os.path.join(BASE_DIR, 'data', 'raw', 'heart_disease_clinical.csv')
    if os.path.exists(raw_csv):
        sample_df = pd.read_csv(raw_csv).head(10).drop(columns=['target'])
        st.download_button(
            label="📥 Download Template Clinical CSV (10 Patients)",
            data=sample_df.to_csv(index=False),
            file_name="cardiosense_patient_sample.csv",
            mime="text/csv"
        )

    uploaded_file = st.file_uploader("Upload Patient Cohort CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            input_df = pd.read_csv(uploaded_file)
            st.write(f"Loaded **{len(input_df)}** patient records. Executing inference using **{selected_model}**...")

            batch_res = predictor.predict_batch(input_df, model_name=selected_model)

            high_count = (batch_res['Predicted_Risk_Class'] == 'High Cardiac Risk').sum()
            low_count = len(batch_res) - high_count

            b_col1, b_col2, b_col3 = st.columns(3)
            b_col1.metric("Total Patients Screened", len(batch_res))
            b_col2.metric("High Risk Triage Cases", high_count, f"{high_count/len(batch_res)*100:.1f}%")
            b_col3.metric("Normal / Low Risk Cases", low_count, f"{low_count/len(batch_res)*100:.1f}%")

            st.dataframe(batch_res, use_container_width=True)

            csv_download = batch_res.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Export Complete Triage Diagnosis Report (CSV)",
                data=csv_download,
                file_name="cardiosense_triage_results.csv",
                mime="text/csv",
                type="primary"
            )
        except Exception as e:
            st.error(f"Error processing CSV: {str(e)}. Ensure all required 13 feature columns are present.")

# -------------------------------------------------------------
# TAB 3: EXPLORATORY DATA ANALYTICS (EDA)
# -------------------------------------------------------------
with tabs[2]:
    st.subheader("Exploratory Data Analysis & Feature Dynamics")
    st.markdown("Statistical analysis and clinical distributions derived from the 1,025 patient cohort:")

    eda_col1, eda_col2 = st.columns(2)
    with eda_col1:
        st.markdown("##### 📌 Diagnosis Class Balance")
        target_plot = os.path.join(BASE_DIR, 'static', 'plots', 'target_distribution.png')
        if os.path.exists(target_plot):
            st.image(target_plot, use_container_width=True)

    with eda_col2:
        st.markdown("##### 📌 Key Clinical Predictors (Feature Importance)")
        feat_plot = os.path.join(BASE_DIR, 'static', 'plots', 'feature_importance.png')
        if os.path.exists(feat_plot):
            st.image(feat_plot, use_container_width=True)

    st.markdown("##### 📌 Comprehensive Clinical Feature Correlation Heatmap")
    corr_plot = os.path.join(BASE_DIR, 'static', 'plots', 'correlation_matrix.png')
    if os.path.exists(corr_plot):
        st.image(corr_plot, use_container_width=True)

    st.markdown("##### 📌 Unsupervised Patient Phenotype Clustering via K-Means (Practical 6)")
    kmeans_plot = os.path.join(BASE_DIR, 'static', 'plots', 'kmeans_clustering.png')
    if os.path.exists(kmeans_plot):
        st.image(kmeans_plot, use_container_width=True)

# -------------------------------------------------------------
# TAB 4: SOTA MODEL BENCHMARKS & ANALYTICS
# -------------------------------------------------------------
with tabs[3]:
    st.subheader("State-of-the-Art Model Benchmark & Performance Analytics")
    st.markdown("Independent Test Set Evaluation ($N = 154$, 15% Hold-out Partition) and 5-Fold Stratified Cross-Validation:")

    if benchmarks:
        summary_rows = []
        for m_name, m_data in benchmarks.items():
            summary_rows.append({
                'Model Architecture': m_name,
                'Accuracy (%)': f"{m_data['Accuracy']}%",
                'Precision (%)': f"{m_data['Precision']}%",
                'Recall (Sensitivity) (%)': f"{m_data['Recall (Sensitivity)']}%",
                'Specificity (%)': f"{m_data['Specificity']}%",
                'F1-Score (%)': f"{m_data['F1-Score']}%",
                'ROC-AUC': m_data['ROC-AUC'],
                'PR-AUC': m_data['PR-AUC'],
                '5-Fold CV Accuracy': f"{m_data['CV_Accuracy_Mean']}% ± {m_data['CV_Accuracy_Std']}%"
            })
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True)

    g_col1, g_col2 = st.columns(2)
    with g_col1:
        st.markdown("##### 📈 Receiver Operating Characteristic (ROC) Curves")
        roc_plot = os.path.join(BASE_DIR, 'static', 'plots', 'roc_curves.png')
        if os.path.exists(roc_plot):
            st.image(roc_plot, use_container_width=True)

    with g_col2:
        st.markdown("##### 📉 Precision-Recall (PR) Curves")
        pr_plot = os.path.join(BASE_DIR, 'static', 'plots', 'pr_curves.png')
        if os.path.exists(pr_plot):
            st.image(pr_plot, use_container_width=True)

    st.markdown("##### 📊 Comparative Bar Chart across All Evaluation Metrics")
    bar_plot = os.path.join(BASE_DIR, 'static', 'plots', 'model_metrics_barchart.png')
    if os.path.exists(bar_plot):
        st.image(bar_plot, use_container_width=True)

    st.markdown("##### 🟦 Confusion Matrix Grid for All 5 Tested Classifiers")
    cm_plot = os.path.join(BASE_DIR, 'static', 'plots', 'confusion_matrices.png')
    if os.path.exists(cm_plot):
        st.image(cm_plot, use_container_width=True)

