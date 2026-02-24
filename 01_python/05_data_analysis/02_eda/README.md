# 📊 Exploratory Data Analysis (EDA) — 02_eda

This directory implements a **structured, reproducible, and production-aware EDA architecture**
for analytics and machine learning workflows.

EDA is not random plotting.  
It is a **diagnostic layer** that reduces modeling risk.

It answers:

- What does the dataset structurally look like?
- Is it statistically stable?
- Are there missing values?
- Are there heavy tails or extreme outliers?
- Do segments behave differently?
- Are features redundant (multicollinearity)?
- Is the dataset modeling-ready?

---

본 디렉토리는 분석 및 ML 프로젝트에서 필요한  
**체계적인 EDA(탐색적 데이터 분석) 아키텍처 구조**를 구현합니다.

EDA는 단순 시각화가 아니라,

- 데이터 구조 진단
- 통계적 특성 분석
- 분포 왜곡 탐지
- 이상치 영향 분석
- 세그먼트 비교
- 상관관계 및 다중공선성 점검
- 모델링 준비 상태 평가

를 수행하는 **모델링 전 안전 점검 체계**입니다.

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- Perform structured statistical profiling
- Diagnose missing values and structural data issues
- Detect outliers using IQR and percentile logic
- Evaluate skewness and tail behavior
- Identify transformation candidates (log / power / Yeo-Johnson)
- Compare numeric behavior across segments
- Analyze correlations and multicollinearity risks
- Implement reproducible visual EDA pipelines
- Build reusable EDA components for scalable systems

본 모듈 완료 후 다음을 수행할 수 있습니다:

- 요약 통계 기반 데이터 진단
- 결측치 및 품질 문제 체계적 파악
- IQR/분위수 기반 이상치 탐지
- 왜도·첨도 기반 분포 안정성 평가
- 변환 후보(log/power/Yeo-Johnson) 판단
- 세그먼트별 통계 비교
- 상관관계 및 다중공선성 리스크 진단
- 재현 가능한 시각 EDA 구조 설계
- 확장 가능한 EDA 모듈 구성

---

# 📂 Files & Progress

---

## ✅ Day 50 — Summary Statistics  
`01_summary_statistics.py`

### Core Implementation

- Dataset structure check (shape / dtypes / head)
- Missing value diagnostics
- Numeric descriptive statistics
- Skewness & kurtosis
- IQR-based outlier detection
- Categorical frequency summary (Top-K)
- Grouped segment statistics

**핵심 개념**

> “데이터의 구조와 품질을 수치적으로 진단하는 단계”

---

## ✅ Day 51 — Distribution Analysis  
`02_distribution_analysis.py`

### Core Implementation

- Quantile-based distribution summary (1%, 5%, 95%, 99%)
- Skewness-driven transformation hints
- IQR outlier rate calculation
- Histogram visualization
- Boxplot (spread + extreme detection)
- QQ plot (normality inspection)
- Top-skewed feature identification
- CSV-based summary export

**핵심 개념**

> “분포의 형태를 이해하고 변환 전략을 판단하는 단계”

---

## ✅ Day 52 — Correlation Analysis  
`03_correlation_analysis.py`

### Core Implementation

- Numeric-only safe correlation computation
- Pearson correlation matrix (linear)
- Spearman correlation matrix (rank-based)
- Target correlation Top-K extraction
- High-correlation pair detection (multicollinearity screening)
- Reusable utility functions for pipelines

**핵심 개념**

> “변수 간 관계 구조를 정량화하고, 다중공선성 리스크를 사전에 탐지하는 단계”

---

## ✅ Day 53 — Visual EDA  
`04_visual_eda.py`

### Core Implementation

- Missingness visualization
- Numeric distribution histograms
- Boxplots for outlier diagnostics
- Categorical frequency plots (Top-K)
- Correlation heatmap (Pearson/Spearman)
- Segment comparison boxplots
- Automated plot export (PNG)
- Console-based correlation summary

**핵심 개념**

> “수치 진단 결과를 시각적으로 검증하고, 모델링 위험을 직관적으로 파악하는 단계”

---

# 🧠 Integrated EDA Architecture (Day 50 → 53)

```text
Raw Dataset
    ↓
Structural Profiling (Day 50)
    ↓
Missing Value Diagnosis
    ↓
Numeric Summary Statistics
    ↓
Skewness / Kurtosis Analysis
    ↓
IQR Outlier Detection
    ↓
Distribution Visualization (Day 51)
    ↓
Transformation Candidate Identification
    ↓
Segment-Level Comparison
    ↓
Correlation Structure Mapping (Day 52)
    ↓
Multicollinearity Screening
    ↓
Visual Validation (Day 53)
    ↓
Modeling Readiness Assessment