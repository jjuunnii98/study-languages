# 🧹 Data Cleaning — 03_data_cleaning (Python Data Analysis)

This directory implements a **production-aware data cleaning architecture**
for analytics and machine learning pipelines.

Data cleaning is not a cosmetic step.
It is a structural control layer that ensures:

- correctness (no silent logical errors)
- statistical stability (distribution robustness)
- modeling safety (reduced distortion)
- schema integrity (consistent dtypes & formats)
- reproducibility (rule-based transformations)

본 디렉토리는 분석/ML 파이프라인에서 필요한  
**실무형 데이터 클리닝 아키텍처**를 구현합니다.

데이터 클리닝은 단순 전처리가 아니라,

- 데이터 품질 진단
- dtype/스키마 정규화
- 결측/이상값 처리 전략 수립
- 분포 안정성 확보
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
- Preserve modeling integrity (avoid leakage & distortion)
- Produce auditable cleaning reports

본 모듈 완료 후 다음을 수행할 수 있습니다:

- 결측치 규모 및 패턴 체계적 진단
- dtype 정규화(숫자/날짜/불리언/범주형)
- 구조적 대체(imputation) 전략 설계
- IQR/MAD 기반 이상치 탐지
- cap / drop / flag 전략을 상황에 맞게 선택
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
- Missing pattern detection (co-missing columns)
- Prioritization of high-missing features

#### 2️⃣ Strategy Patterns
- Drop rows / Drop columns (threshold-based)
- Numeric imputation (mean / median)
- Categorical imputation (mode / constant)
- Group-based imputation (segment median / mode)
- Time-aware imputation (ffill / bfill / interpolation)

#### 3️⃣ Modeling-Safe Features
- Missing flag feature generation (`__is_missing`)
- Before–After comparison report
- Leakage-aware mindset

---

### 🧠 Why Day 54 Matters

Most modeling instability originates from:

- Hidden missing clusters
- Segment-dependent missing bias
- Improper global imputation
- Leakage during train/test split

Day 54 establishes structured missing governance.

---

## ✅ Day 55 — Outlier Handling  
`02_outlier_handling.py`

### Core Capabilities

#### 1️⃣ Robust Detection Methods
- IQR rule (Q1 − k·IQR / Q3 + k·IQR)
- MAD-based robust z-score
- Percentile boundary detection

#### 2️⃣ Policy-Based Actions
- Cap (Winsorization) → recommended default
- Drop rows → only when statistically justified
- Flag only → preserve extreme-value signal

#### 3️⃣ Governance & Reporting
- Column-level outlier rate
- Threshold logging
- Row-drop impact monitoring
- Policy object (`OutlierPolicy`) for reproducibility

---

### 🧠 Why Day 55 Matters

Outliers can:

- Distort central tendency
- Break regression assumptions
- Inflate loss functions
- Create unstable gradients

Blind removal is dangerous.

Day 55 enforces explicit statistical discipline.

---

## ✅ Day 56 — Data Type Fixing  
`03_data_type_fixing.py`

### Core Capabilities

#### 1️⃣ Column Name Normalization
- lowercasing
- whitespace normalization
- safe character filtering

#### 2️⃣ Numeric Normalization
- Currency parsing (₩, $, €, commas)
- Parenthesis negative handling `(1,200)`
- Percent conversion `"12%" → 0.12`
- Safe coercion with failure-rate reporting

#### 3️⃣ Datetime Normalization
- Multi-format parsing
- UTC control
- dayfirst option
- Failure rate monitoring

#### 4️⃣ Boolean Normalization
- Yes/No, Y/N, 1/0, true/false → BooleanDtype

#### 5️⃣ Category Normalization
- Lowercase/strip cleaning
- Rare-category consolidation (min_freq threshold)
- category dtype conversion

#### 6️⃣ Transformation Report
- Before/After dtype comparison
- Parse failure rate tracking
- Column-level transformation notes

---

### 🧠 Why Day 56 Matters

Inconsistent dtypes cause:

- Join failures
- Aggregation errors
- Incorrect missing detection
- Model input crashes
- Silent logic bugs

Day 56 ensures schema stability before statistical cleaning begins.

---

# 🧠 Integrated Cleaning Flow (Day 54 → 56)

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
Before–After Validation Report
    ↓
Clean Dataset for EDA / Modeling