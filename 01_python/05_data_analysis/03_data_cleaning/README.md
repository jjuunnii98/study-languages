# 🧹 Data Cleaning — 03_data_cleaning (Python Data Analysis)

This directory implements a **production-aware data cleaning architecture**
for analytics and machine learning pipelines.

Data cleaning is not a cosmetic step.
It is a structural control layer that ensures:

- correctness (no silent logical errors)
- statistical stability (distribution robustness)
- modeling safety (reduced distortion)
- reproducibility (rule-based transformations)

본 디렉토리는 분석/ML 파이프라인에서 필요한  
**실무형 데이터 클리닝 아키텍처**를 구현합니다.

데이터 클리닝은 단순 전처리가 아니라,

- 데이터 품질 진단
- 결측/이상값 처리 전략 수립
- 분포 안정성 확보
- 재현 가능한 처리 규칙 구축

을 목표로 하는 핵심 단계입니다.

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- Diagnose missingness magnitude and patterns
- Apply structured imputation strategies safely
- Detect outliers using robust statistical rules
- Choose between cap / drop / flag strategies rationally
- Preserve modeling integrity (avoid leakage & distortion)
- Build reusable cleaning utilities for scalable pipelines

본 모듈 완료 후 다음을 수행할 수 있습니다:

- 결측치 규모 및 패턴 체계적 진단
- 구조적 대체(imputation) 전략 설계
- IQR/MAD 기반 이상치 탐지
- cap / drop / flag 전략을 상황에 맞게 선택
- 모델 왜곡을 최소화하는 안전한 처리 구조 설계
- 파이프라인에 재사용 가능한 클리닝 유틸 구현

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
- Numeric imputation:
  - mean
  - median
- Categorical imputation:
  - mode
  - constant (e.g., `"Unknown"`)
- Group-based imputation:
  - segment median
  - segment mode
- Time-aware imputation:
  - forward fill / backward fill
  - linear interpolation

#### 3️⃣ Modeling-Safe Features
- Missing flag feature generation (`__is_missing`)
- Before/After comparison report
- Leakage-aware mindset (rule separation)

---

### 🧠 Why Day 54 Matters

Most modeling instability originates from:

- Hidden missing clusters
- Segment-dependent missing bias
- Improper global imputation
- Leakage during train/test split

Day 54 establishes:

- Structured diagnostics
- Policy-based imputation
- Reproducible missing handling

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
- Drop rows → only when justified
- Flag only → preserve signal for modeling

#### 3️⃣ Reporting & Governance
- Column-level outlier count & rate
- Applied thresholds logging
- Row-drop impact tracking
- Reproducible policy object (`OutlierPolicy`)

---

### 🧠 Why Day 55 Matters

Outliers can:

- Distort mean & variance
- Break linear models
- Inflate loss functions
- Create unstable gradient behavior

Blind removal is dangerous.

Day 55 enforces:

- Explicit detection rules
- Controlled impact reduction
- Documented transformation policies

---

# 🧠 Integrated Cleaning Flow (Day 54 → 55)

```text
Raw Dataset
    ↓
Schema & dtype validation
    ↓
Missing Profiling (count / pattern)
    ↓
Missing Handling (drop / impute / flag)
    ↓
Outlier Detection (IQR / MAD)
    ↓
Outlier Action (cap / drop / flag)
    ↓
Before–After Validation Report
    ↓
Clean Dataset for EDA / Modeling