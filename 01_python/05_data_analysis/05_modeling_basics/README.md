# 🤖 Modeling Basics — 05_modeling_basics (Python Data Analysis)

This directory implements **production-aware modeling fundamentals**
for machine learning workflows.

Modeling is not “just fitting a model.”
It is a disciplined process that starts with:

- correct dataset splitting
- leakage-safe preprocessing
- reproducible evaluation design
- metric-aware model assessment
- stable validation strategy

본 디렉토리는 ML 프로젝트의 **모델링 기본 구조(실무형)**를 다룹니다.

단순히 모델을 학습시키는 것이 아니라,

- 데이터 분할의 정확성
- 데이터 누수(leakage) 방지
- 재현 가능한 평가 구조
- 올바른 성능 해석
- 안정적인 검증 전략

을 코드로 증명하는 것을 목표로 합니다.

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- Explain why train/test split is mandatory for honest evaluation
- Prevent preprocessing leakage using train-only fitting rules
- Evaluate classification models using multiple metrics
- Interpret confusion matrix and threshold trade-offs
- Use cross validation to estimate model stability
- Build reusable modeling utilities for scalable ML workflows

본 모듈 완료 후 다음을 수행할 수 있습니다:

- Train/Test split이 왜 필수인지 설명
- train 기준 전처리로 누수 방지 구조 구현
- 분류 모델을 다중 지표로 평가
- confusion matrix와 threshold trade-off 해석
- cross validation으로 성능 안정성 평가
- 재사용 가능한 모델링 유틸 구성

---

# 📂 Files & Progress

---

## ✅ Day 62 — Train/Test Split  
`01_train_test_split.py`

### Core Coverage

- Honest evaluation boundary via train/test split
- Reproducibility with `random_state`
- Class-balance preservation using `stratify`
- Time-series split basics (`shuffle=False`, past → future)
- Leakage-safe preprocessing pattern:
  - fit on train only
  - transform on train/test
- Split reporting:
  - shapes
  - label distribution
  - sample rows

### 핵심 개념

Train/Test split은 모델링의 첫 번째 방어선이다.

핵심 원칙:

- train과 test는 평가 경계선이다
- test 정보를 train 과정에서 사용하면 안 된다
- 시계열 데이터는 무작위 섞기 금지
- 전처리 규칙은 반드시 train 기준으로만 학습해야 한다

### Summary

```text
Raw Data
    ↓
Train/Test Split
    ↓
Fit preprocessing on Train only
    ↓
Transform Train/Test
    ↓
Model Training & Honest Evaluation
```

---

## ✅ Day 64 — Model Evaluation  
`03_model_evaluation.py`

### Core Coverage

- Classification model training (baseline)
- Accuracy, Precision, Recall, F1 Score
- ROC AUC
- Confusion Matrix
- Classification Report
- Threshold-based decision logic
- Metric interpretation guide

### 핵심 개념

Accuracy 하나만으로 모델을 평가하면 위험하다.

문제의 비용 구조에 따라 중요한 지표가 달라진다:

- Precision 중요 → False Positive 비용이 클 때
- Recall 중요 → False Negative 비용이 클 때
- F1 중요 → Precision / Recall 균형이 필요할 때
- ROC AUC 중요 → 확률 예측 전반의 품질을 보고 싶을 때

### Summary

```text
Predicted Labels / Probabilities
    ↓
Accuracy / Precision / Recall / F1
    ↓
Confusion Matrix
    ↓
ROC AUC
    ↓
Metric-based Interpretation
```

---

## ✅ Day 65 — Cross Validation  
`04_cross_validation.py`

### Core Coverage

- K-Fold / Stratified K-Fold validation
- Fold-wise performance tracking
- Mean / Std interpretation
- Leakage-safe preprocessing with `Pipeline`
- Train vs Test score comparison
- Hold-out split vs CV comparison

### 핵심 개념

단일 train/test split은 split 운에 따라 성능이 흔들릴 수 있다.

Cross Validation은:

- 평균 성능을 본다
- fold 간 변동성을 본다
- 모델의 안정성을 판단하게 해준다

특히 중요한 해석:

- `test_mean` ↑ → 평균 성능 좋음
- `test_std` ↓ → fold 간 안정적
- `train_mean >> test_mean` → 과적합 가능성

### Summary

```text
Dataset
    ↓
K folds
    ↓
Train on K-1 folds / Validate on 1 fold
    ↓
Repeat K times
    ↓
Mean performance + Std stability
```

---

# 🧠 Modeling Workflow (Integrated)

```text
Raw Dataset
    ↓
Train/Test Split (Day 62)
    ↓
Leakage-Safe Preprocessing
    ↓
Baseline Model Training
    ↓
Metric-Based Evaluation (Day 64)
    ↓
Cross Validation (Day 65)
    ↓
Reliable Modeling Decision
```

---

# ⚙️ Practical Modeling Principles

## 1️⃣ Split First, Preprocess Later
Always split before scaling, encoding, or imputing.

데이터를 먼저 나누고 그 다음 전처리해야 한다.  
전처리를 먼저 하면 test 정보가 train에 섞일 수 있다.

---

## 2️⃣ Fit on Train Only
Preprocessing statistics are learned information.

예:

- scaler의 mean/std
- imputer의 median/mode
- encoder의 category mapping

이런 값들은 반드시 train에서만 학습해야 한다.

---

## 3️⃣ Metrics Depend on Business Cost
There is no universally “best” metric.

예:

- 의료 진단 → Recall 우선
- 스팸 필터 → Precision 우선
- 불균형 분류 → F1 / ROC AUC 함께 확인

---

## 4️⃣ Stability Matters
A model with slightly lower mean but much lower variance
may be safer than a high-variance model.

평균 성능뿐 아니라 성능의 흔들림(std)도 함께 봐야 한다.

---

## 5️⃣ Pipelines Reduce Leakage Risk
Using `Pipeline` helps ensure
that preprocessing happens correctly inside each fold.

특히 Cross Validation에서는 Pipeline이 누수 방지의 핵심이다.

---

# 📊 Capability Summary

| Area | Implemented |
|------|------------|
| Train/Test split | ✅ |
| Stratified split | ✅ |
| Time-series split basics | ✅ |
| Leakage-safe scaling | ✅ |
| Classification metrics | ✅ |
| Confusion matrix | ✅ |
| ROC AUC | ✅ |
| Classification report | ✅ |
| Cross validation | ✅ |
| Fold-wise score reporting | ✅ |
| CV mean/std interpretation | ✅ |
| Pipeline-based preprocessing | ✅ |

---

# 🚀 Current Status

**Day 62, 64, 65 Completed**

This module now establishes a clean foundation for:

- honest model evaluation
- leakage-safe preprocessing
- reproducible experiment setup
- stable validation strategy
- portfolio-ready ML workflow design

---

# 🔜 Next Logical Expansion

Possible next topics:

- hyperparameter tuning
- feature importance / model interpretation
- calibration and threshold tuning
- imbalanced classification strategies
- regression evaluation
- end-to-end modeling pipeline

---

# 🏁 Summary

This module moves modeling beyond:

“train a model and print accuracy”

into:

- controlled data splitting
- leakage-safe preprocessing
- metric-aware evaluation
- stability-aware validation

It forms the foundation for **production-grade machine learning experimentation**.