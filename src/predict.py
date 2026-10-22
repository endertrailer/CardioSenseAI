import os
import joblib
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

class HeartDiseasePredictor:
    def __init__(self, models_dir=MODELS_DIR):
        self.models_dir = models_dir
        self.model = joblib.load(os.path.join(models_dir, 'best_model.joblib'))
        self.scaler = joblib.load(os.path.join(models_dir, 'scaler.joblib'))
        self.feature_names = joblib.load(os.path.join(models_dir, 'feature_names.joblib'))
        self.all_models = joblib.load(os.path.join(models_dir, 'all_models.joblib'))

    def predict_single(self, patient_data: dict, model_name: str = None) -> dict:
        """
        patient_data: dictionary containing all 13 clinical features
        """
        df = pd.DataFrame([patient_data])[self.feature_names]
        df_scaled = pd.DataFrame(self.scaler.transform(df), columns=self.feature_names)

        clf = self.all_models.get(model_name, self.model) if model_name else self.model
        pred = int(clf.predict(df_scaled)[0])
        prob = float(clf.predict_proba(df_scaled)[0][1])

        if prob < 0.35:
            risk_level = "Low Risk (Healthy Profile)"
            color = "#10b981"
            recommendation = "Maintain regular cardiovascular exercise, balanced diet, and annual preventive checkups."
        elif prob < 0.70:
            risk_level = "Moderate Risk (Pre-Clinical Caution)"
            color = "#f59e0b"
            recommendation = "Recommend lipid panel monitoring, strict blood pressure control, and lifestyle modification."
        else:
            risk_level = "High Risk (Cardiovascular Anomaly Detected)"
            color = "#ef4444"
            recommendation = "URGENT: Schedule cardiology consultation, stress echocardiogram, and diagnostic coronary angiogram."

        return {
            'prediction': pred,
            'prediction_label': 'High Cardiac Risk' if pred == 1 else 'Low / Normal Risk',
            'probability': round(prob * 100, 2),
            'risk_level': risk_level,
            'risk_color': color,
            'clinical_recommendation': recommendation,
            'model_used': model_name if model_name else 'Champion Model (Logistic Regression)'
        }

    def predict_batch(self, input_df: pd.DataFrame, model_name: str = None) -> pd.DataFrame:
        """
        input_df: dataframe containing patient records
        """
        df_features = input_df[self.feature_names].copy()
        
        # Clinical Imputation (Practical 1): Handle missing values (NaN) with reference clinical medians
        default_medians = {
            'age': 54.0, 'sex': 1.0, 'chest_pain_type': 1.0, 'resting_bp': 131.0,
            'cholesterol': 247.0, 'fasting_bs': 0.0, 'rest_ecg': 1.0,
            'max_heart_rate': 167.0, 'exercise_angina': 0.0, 'st_depression': 0.7,
            'st_slope': 1.0, 'num_major_vessels': 0.0, 'thalassemia': 2.0
        }
        df_features = df_features.fillna(default_medians)
        
        df_scaled = pd.DataFrame(self.scaler.transform(df_features), columns=self.feature_names)

        clf = self.all_models.get(model_name, self.model) if model_name else self.model
        preds = clf.predict(df_scaled)
        probs = clf.predict_proba(df_scaled)[:, 1]

        result_df = input_df.copy()
        result_df['Predicted_Risk_Class'] = np.where(preds == 1, 'High Cardiac Risk', 'Normal / Low Risk')
        result_df['Risk_Probability_%'] = (probs * 100).round(2)
        result_df['Risk_Category'] = np.where(
            probs >= 0.70, 'High',
            np.where(probs >= 0.35, 'Moderate', 'Low')
        )
        return result_df

if __name__ == '__main__':
    predictor = HeartDiseasePredictor()
    sample_patient = {
        'age': 57,
        'sex': 1,
        'chest_pain_type': 2,
        'resting_bp': 140,
        'cholesterol': 260,
        'fasting_bs': 0,
        'rest_ecg': 1,
        'max_heart_rate': 155,
        'exercise_angina': 0,
        'st_depression': 1.2,
        'st_slope': 1,
        'num_major_vessels': 1,
        'thalassemia': 2
    }
    res = predictor.predict_single(sample_patient)
    print("Single Patient Diagnostic Output:")
    print(res)
