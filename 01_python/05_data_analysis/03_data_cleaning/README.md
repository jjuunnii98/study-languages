# 🧹 Data Cleaning — 03_data_cleaning (Python Data Analysis)

This directory implements a **production-aware data cleaning workflow** for analytics and ML pipelines.

Data cleaning is not “fixing a few NaNs.”
It is a systematic process that ensures:

- correctness (no silent errors)
- consistency (stable types / formats)
- robustness (edge-case safe)
- reproducibility (same inputs → same outputs)

본 디렉토리는 분석/ML 파이프라인에서 필요한 **실무형 데이터 클리닝 구조**를 구현합니다.

데이터 클리닝은 “결측치 조금 채우기”가 아니라,

- 데이터 품질(Quality) 진단
- 결측/이상값 처리 전략 수립
- 타입/포맷 정규화
- 재현 가능한 처리 규칙 구축

을 목표로 하는 핵심 단계입니다.

---

## 🎯 Learning Objectives

After completing this module, you will be able to:

- Diagnose missingness patterns (count / rate / columns to prioritize)
- Choose appropriate missing-value strategies (drop vs impute)
- Implement safe imputations (numeric / categorical / grouped)
- Avoid leakage (fit-on-train, apply-on-test mindset)
- Build reusable cleaning utilities for pipelines

본 모듈을 완료하면 다음을 수행할 수 있습니다:

- 결측치 규모/분포를 구조적으로 진단
- 제거(drop) vs 대체(impute) 전략을 합리적으로 선택
- 수치/범주/그룹 기반 결측치 처리 구현
- 데이터 누수(leakage) 방지 관점으로 처리 설계
- 파이프라인에 재사용 가능한 클리닝 유틸 작성

---

## 📂 Files & Progress

### ✅ Day 54 — Missing Values Handling  
`01_missing_values.py`

**Core Coverage (English)**

- Missing value profiling (count / percent)
- Column prioritization (high-missing columns)
- Strategy patterns:
  - row/column dropping thresholds
  - numeric imputation (mean/median)
  - categorical imputation (mode/constant like `"Unknown"`)
  - group-wise imputation (e.g., median by segment)
- Leakage-safe mindset (separate “fit rules” and “apply rules”)
- Utility-style functions for repeatable cleaning

**코드 내 한국어 설명 기준 요약**

- 결측치 개수/비율을 표로 요약
- 결측치 많은 컬럼 우선순위화
- drop vs impute 선택 기준(임계치, 분석 목적)
- 수치/범주형 각각 안전한 대체 전략
- 그룹 기반 대체(세그먼트별 중앙값 등)
- 규칙을 함수화하여 재현 가능하게 구성

---

## 🧠 Recommended Cleaning Order

```text
Raw Data
  ↓
Schema / dtype validation
  ↓
Missing value profiling
  ↓
Drop rules (if needed)
  ↓
Imputation rules (numeric / categorical / grouped)
  ↓
Post-check (missing left? dtype stable?)
  ↓
Clean dataset for EDA / modeling