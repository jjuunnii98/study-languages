# Statistics (Python Libraries)

This directory covers **core statistics concepts and practical implementations**
essential for data analysis, machine learning, and research workflows.

Rather than focusing on formulas alone, this module emphasizes a **code-first,
reproducible workflow**:

> definition → computation → interpretation → validation

본 디렉토리는 데이터 분석·머신러닝·연구에 필요한
통계 개념을 **실행 가능한 Python 코드**로 정리합니다.  
공식 암기가 아니라, **분석 흐름과 해석 능력**을 기르는 데 목적이 있습니다.

---

## 🎯 Objectives

- Summarize data using descriptive and robust statistics
- Understand randomness through distributions and sampling
- Apply hypothesis testing with correct assumptions
- Interpret p-values together with effect sizes
- Build statistically sound, reproducible analysis pipelines

---

## 📂 Structure & Progress

Each file represents one focused statistical topic.
Files are completed incrementally with daily commits.

각 파일은 하나의 통계 개념을 중심으로 구성되며,
일일 학습 단위로 단계적으로 완성됩니다.

---

### ✅ Day 34 — Descriptive Statistics  
**`01_descriptive_stats.py`**

Descriptive and robust summaries of numerical data.

**Key Concepts**
- Central tendency: mean, median, mode
- Dispersion: variance, standard deviation, range
- Robust statistics: IQR, trimmed mean, MAD
- Outlier detection using IQR rule

**Purpose**
- Understand data shape before any modeling
- Build intuition for variability and robustness

---

### ✅ Day 35 — Distributions & Sampling  
**`02_distributions_sampling.py`**

Probability distributions and sampling-based intuition.

**Key Concepts**
- Random variables and probability distributions
- Normal distribution and empirical behavior
- Sampling variability and simulation
- Law of Large Numbers (LLN)
- Connection to Central Limit Theorem (CLT)

**Purpose**
- Develop intuition about randomness and uncertainty
- Prepare foundations for inference and hypothesis testing

---

### ✅ Day 36 — Hypothesis Testing Basics  
**`03_hypothesis_testing_basics.py`**

Statistical hypothesis testing with interpretation and effect sizes.

**Covered Tests**
- One-sample mean test (normal approximation)
- Two-sample Welch t-test (unequal variance)
- Chi-square test of independence (2×2)
- Permutation test (distribution-free validation)

**Key Concepts**
- Null vs alternative hypotheses
- Test statistic and p-value interpretation
- Effect sizes:
  - Cohen’s d
  - Hedges’ g
  - Cramér’s V
- Statistical vs practical significance

**Purpose**
- Move beyond “p < 0.05”
- Interpret results in a research- and business-relevant way

---

## 🧠 Why Statistics Matters

Statistics is the language of uncertainty.

In real-world analytics and machine learning, you must:
- quantify variability
- test assumptions
- validate conclusions
- communicate confidence and limitations

Without statistical reasoning,
models can be misleading—even if technically correct.

통계는 단순한 도구가 아니라  
**불확실성 하에서 올바른 의사결정을 가능하게 하는 사고 체계**입니다.

---

## 📌 한국어 요약

- Day 34: 기술 통계와 강건 통계로 데이터 요약
- Day 35: 분포와 샘플링을 통한 확률 직관 형성
- Day 36: 가설검정 + 효과크기 + 해석 중심 접근

이 모듈은  
**대학원 연구, 데이터 사이언스, ML 실무**를 위한
통계적 사고의 기반을 제공합니다.

---

## 🚧 Status

**Completed (Day 34–36)**  

This module forms a complete introduction to
statistical reasoning for data analysis and research,
and serves as a foundation for:
- regression analysis
- experimental design
- causal inference
- advanced machine learning evaluation