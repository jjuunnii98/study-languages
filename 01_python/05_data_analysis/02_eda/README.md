# 📊 Exploratory Data Analysis (EDA) — 02_eda

This directory implements a **structured and production-aware EDA workflow**
for analytics and machine learning projects.

EDA is not random plotting.

It is a systematic diagnostic layer that answers:

- What does the dataset structurally look like?
- Is it statistically stable?
- Are there missing values?
- Are there heavy tails or extreme outliers?
- Do segments behave differently?
- Is the dataset modeling-ready?

본 디렉토리는 분석 및 ML 프로젝트에서 필요한  
**체계적인 EDA 아키텍처 구조**를 구현합니다.

EDA는 단순 시각화가 아니라,

- 데이터 구조 진단
- 통계적 특성 이해
- 분포 왜곡 탐지
- 이상치 영향 분석
- 세그먼트 비교
- 모델링 준비 상태 평가

를 수행하는 핵심 단계입니다.

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- Perform structured statistical profiling
- Diagnose missing values and structural data issues
- Detect outliers using IQR and percentile logic
- Evaluate skewness and tail behavior
- Identify transformation candidates (log / power / Yeo-Johnson)
- Compare numeric behavior across segments
- Build reusable EDA components for scalable pipelines

본 모듈 완료 후 다음을 수행할 수 있습니다:

- 요약 통계 기반 데이터 진단
- 결측치 및 품질 문제 체계적 파악
- IQR 및 분위수 기반 이상치 탐지
- 왜도 기반 변환 후보 판단
- 세그먼트별 통계 비교
- 재사용 가능한 EDA 설계 구조 구현

---

# 📂 Files & Progress

---

## ✅ Day 50 — Summary Statistics  
`01_summary_statistics.py`

### Core Implementation

Structured statistical profiling including:

- Basic dataset structure check (shape / dtypes / head)
- Missing value diagnostics
- Numeric descriptive statistics
- Skewness & kurtosis calculation
- IQR-based outlier detection
- Categorical frequency summary (Top-K)
- Grouped statistics (segment-level comparison)

Day 50의 핵심은:

> “데이터의 기본 구조와 품질을 통계적으로 진단하는 단계”

---

## ✅ Day 51 — Distribution Analysis  
`02_distribution_analysis.py`

### Core Implementation

Advanced distribution diagnostics including:

- Quantile-based distribution summary (1%, 5%, 95%, 99%)
- Skewness-driven transformation hints
- IQR outlier rate calculation
- Histogram visualization
- Boxplot for spread and extreme values
- QQ plot for normality inspection
- Top-skewed feature visualization
- CSV-based summary export

Day 51의 핵심은:

> “분포의 형태를 이해하고 변환 전략을 판단하는 단계”

---

# 🧠 Integrated EDA Flow (Day 50 → 51)

Raw Dataset
    ↓
Structural Profiling
    ↓
Missing Value Diagnosis
    ↓
Numeric Summary Statistics
    ↓
Skewness / Kurtosis Analysis
    ↓
IQR Outlier Detection
    ↓
Distribution Visualization
    ↓
Transformation Candidate Identification
    ↓
Segment-Level Comparison
    ↓
Modeling Readiness Assessment

이 흐름은 단순 탐색이 아니라  
**모델링 이전의 안전 점검 체계**입니다.

---

# 🔍 Why Day 50–51 Matter

Most modeling instability originates from:

- Hidden missing values
- Heavy-tailed distributions
- High skewness
- Extreme outliers
- Segment imbalance
- Incorrect numeric types

Day 50–51 establish:

- Statistical awareness
- Distribution-level insight
- Transformation decision support
- Modeling safety diagnostics
- Reproducible EDA workflow

---

# ⚙️ Practical Capabilities Implemented

## 1️⃣ Missing Value Diagnostics
- Count
- Percentage
- Priority ranking

## 2️⃣ Numeric Distribution Summary
- Mean / Median / Std
- Extended percentiles
- Skewness
- Kurtosis

## 3️⃣ IQR-based Outlier Detection
- Outlier count
- Outlier rate
- Robust extreme-value check

## 4️⃣ Transformation Hinting
- Right-skew detection → log1p / sqrt suggestion
- Left-skew detection → power transform suggestion
- Approximate symmetry detection

## 5️⃣ Distribution Visualization
- Histogram
- Boxplot
- QQ plot (if scipy available)

## 6️⃣ Segment-Level Comparison
- Grouped mean / median / spread
- Cross-segment behavior inspection

---

# 🚀 Current Status

**Day 50–51 Completed**

This module establishes the statistical and distributional foundation for:

- Feature engineering
- Log transformation
- Robust scaling
- Outlier handling
- Modeling pipeline preparation

---

# 🔜 Next Planned Extensions

- Correlation & multicollinearity analysis
- Distribution transformation benchmarking
- Automated EDA report generator
- Feature stability diagnostics
- Data drift comparison module