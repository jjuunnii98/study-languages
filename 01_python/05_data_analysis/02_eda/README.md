# 📊 Exploratory Data Analysis (EDA) — 02_eda

This directory covers **structured exploratory data analysis (EDA) workflows**
for analytical and machine learning projects.

EDA is not random plotting.

It is a systematic process that answers:

- What does the data look like?
- Is it clean?
- Are there missing values?
- Are there extreme values (outliers)?
- Do segments behave differently?
- Is the dataset modeling-ready?

본 디렉토리는 분석/ML 프로젝트에서 필요한  
**체계적인 EDA(탐색적 데이터 분석) 구조**를 다룹니다.

EDA는 단순 시각화가 아니라,

- 데이터 품질 점검
- 분포 이해
- 이상치 탐지
- 세그먼트 비교
- 모델링 준비 상태 점검

을 수행하는 핵심 단계입니다.

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- Perform structured summary statistics analysis
- Diagnose missing values and data quality issues
- Detect potential outliers using IQR
- Compare numeric distributions across segments
- Build reusable EDA utilities for production pipelines

본 모듈 완료 후 다음을 수행할 수 있습니다:

- 요약 통계 기반 데이터 진단
- 결측치 및 품질 문제 파악
- IQR 기반 이상치 탐지
- 세그먼트별 수치 차이 분석
- 재사용 가능한 EDA 코드 구조 설계

---

# 📂 Files & Progress

---

## ✅ Day 50 — Summary Statistics  
`01_summary_statistics.py`

### What It Implements

Structured EDA workflow including:

- Basic profile (shape, dtypes, head)
- Missing value summary
- Numeric descriptive statistics
- Skewness & kurtosis
- IQR-based outlier detection
- Categorical frequency summary
- Grouped statistics (segment comparison)

---

# 🧠 EDA Structure (Conceptual Flow)

Raw Dataset
↓
Basic Structure Check
↓
Missing Value Analysis
↓
Numeric Distribution Summary
↓
Outlier Detection (IQR)
↓
Categorical Frequency Analysis
↓
Grouped / Segment Comparison
↓
Modeling Readiness 판단

이 흐름은 데이터 분석에서 가장 기본이면서도  
가장 중요한 구조입니다.

---

# 🔍 Why Day 50 Matters

Most modeling failures originate from:

- Hidden missing values
- Heavy-tailed distributions
- Outliers distorting means
- Imbalanced segments
- Incorrect data types

Day 50 establishes:

- Statistical awareness
- Data hygiene discipline
- Modeling safety checks
- Reproducible EDA patterns

---

# ⚙️ Practical Features Implemented

### 1️⃣ Missing Value Diagnostics
- Count
- Percentage
- Sorted importance

### 2️⃣ Numeric Distribution Checks
- Mean / Median / Std
- Custom percentiles (1%, 5%, 95%, 99%)
- Skewness
- Kurtosis

### 3️⃣ IQR-based Outlier Count
Quick detection of extreme observations.

### 4️⃣ Categorical Top-K Frequency
Segment cardinality and imbalance detection.

### 5️⃣ Grouped Statistics
Segment-level comparison for:

- Mean
- Median
- Spread

---

# 🚀 Status

**Day 50 Completed**

This module establishes the statistical foundation
for:

- Feature engineering
- Distribution transformation
- Outlier handling
- Model-ready dataset preparation

Next Steps (Planned):

- Distribution visualization
- Log transformation checks
- Correlation heatmaps
- Automated EDA reporting