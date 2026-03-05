# 🤖 Modeling Basics — 05_modeling_basics (Python Data Analysis)

This directory implements **production-aware modeling fundamentals** for machine learning workflows.

Modeling is not “just fit a model”.
It is a disciplined pipeline that starts with:

- correct dataset splitting (to prevent leakage)
- reproducible evaluation setup
- train-only fitting rules for preprocessing
- auditable experiment structure

본 디렉토리는 ML 프로젝트의 **모델링 기본 구조(실무형)**를 다룹니다.  
단순히 모델을 돌리는 것이 아니라,

- 데이터 누수(leakage) 방지
- 재현 가능한 평가 구조
- train 기준 전처리 규칙
- 실험 설계의 일관성

을 코드로 증명하는 것을 목표로 합니다.

---

## 🎯 Learning Objectives

After completing this module, you will be able to:

- Explain why **train/test split** is mandatory for honest evaluation
- Prevent data leakage (fit on train, transform on test)
- Use `stratify` to preserve class balance for classification
- Handle time-series splitting correctly (no shuffle, past → future)
- Report split quality (size, distribution, sanity checks)
- Build reusable split utilities for scalable pipelines

본 모듈 완료 후 다음을 수행할 수 있습니다:

- Train/Test 분리가 왜 필수인지 설명
- 전처리 누수 방지(fit=train, transform=test) 구조 구현
- 분류 문제에서 stratify로 라벨 분포 유지
- 시계열 분할 원칙(Shuffle 금지, 과거→미래) 적용
- 분할 결과 리포팅(크기/분포/샘플) 자동화
- 파이프라인에 재사용 가능한 split 유틸 구성

---

## 📂 Files & Progress

### ✅ Day 62 — Train/Test Split (Leakage-Safe Split)
`01_train_test_split.py`

#### Core Coverage (English)

- Train/Test split as an evaluation boundary (no leakage)
- Reproducibility using `random_state`
- Class-balance preservation using `stratify`
- Time-series split basics (sort by time, no shuffle)
- Leakage-safe preprocessing pattern:
  - `fit` on train only
  - `transform` on both train/test
- Split reporting:
  - shapes
  - label distribution (classification)
  - sample rows

#### 코드 내 한국어 설명 기준 요약

- Train/Test split은 모델 평가의 “경계선”이며, 누수 방지의 시작점
- `random_state`로 결과 재현성 확보
- 분류 문제는 `stratify=y`로 train/test 라벨 비율 유지
- 시계열은 `shuffle=False` + 시간 정렬 기반 분할(과거→미래)
- 전처리(스케일링/인코딩)는 **train에서만 fit** → test에는 transform만 적용
- 분할 결과를 리포트로 출력하여 “검증 가능한 실험 구조”를 만든다

---

## 🧠 Why Day 62 Matters

Most ML projects fail silently because of:

- data leakage (test information used during training)
- improper split strategy (random split on time-series)
- unstable evaluation (no fixed seed)
- class imbalance drift (train/test label ratio mismatch)
- non-auditable experiments (no split report)

Day 62 establishes:

- honest evaluation boundaries
- reproducible experiment conditions
- leakage-safe preprocessing mindset
- an auditable modeling foundation

---

## ✅ Recommended Split Strategy

### 1) Tabular Classification (default)
- `train_test_split(..., stratify=y, shuffle=True)`
- Keep label ratio stable across train/test

### 2) Time Series (forecast / temporal causality)
- Sort by time
- Split last `test_size` portion as test
- `shuffle=False` (mandatory)

> 핵심 원칙: **미래 데이터로 과거 모델을 학습하면 안 된다.**

---

## 🔒 Leakage-Safe Rule (중요)

Preprocessing must follow:

```text
train: fit + transform
test : transform only
```

즉,
	•	scaler/encoder/imputer는 train에서 규칙을 학습(fit)
	•	test에는 동일 규칙을 적용(transform)
	•	test 정보를 보고 전처리 규칙을 만들면 평가 성능이 과대평가된다

---

## 🔄 Modeling Workflow (Conceptual)

'''
Raw Dataset
    ↓
Train/Test Split (Day 62)
    ↓
Train-only Fit Preprocessing (scaler/encoder)
    ↓
Model Training
    ↓
Test Evaluation (honest performance)
    ↓
Report & Iteration
'''

---

## ✅ Status

Day 62 Completed

This module now provides a clean baseline for:
	•	future model experiments
	•	pipeline construction (ColumnTransformer / Pipeline)
	•	proper validation strategy (K-Fold, TimeSeriesSplit)
	•	portfolio-grade reproducible ML workflows