# ML Basics (Python Libraries)

This directory covers **machine learning fundamentals** using Python libraries
(mainly scikit-learn).  
The goal is to build correct ML workflows that are:

- reproducible
- evaluation-driven
- aligned with real-world modeling practice

본 디렉토리는 scikit-learn을 중심으로
머신러닝의 핵심 기초를 **워크플로우 관점**에서 정리합니다.

단순히 모델을 돌리는 것이 아니라,
- 데이터 분리
- 평가 지표
- 검증
을 통해 “올바른 실험”을 수행하는 것을 목표로 합니다.

---

## 🎯 Objectives

- Split data properly to avoid leakage
- Evaluate models with correct metrics for the task
- Understand why evaluation matters more than model choice
- Build ML baselines that can extend to advanced topics (CV, pipelines, tuning)

---

## 📂 Structure & Progress

Each file represents one essential ML workflow step.
Files are completed incrementally with daily commits.

각 파일은 ML 워크플로우의 필수 단계를 하나씩 다루며,
일일 학습 단위로 순차적으로 완성됩니다.

---

## ✅ Completed

### ✅ Day 37 — Train/Test Split  
**`01_train_test_split.py`**

**Focus**
- Correct dataset split strategy to evaluate generalization performance

**Key Concepts**
- `train_test_split`
- random seed & reproducibility
- stratification (when classification is imbalanced)
- avoiding data leakage

**Why it matters**
- Without a proper split, “good performance” can be fake.

---

### ✅ Day 38 — Metrics Basics  
**`02_metrics_basics.py`**

**Focus**
- Core evaluation metrics for classification and regression

**Classification Metrics**
- Accuracy
- Precision / Recall
- F1-score
- Confusion Matrix

**Regression Metrics**
- MSE / RMSE
- MAE
- R² (coefficient of determination)

**Why it matters**
- Model evaluation is not optional.
- Choosing the wrong metric can lead to wrong decisions.

---

## 🧠 Why ML Basics Matter

Machine learning is an experimental discipline.  
The same model can look “great” or “bad” depending on:

- how the data was split
- which metric was used
- whether leakage occurred

These basics form the foundation for:
- cross validation
- pipelines
- hyperparameter tuning
- model comparison and deployment

머신러닝은 결국 **실험 설계(Experiment Design)** 입니다.  
기초가 흔들리면 이후 단계(CV, 튜닝, 파이프라인)가 모두 무너집니다.

---

## 📌 한국어 요약

- Day 37: Train/Test 분리로 일반화 성능 평가 기반 구축
- Day 38: 분류/회귀 평가 지표의 핵심 개념 정리

이 폴더는  
**ML을 “돌리는 것”이 아니라 “검증하는 것”** 에 초점을 둡니다.

---

## 🚧 Status

**In progress — ML Basics**

Next recommended topics:
- ROC-AUC & PR curve (classification threshold analysis)
- Cross Validation (KFold / StratifiedKFold)
- Model comparison template
- Pipelines (preprocessing + model)