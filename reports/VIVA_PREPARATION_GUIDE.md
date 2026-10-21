# CardioSense AI - Demo & Viva Voce Preparation Guide (15 Marks)

**Candidate Name:** Masoom Anis  
**Roll Number:** 63 | **Section:** A2 | **Batch:** B4  
**Subject:** Machine Learning Laboratory (24CS01TH0501 / 870439953001)  
**Scheduled Evaluation Date:** 22nd October 2026  

---

## 🎯 Executive Rubric Defense Summary (15/15 Marks)

| Rubric | Marks | What You Must Say / Demonstrate | Key Proof in Code & Report |
| :--- | :---: | :--- | :--- |
| **1: Data Cleaning & Splitting** | **3** | • Imputed missing values using **median** (not mean) to prevent distortion from skewed physiological variables.<br>• Used **Tukey's IQR method** ($[Q_1 - 1.5\text{IQR}, Q_3 + 1.5\text{IQR}]$) to cap extreme outliers (e.g., BP 260, Chol 710).<br>• Partitioned data using **Stratified 70-15-15 Train-Validation-Test** split.<br>• `StandardScaler` was **fitted strictly on the Train set only** to prevent **Data Leakage**. | `src/data_preprocessing.py`<br>`data/processed/train_scaled.csv`<br>Section 4 in Report |
| **2: SOTA Models Comparison & Analytics** | **4** | • Benchmarked **5 distinct models**: Logistic Regression, Random Forest, Gradient Boosting, SVM (RBF kernel), and Multi-Layer Perceptron (Neural Net).<br>• Evaluated **Accuracy, Precision, Recall/Sensitivity, Specificity, F1-Score, ROC-AUC, and PR-AUC**.<br>• Champion Model: **MLP Neural Network** (**96.10% Accuracy, 93.06% Recall, 95.71% F1, 0.9953 ROC-AUC**).<br>• Demonstrated **5-Fold Stratified Cross-Validation** (tight std dev ±1.5%). | `src/train_and_evaluate.py`<br>`models/model_benchmark_results.json`<br>Section 5 in Report |
| **3: UI Deployment & Accessibility** | **4** | • Built an interactive **Streamlit web application** (`app.py`).<br>• Cross-platform accessible on **Desktop, Tablet, and Mobile** over standard HTTP.<br>• Features **Single Patient Risk Scoring** (with risk gauge, probability %, and clinical advice) + **Batch CSV Upload** for population screening with downloadable triage report.<br>• Live EDA and Model Benchmarks tabs. | `app.py`<br>Run with `streamlit run app.py`<br>Section 7 in Report |
| **4: Code Quality, Repo & Report** | **4** | • Production-grade modular package layout (`src/`, `models/`, `reports/`, `data/`).<br>• Git initialized with `.gitignore`, `requirements.txt`, clean commit history.<br>• Comprehensive **10-page formal academic report** with 5 latest IEEE literature papers and references. | Git repo at `/home/endertrailer/ml`<br>`reports/ML_Mini_Project_Report_Masoom_Anis.pdf` |

---

## 🎤 Top 10 Expected Viva Voce Questions & Model Answers

### Q1: Why did you choose Cardiovascular Disease Prediction for your project?
> **Answer:** "Cardiovascular diseases are the leading cause of death worldwide according to WHO, responsible for nearly 18 million deaths annually. Early diagnosis using non-invasive physiological indicators (like resting blood pressure, ST depression, cholesterol, and chest pain classification) can prevent fatal myocardial infarctions. Machine learning allows us to detect subtle, non-linear feature interactions that traditional clinical scores like Framingham often overlook."

---

### Q2: Why is Recall (Sensitivity) more important than Accuracy in healthcare?
> **Answer:** "In a clinical diagnostic system, the costs of classification errors are highly asymmetric:
> - A **False Positive** means a healthy person is flagged as high risk. The consequence is merely ordering a confirmatory stress test or angiogram.
> - A **False Negative** means a patient with active coronary artery disease is misdiagnosed as healthy and sent home without treatment, which can lead to sudden cardiac death.
> Therefore, maximizing **Recall / Sensitivity** ($\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$) is paramount. Our champion Neural Network achieved **93.06% Recall**, successfully catching nearly all high-risk cardiac patients."

---

### Q3: What is Data Leakage and how did you prevent it?
> **Answer:** "Data leakage occurs when information from outside the training dataset (such as validation or test data) is inadvertently used to train or scale the model, leading to unrealistically optimistic performance that fails in real clinical deployment.
> We strictly prevented data leakage in three ways:
> 1. We performed **Stratified 70-15-15 Train-Validation-Test splitting** before any feature transformations.
> 2. The `StandardScaler` was **fitted only on the Training set** ($\mu_{\text{train}}, \sigma_{\text{train}}$) and then used to transform the validation and test sets without re-computing statistics.
> 3. We performed **5-Fold Stratified Cross-Validation** exclusively within the training partition."

---

### Q4: Why did you use Median Imputation instead of Mean for missing data?
> **Answer:** "Physiological continuous variables such as serum cholesterol and blood pressure are frequently right-skewed and susceptible to extreme outlier measurements. The arithmetic mean is heavily dragged by outliers, whereas the **median is a robust non-parametric location estimator**. Imputing with the median preserves the underlying population distribution without artificial variance inflation."

---

### Q5: How did you handle outliers? Did you drop them?
> **Answer:** "We did not drop outlier rows because discarding clinical records reduces sample size and introduces survivorship bias. Instead, we used **Tukey's Interquartile Range (IQR) Winsorization / Capping**:
> $$\text{Lower} = Q_1 - 1.5 \times \text{IQR}, \quad \text{Upper} = Q_3 + 1.5 \times \text{IQR}$$
> Extreme values (e.g. blood pressures above 175 mm Hg or cholesterol above 389 mg/dl) were capped to the threshold boundaries, stabilizing gradient descent during model optimization."

---

### Q6: Explain the 5 models you compared and why you picked these specific architectures.
> **Answer:** "We deliberately chose 5 models representing fundamentally different mathematical paradigms:
> 1. **Logistic Regression (Linear / Parametric Baseline):** Uses the log-odds sigmoid function with $L_2$ Ridge penalty. Provides interpretability and a baseline.
> 2. **Random Forest (Bagging Ensemble):** 120 de-correlated decision trees that reduce variance by bootstrap aggregating.
> 3. **Gradient Boosting (Boosting Ensemble):** 130 sequential trees that fit to residual pseudo-errors using gradient descent in function space.
> 4. **Support Vector Machine (Kernel Method):** Uses a non-linear Radial Basis Function (RBF) kernel with margin parameter $C=1.5$ to map clinical vectors into high-dimensional space.
> 5. **Multi-Layer Perceptron (Deep Feedforward Neural Network):** Architecture with two hidden layers (64 and 32 neurons) with non-linear ReLU activations and Adam optimizer. It captured high-order non-linear physiological interactions, yielding the highest F1-score (**95.71%**) and ROC-AUC (**0.9953**)."

---

### Q7: What are the most important clinical features identified by your models?
> **Answer:** "From the tree ensembles' Gini and Friedman importance scores:
> 1. **ST Depression (`oldpeak`):** Electrocardiographic ST-segment depression during peak treadmill stress testing.
> 2. **Major Vessels Colored (`ca`):** The number of coronary blood vessels visible under fluoroscopy.
> 3. **Chest Pain Type (`cp`):** Specifically asymptomatic or atypical angina.
> 4. **Maximum Heart Rate Achieved (`thalach`):** Decreased peak heart rate relative to age is a strong marker of chronotropic incompetence and coronary ischemia."

---

### Q8: What is the difference between ROC-AUC and PR-AUC? Why report both?
> **Answer:** "
> - **ROC-AUC (Receiver Operating Characteristic):** Plots True Positive Rate vs False Positive Rate. It measures how well the model discriminates between diseased and healthy patients across all possible classification thresholds. All our models achieved ROC-AUC $> 0.970$, with MLP reaching $0.9953$.
> - **PR-AUC (Precision-Recall Curve):** Plots Precision vs Recall. PR curves focus directly on the positive minority class (diseased patients) and are more informative when classes have imbalances. Reporting both demonstrates complete diagnostic rigor."

---

### Q9: How does your UI achieve cross-platform accessibility?
> **Answer:** "Our UI is developed in Streamlit using responsive HTML5/CSS3 container flexboxes. It runs on a lightweight web server serving standard HTTP on port 8501. A doctor or nurse can access the application from a desktop computer, hospital tablet (iPad/Android), or smartphone without installing any client-side software. It also supports both single-patient diagnostic consultation and multi-patient batch CSV screening."

---

### Q10: How would you deploy this into a real hospital setting?
> **Answer:** "In a real hospital setting:
> 1. We would containerize the application using **Docker** and deploy it as a microservice on Kubernetes.
> 2. Connect it to the hospital's **Electronic Health Record (EHR)** system using healthcare interoperability standards like **HL7** and **FHIR (Fast Healthcare Interoperability Resources)**.
> 3. Implement **Explainable AI (XAI)** frameworks like SHAP or LIME so cardiologists can see patient-specific feature attributions before signing off on treatment plans."

---

## 💻 Step-by-Step Demo Script (What to Show the Evaluator)

1. **Step 1: Open Terminal & Show Repository Structure**
   ```bash
   cd /home/endertrailer/ml
   ls -la
   git status
   ```
   *Explain:* "Sir/Ma'am, the project is structured modularly with separate pipelines for data preprocessing, training, inference, and UI deployment."

2. **Step 2: Show Training & Benchmarking**
   ```bash
   venv/bin/python src/train_and_evaluate.py
   ```
   *Explain:* "Here we train and benchmark all 5 models on the hold-out test set and compute 5-fold cross validation."

3. **Step 3: Launch Web Application**
   ```bash
   venv/bin/streamlit run app.py
   ```
   - Open browser at `http://localhost:8501`.
   - **Tab 1:** Show a sample patient assessment. Adjust ST depression slider to 2.5 and chest pain to 0 $\rightarrow$ show Risk Gauge jumps to High Risk (Red banner with clinical advice).
   - **Tab 2:** Show Batch Screening. Click "Download Template Clinical CSV", upload it, and show the instant batch prediction table with downloadable triage report.
   - **Tab 3 & 4:** Show the EDA charts and the SOTA model comparison table, ROC curves, and confusion matrix grid.
   - **Tab 5:** Show the Student Details badge (Masoom Anis, Roll No: 63, Section: A2, Batch: B4).

4. **Step 4: Present the 10-Page Project Report**
   - Open `/home/endertrailer/ml/reports/ML_Mini_Project_Report_Masoom_Anis.pdf` (or `.docx`).
   - Show the cover page, 5-paper literature review table, data cleaning section, model comparison tables, embedded high-resolution figures, and IEEE references.
