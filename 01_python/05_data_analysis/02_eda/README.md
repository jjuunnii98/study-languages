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
**체계적인 EDA(탐색적 데이터 분석) 아키텍처**를 구현합니다.

EDA는 단순 시각화가 아니라,

- 데이터 구조 진단
- 통계적 특성 이해
- 분포 왜곡 탐지
- 이상치 영향 분석
- 세그먼트 비교
- 모델링 준비 상태 평가

를 수행하는 핵심 단계입니다.

---

## 🎯 Learning Objectives

After completing this module, you will be able to:

- Perform structured statistical profiling
- Diagnose missing values and structural data issues
- Detect outliers using IQR and percentile logic
- Evaluate skewness and tail behavior
- Identify transformation candidates (log / power / Yeo-Johnson)
- Compare numeric behavior across segments
- Analyze correlations and multicollinearity risks
- Build reusable EDA components for scalable pipelines

본 모듈 완료 후 다음을 수행할 수 있습니다:

- 요약 통계 기반 데이터 진단
- 결측치 및 품질 문제 체계적 파악
- IQR 및 분위수 기반 이상치 탐지
- 왜도/첨도 기반 분포 안정성 점검
- 변환 후보(log/power/Yeo-Johnson) 판단
- 세그먼트별 통계 비교
- 상관관계 및 다중공선성 리스크 진단
- 재사용 가능한 EDA 구성요소 설계/구현

---

## 📂 Files & Progress

### ✅ Day 50 — Summary Statistics  
`01_summary_statistics.py`

**Core Implementation (English)**

- Basic dataset structure check (shape / dtypes / head)
- Missing value diagnostics
- Numeric descriptive statistics
- Skewness & kurtosis calculation
- IQR-based outlier detection
- Categorical frequency summary (Top-K)
- Grouped statistics (segment-level comparison)

**Day 50 핵심 (한국어)**  
> “데이터의 기본 구조와 품질을 통계적으로 진단하는 단계”

---

### ✅ Day 51 — Distribution Analysis  
`02_distribution_analysis.py`

**Core Implementation (English)**

- Quantile-based distribution summary (1%, 5%, 95%, 99%)
- Skewness-driven transformation hints
- IQR outlier rate calculation
- Histogram visualization
- Boxplot for spread and extreme values
- QQ plot for normality inspection (if available)
- Top-skewed feature visualization
- CSV-based summary export

**Day 51 핵심 (한국어)**  
> “분포의 형태를 이해하고 변환 전략을 판단하는 단계”

---

### ✅ Day 52 — Correlation Analysis  
`03_correlation_analysis.py`

**Core Implementation (English)**

- Numeric-only selection and safe correlation computation
- Pearson correlation matrix (linear relationship focus)
- Spearman correlation matrix (rank-based, monotonic focus)
- Target correlation Top-K extraction (optional)
- High-correlation pair detection for multicollinearity screening
- Reusable utilities (functions) for pipeline integration

**Day 52 핵심 (한국어)**  
> “변수 간 관계 구조를 정량화하고, 다중공선성 리스크를 사전에 탐지하는 단계”

---

## 🧠 Integrated EDA Flow (Day 50 → 52)

```text
Raw Dataset
    ↓
Structural Profiling (Day 50)
    ↓
Missing Value Diagnosis (Day 50)
    ↓
Numeric Summary Statistics (Day 50)
    ↓
Skewness / Kurtosis Analysis (Day 50–51)
    ↓
IQR Outlier Detection (Day 50–51)
    ↓
Distribution Visualization (Day 51)
    ↓
Transformation Candidate Identification (Day 51)
    ↓
Segment-Level Comparison (Day 50–51)
    ↓
Correlation Structure Mapping (Day 52)
    ↓
Multicollinearity Screening (Day 52)
    ↓
Modeling Readiness Assessment