# Statistics (Python Libraries)

This directory covers **core statistics concepts and practical implementations**
for data analysis, machine learning, and research workflows.

It focuses on building statistical intuition and writing reproducible code for:
- descriptive summaries
- probability and distributions
- hypothesis testing
- confidence intervals and effect sizes
- (optional) simulation-based validation

본 디렉토리는 데이터 분석·머신러닝·연구에 필요한
통계 개념을 **코드로 재현 가능한 형태**로 정리합니다.

단순 공식 암기보다,
**정의 → 계산 → 해석 → 재현(검증)** 흐름을 중심으로 구성합니다.

---

## 🎯 Objectives

- Summarize data using robust descriptive statistics
- Understand distributions and uncertainty through simulation
- Apply hypothesis tests with correct assumptions and interpretation
- Report statistical results with effect sizes and confidence intervals
- Build foundations for research-grade analysis (reproducibility)

---

## 📂 Structure & Progress

Each file represents a focused topic and can be studied independently.
Files are completed incrementally with daily commits.

각 파일은 하나의 통계 주제를 집중적으로 다루며,
일일 학습 단위로 순차적으로 완성됩니다.

### ✅ Completed

- `01_descriptive_stats.py`  *(Day 34)*  
  Descriptive statistics & robust summaries  
  기술 통계 및 강건 요약(평균/중앙값/최빈값, 분산/표준편차, IQR, 절사평균, MAD)

  **Key Concepts**
  - Central tendency (mean/median/mode)
  - Dispersion (variance/std/range)
  - Robust stats (IQR, trimmed mean, MAD)
  - Clean summary report + IQR outlier rule example

---

### ⏳ Planned (Roadmap)

- `02_probability_distributions.py`  
  Common distributions (normal/binomial/poisson) + simulation  
  주요 확률분포(정규/이항/포아송) + 시뮬레이션 기반 직관

- `03_sampling_clt.py`  
  Sampling and Central Limit Theorem  
  표본추출과 중심극한정리(CLT)

- `04_confidence_intervals.py`  
  Confidence intervals and uncertainty reporting  
  신뢰구간과 불확실성 리포팅

- `05_hypothesis_testing_basics.py`  
  t-test / chi-square / assumptions / interpretation  
  가설검정 기초(가정, p-value 해석, 검정 선택)

- `06_effect_size_power.py`  
  Effect size and statistical power (practical significance)  
  효과크기와 검정력(실질적 유의성)

- `07_bootstrap_permutation.py`  
  Bootstrap & permutation tests (simulation-first)  
  부트스트랩/퍼뮤테이션 검정(시뮬레이션 기반)

---

## 🧠 Why Statistics Matters

Statistics is the language of uncertainty.
In real-world ML and analytics, you must:
- quantify variability
- validate results
- avoid misleading conclusions
- communicate confidence and limitations

통계는 “불확실성 하에서의 의사결정 언어”입니다.
머신러닝과 데이터 분석에서 통계를 이해하면,
결과를 더 신뢰 가능하게 만들고, 더 설득력 있게 설명할 수 있습니다.

---

## 📌 한국어 요약

- Day 34: 기술 통계 + 강건 통계 지표로 데이터 요약 체계화
- 이후: 확률분포 → 표본/CLT → 신뢰구간 → 가설검정 → 효과크기/검정력 → 시뮬레이션 기반 검정

이 모듈은  
**연구/실무에서 “통계적으로 올바른 분석”을 수행하기 위한 기반**입니다.

---

## 🚧 Status

**In progress — Statistics (Day 34 started)**  
This module is developed incrementally with daily commits.

본 단계는 진행 중이며,
통계 핵심 주제를 코드 기반으로 확장해 나갑니다.