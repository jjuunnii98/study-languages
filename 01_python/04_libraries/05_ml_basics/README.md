# ML Basics (Python Libraries)

This directory covers **core machine learning workflow fundamentals**
using Python libraries (mainly scikit-learn).

The goal is not just to “train models,”  
but to design **correct, reproducible, and evaluation-driven experiments**.

본 디렉토리는 scikit-learn을 중심으로  
머신러닝의 핵심 기초를 **워크플로우 중심**으로 정리합니다.

모델을 단순히 돌리는 것이 아니라,

- 데이터 분리
- 평가 지표 선택
- 모델 학습
- 해석 가능성

을 체계적으로 이해하는 것을 목표로 합니다.

---

## 🎯 Objectives

- Split data properly to prevent leakage
- Choose correct evaluation metrics for each task
- Build interpretable baseline models
- Understand the importance of experiment design
- Prepare for advanced topics (CV, pipelines, tuning)

---

# 📂 Structure & Progress

Each file represents one essential ML workflow step.  
Files are completed incrementally with daily commits.

각 파일은 머신러닝 워크플로우의 핵심 단계를 다루며,  
일일 학습 단위로 확장됩니다.

---

## ✅ Completed

---

### ✅ Day 37 — Train/Test Split  
**`01_train_test_split.py`**

**Focus**
- Proper dataset splitting for generalization evaluation

**Key Concepts**
- `train_test_split`
- random seed & reproducibility
- stratified splitting
- avoiding data leakage

**Why it matters**
Without correct splitting, model performance is meaningless.

---

### ✅ Day 38 — Metrics Basics  
**`02_metrics_basics.py`**

**Focus**
- Core evaluation metrics for classification and regression

**Classification Metrics**
- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

**Regression Metrics**
- MSE / RMSE
- MAE
- R²

**Why it matters**
Choosing the wrong metric leads to wrong decisions.

---

### ✅ Day 39 — Linear Models  
**`03_linear_models.py`**

**Focus**
- Fundamental baseline models for regression and classification

**Models Covered**
- Linear Regression
- Logistic Regression
- Ridge (L2 Regularization)

**Key Concepts**
- coefficient / intercept interpretation
- regularization intuition
- linear decision boundaries

**Why it matters**
Linear models are interpretable, fast, and strong baselines.

---

### ✅ Day 40 — Tree Models  
**`04_tree_models.py`**

**Focus**
- Tree-based models for non-linear patterns and interactions

**Models Covered**
- Decision Tree (classification)
- Random Forest (ensemble)

**Key Concepts**
- overfitting control (`max_depth`, `min_samples_leaf`)
- ensemble intuition (variance reduction)
- feature importance (basic interpretation + caveats)

**Why it matters**
Tree models provide strong non-linear baselines and practical interpretability tools.

---

# 🧠 Why ML Basics Matter

Machine learning is an experimental discipline.

The same model can look “great” or “bad” depending on:

- how the data was split
- which metric was used
- whether leakage occurred
- whether the baseline was properly defined

이 단계는  
**ML을 ‘모델 선택’이 아니라 ‘실험 설계’로 이해하는 과정**입니다.

These fundamentals form the foundation for:

- Cross Validation
- Model comparison frameworks
- Pipelines
- Hyperparameter tuning
- Production ML systems

---

## 📌 한국어 요약

- Day 37: 올바른 Train/Test 분리
- Day 38: 분류·회귀 평가 지표 이해
- Day 39: 선형 모델 기반 베이스라인 구축
- Day 40: 트리/앙상블 기반 비선형 베이스라인 구축

이 폴더는  
**ML 실험의 기초 체력**을 만드는 단계입니다.

---

## 🚧 Status

**In progress — ML Basics**

Next recommended steps:

- ROC-AUC & Precision-Recall Curve (threshold analysis)
- Cross Validation (KFold / StratifiedKFold)
- Pipeline construction (preprocessing + model)
- Model comparison template
- Hyperparameter tuning (GridSearchCV / RandomizedSearchCV)