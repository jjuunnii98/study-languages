# 🤖 Modeling Basics — 05_modeling_basics (Python Data Analysis)

This directory implements **production-aware modeling fundamentals** for machine learning workflows.

Modeling is not “just fit a model”.  
It is a disciplined pipeline that starts with:

- correct dataset splitting (to prevent leakage)
- reproducible evaluation setup
- baseline performance benchmarks
- auditable experiment structure

본 디렉토리는 ML 프로젝트의 **모델링 기본 구조(실무형)**를 다룹니다.  
단순히 모델을 실행하는 것이 아니라,

- 데이터 누수(leakage) 방지
- 재현 가능한 평가 구조
- baseline 성능 기준 설정
- 실험 구조의 일관성

을 코드로 증명하는 것을 목표로 합니다.

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- Explain why **train/test split** is mandatory for honest evaluation
- Prevent data leakage (fit on train, transform on test)
- Establish **baseline models** before advanced ML
- Use `stratify` to preserve class balance for classification
- Handle time-series splitting correctly (no shuffle, past → future)
- Build reproducible modeling experiments

본 모듈 완료 후 다음을 수행할 수 있습니다:

- Train/Test 분리가 왜 필수인지 설명
- 전처리 누수 방지(fit=train, transform=test) 구조 구현
- 고급 모델 이전에 **baseline 모델 성능 기준 설정**
- 분류 문제에서 stratify로 라벨 분포 유지
- 시계열 분할 원칙(Shuffle 금지, 과거→미래) 적용
- 재현 가능한 모델링 실험 구조 구축

---

# 📂 Files & Progress

---

# ✅ Day 62 — Train/Test Split (Leakage-Safe Split)

`01_train_test_split.py`

## Core Coverage (English)

- Train/Test split as an evaluation boundary (no leakage)
- Reproducibility using `random_state`
- Class-balance preservation using `stratify`
- Time-series split basics (sort by time, no shuffle)
- Leakage-safe preprocessing pattern
- Split reporting for experiment auditing

## 코드 내 한국어 설명 요약

- Train/Test split은 모델 평가의 **경계선(boundary)**
- `random_state`로 결과 재현성 확보
- 분류 문제는 `stratify=y`로 train/test 라벨 비율 유지
- 시계열은 `shuffle=False` + 시간 기반 분할
- 전처리는 **train에서만 fit**
- split 결과를 리포트하여 **검증 가능한 실험 구조**를 만든다

---

# ✅ Day 63 — Baseline Models (Minimum Performance Benchmark)

`02_baseline_models.py`

## Core Coverage (English)

Before training complex models, establish a **baseline performance level**.

Baseline models provide a **minimum benchmark** that any real model must beat.

This module introduces:

- Dummy classifiers for classification tasks
- Dummy regressors for regression tasks
- Baseline evaluation metrics

Strategies implemented:

Classification:

- `most_frequent`
- `stratified`
- `uniform`

Regression:

- `mean`
- `median`

Evaluation metrics:

- classification → accuracy / f1 / roc_auc
- regression → MAE / RMSE / R²

## 코드 내 한국어 설명 요약

Baseline 모델은 **“최소 성능 기준선”**이다.

고급 모델(RandomForest, XGBoost 등)을 사용하기 전에 반드시 확인해야 한다.

이유:

- 모델이 baseline보다 못하면 **모델링 실패**
- 데이터 누수(leakage) 탐지 가능
- 불균형 데이터 문제 조기 발견
- 평가 구조 검증 가능

사용 전략

분류 문제

- `most_frequent` → 항상 가장 많은 클래스 예측
- `stratified` → 라벨 비율 기반 랜덤 예측
- `uniform` → 균등 랜덤 예측

회귀 문제

- `mean` → 평균값 예측
- `median` → 중앙값 예측

핵심 질문

> “내 모델이 baseline보다 얼마나 좋아졌는가?”

---

# 🧠 Why Day 62 & Day 63 Matter

Most ML projects fail silently because of:

- data leakage
- improper evaluation split
- unstable experiment setup
- lack of baseline comparison

These two modules establish the **foundation of trustworthy modeling**.

### Day 62 provides

- honest evaluation boundary
- leakage-safe preprocessing
- reproducible split logic

### Day 63 provides

- minimum performance benchmark
- sanity check for modeling pipeline
- baseline reference for future models

---

# 🔒 Leakage-Safe Rule (중요)

Preprocessing must follow:

train: fit + transform 
test: transform only

'''
즉

- scaler / encoder / imputer → train에서 규칙 학습
- test → 동일 규칙 적용

test 정보를 보고 규칙을 만들면 **성능이 과대평가된다.**
'''

---

# 🔄 Modeling Workflow (Conceptual)

'''
Raw Dataset
↓
Train/Test Split (Day 62)
↓
Baseline Model (Day 63)
↓
Preprocessing (train-fit only)
↓
Advanced Model Training
↓
Evaluation
↓
Experiment Report
'''

---

# 📊 Modeling Principle

A model is only meaningful if:

Model Performance > Baseline Performance

If not,

- feature engineering 문제
- data leakage
- wrong modeling strategy

가능성이 높다.

---

# 🚀 Next Modules (Planned)

This module prepares the ground for:

- model evaluation metrics
- cross validation
- sklearn pipelines
- hyperparameter tuning
- experiment tracking

---

# ✅ Status

Day 62 Completed  
Day 63 Completed

This module now provides a clean baseline for:

- reproducible ML experiments
- leakage-safe modeling workflows
- baseline benchmarking
- portfolio-grade machine learning structure