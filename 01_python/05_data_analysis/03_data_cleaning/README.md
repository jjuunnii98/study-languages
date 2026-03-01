# 🧹 Data Cleaning — 03_data_cleaning (Python Data Analysis)

This directory implements a **production-grade data cleaning architecture**
for analytics and machine learning pipelines.

Data cleaning is not a cosmetic preprocessing step.  
It is a **structural control layer** that guarantees:

- correctness (no silent logical errors)
- statistical stability (robust distributions)
- modeling safety (reduced distortion)
- schema integrity (consistent dtypes & formats)
- numerical stability (well-scaled features)
- reproducibility (rule-based deterministic transformations)

본 디렉토리는 분석/ML 파이프라인에서 필요한  
**실무형 데이터 클리닝 아키텍처**를 구현합니다.

데이터 클리닝은 단순 전처리가 아니라,

- 데이터 품질 진단
- dtype/스키마 정규화
- 결측/이상값 처리 전략 수립
- 분포 안정성 확보
- 스케일 정규화
- 재현 가능한 처리 규칙 구축

을 목표로 하는 핵심 단계입니다.

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- Diagnose missingness magnitude and structural patterns
- Normalize inconsistent data types safely
- Apply structured imputation strategies
- Detect outliers using robust statistical rules
- Choose between cap / drop / flag strategies rationally
- Normalize feature scales (standard / minmax / robust / power)
- Preserve modeling integrity (avoid leakage & distortion)
- Produce auditable cleaning reports

본 모듈 완료 후 다음을 수행할 수 있습니다:

- 결측치 규모 및 패턴 체계적 진단
- dtype 정규화(숫자/날짜/불리언/범주형)
- 구조적 대체(imputation) 전략 설계
- IQR/MAD 기반 이상치 탐지
- cap / drop / flag 전략을 상황에 맞게 선택
- feature scaling 전략 적용
- 모델 왜곡을 최소화하는 안전한 처리 구조 설계
- 리포트 기반 재현 가능한 데이터 정제 구현

---

# 📂 Files & Progress

---

## ✅ Day 54 — Missing Values Handling  
`01_missing_values.py`

### Core Capabilities

#### 1️⃣ Missing Profiling
- Column-level missing count & percentage
- Missing pattern detection
- High-missing feature prioritization

#### 2️⃣ Strategy Patterns
- Drop rows / Drop columns (threshold-based)
- Numeric imputation (mean / median)
- Categorical imputation (mode / constant)
- Group-based imputation (segment median / mode)
- Time-aware imputation (ffill / bfill / interpolation)

#### 3️⃣ Modeling-Safe Utilities
- Missing flag feature (`__is_missing`)
- Before–After comparison report
- Leakage-aware design (fit rules vs apply rules)

### 🧠 Why Day 54 Matters

Hidden missing clusters and improper global imputation
are major sources of model instability.

Day 54 establishes structured missing governance.

---

## ✅ Day 55 — Outlier Handling  
`02_outlier_handling.py`

### Core Capabilities

#### 1️⃣ Robust Detection
- IQR rule
- MAD-based robust z-score
- Percentile boundary detection

#### 2️⃣ Policy-Based Actions
- Cap (Winsorization) — recommended default
- Drop rows — only with justification
- Flag only — preserve signal

#### 3️⃣ Governance & Reporting
- Column-level outlier rate
- Threshold logging
- Row-drop impact tracking
- Reproducible `OutlierPolicy`

### 🧠 Why Day 55 Matters

Outliers distort:

- mean / variance
- regression coefficients
- gradient-based optimization
- model stability

Day 55 enforces explicit statistical discipline.

---

## ✅ Day 56 — Data Type Fixing  
`03_data_type_fixing.py`

### Core Capabilities

#### 1️⃣ Column Name Normalization
- lowercasing
- whitespace cleanup
- safe character filtering

#### 2️⃣ Numeric Parsing
- Currency parsing (₩, $, €, commas)
- Parenthesis negatives `(1,200)`
- Percent conversion `"12%" → 0.12`
- Safe coercion with failure-rate reporting

#### 3️⃣ Datetime Normalization
- Multi-format parsing
- UTC control
- dayfirst option
- Failure-rate monitoring

#### 4️⃣ Boolean Normalization
- Yes/No, Y/N, 1/0, true/false → BooleanDtype

#### 5️⃣ Category Normalization
- Lowercase/strip cleaning
- Rare-category consolidation
- category dtype conversion

#### 6️⃣ Transformation Report
- Before/After dtype comparison
- Parse failure tracking
- Column-level notes

### 🧠 Why Day 56 Matters

Inconsistent dtypes cause:

- Join failures
- Aggregation errors
- Incorrect missing detection
- Model crashes
- Silent logic bugs

Day 56 ensures schema stability before statistical cleaning.

---

## ✅ Day 57 — Feature Normalization  
`04_feature_normalization.py`

### Core Capabilities

#### 1️⃣ Scaling Methods
- Standard Scaling (Z-score)
- Min-Max Scaling
- Robust Scaling (median/IQR)
- Log transformation
- Yeo-Johnson Power transform

#### 2️⃣ Fit / Transform Separation
- Train-based statistics
- Safe test-set application
- Leakage prevention design

#### 3️⃣ Optional Clipping
- Extreme value bounding
- Stability control

#### 4️⃣ Normalization Report
- Mean/std before & after comparison
- Scaling diagnostics

### 🧠 Why Day 57 Matters

Unscaled features cause:

- Biased regression coefficients
- Broken KNN distance metrics
- Neural network gradient explosion
- Regularization imbalance

Day 57 stabilizes model input space.

---

# 🧠 Integrated Cleaning Flow (Day 54 → 57)

```text
Raw Dataset
    ↓
Column Name Normalization (Day 56)
    ↓
Dtype Normalization (numeric / datetime / bool / category)
    ↓
Missing Profiling (Day 54)
    ↓
Missing Handling (drop / impute / flag)
    ↓
Outlier Detection (Day 55)
    ↓
Outlier Action (cap / drop / flag)
    ↓
Feature Normalization (Day 57)
    ↓
Before–After Validation Report
    ↓
Clean & Model-Ready Dataset
```

---

# 🏗️ Architectural Philosophy

This module enforces:

- Policy-based transformations
- Deterministic rule execution
- Auditability
- Train/Test separation mindset
- Statistical robustness
- Production-ready preprocessing discipline

이 디렉토리는 단순 전처리 코드가 아니라  
**모델링 직전의 안정성 확보 레이어**입니다.