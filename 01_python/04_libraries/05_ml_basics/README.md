# Machine Learning Basics (Python)

This directory covers **fundamental machine learning workflow principles**
that must be understood *before* applying any model or algorithm.

Rather than starting with models, this module focuses on:
- correct data splitting
- experimental design
- evaluation integrity
- prevention of data leakage

본 디렉토리는 머신러닝 알고리즘 이전에 반드시 이해해야 하는  
**데이터 분리, 검증 설계, 재현성 확보**의 기초를 다룹니다.

좋은 모델 성능은 알고리즘보다  
**데이터를 어떻게 나누고 검증했는지**에 의해 결정됩니다.

---

## 🎯 Objectives

- Understand why data must be split into train/test sets
- Prevent common data leakage scenarios
- Handle class imbalance correctly using stratification
- Respect temporal order in time-series data
- Avoid group-level leakage (patient/user/session level)
- Build reproducible machine learning experiments

---

## 📂 Structure & Progress

Each file represents a core concept in ML experiment design.
Files are completed incrementally with daily commits.

각 파일은 머신러닝 실험 설계의 핵심 개념 하나를 다루며,  
일일 학습 단위로 점진적으로 완성됩니다.

---

### ✅ Day 37 — Train / Test Split  
**`01_train_test_split.py`**

Best practices for splitting data into training and testing sets.

**Covered Scenarios**
- Random split with shuffle and reproducibility
- Stratified split for classification imbalance
- Time series split (no shuffle)
- Group-aware split (avoid entity leakage)

**Key Concepts**
- Data leakage and why it invalidates evaluation
- `random_state` for reproducibility
- When *not* to shuffle data
- Why group-level separation matters in real-world datasets

**Purpose**
- Ensure fair and reliable model evaluation
- Build experiments that can be trusted and reproduced
- Lay the foundation for cross-validation and model comparison

---

## 🧠 Why ML Basics Matter

Many machine learning failures are not caused by poor models,
but by **incorrect experimental design**.

Common pitfalls include:
- training on future information
- leaking user or patient identity across splits
- evaluating on data seen during training
- misrepresenting class distributions

Understanding these basics ensures that:
- reported performance is meaningful
- results generalize to real-world data
- conclusions are scientifically defensible

머신러닝의 신뢰성은  
모델보다 **실험 설계의 정확성**에서 시작됩니다.

---

## 📌 한국어 요약

- Day 37: 다양한 데이터 특성에 맞는 train/test 분리 전략 정리
- 데이터 누수(leakage) 방지의 중요성 이해
- 분류, 시계열, 그룹 데이터에 대한 분리 기준 확립

이 모듈은  
**머신러닝 모델링 이전 단계에서 반드시 필요한 실험 설계 기초**를 제공합니다.

---

## 🚧 Status

**In progress — Machine Learning Basics (Day 37 started)**

Next recommended topics:
- Cross-validation (KFold, StratifiedKFold, GroupKFold, TimeSeriesSplit)
- Model evaluation metrics (accuracy vs ROC-AUC vs RMSE)
- Baseline models and sanity checks