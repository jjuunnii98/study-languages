# pandas Fundamentals

This directory covers the **fundamental pandas concepts**
required for real-world data analysis and machine learning workflows.

pandas is the primary Python library for structured data manipulation,
built on top of NumPy, and is essential for EDA, preprocessing,
and feature engineering.

본 폴더는 실전 데이터 분석을 위한
pandas의 핵심 개념과 사용 패턴을 단계적으로 정리합니다.

---

## 🎯 Learning Objectives

- Understand pandas core data structures: Series and DataFrame
- Perform selection, filtering, and indexing effectively
- Build intuition for tabular data manipulation and EDA workflows
- Prepare for aggregation, merging, and feature engineering
- Connect pandas workflows to machine learning pipelines

---

## 📂 Structure & Progress

Each file represents one focused daily learning unit.
The module is expanded incrementally with clear analytical intent.

각 파일은 하루 단위 학습 단위로 구성되며,
실전 데이터 분석 흐름(EDA → 전처리 → 모델링)과 연결되도록 설계되었습니다.

### ✅ Completed

- `01_series_dataframe.py` (Day 26)  
  Core pandas data structures: **Series & DataFrame**  
  pandas 핵심 자료구조 이해 및 기본 조작  
  - Series 생성과 인덱스 개념
  - DataFrame 생성 및 구조 확인(shape, dtypes)
  - 컬럼/행 선택 기초
  - 조건 필터링 및 파생 변수 생성

- `02_select_filter.py` (Day 27)  
  **Selection & Filtering (실전 필수 패턴)**  
  데이터 선택/필터링/정렬을 위한 핵심 문법 정리  
  - 컬럼 선택(Series vs DataFrame)
  - `loc` / `iloc` 기반 행 선택
  - boolean indexing + 다중 조건 필터링
  - `isin`, `between`, `query` 활용
  - `sort_values`, `reset_index` 패턴

---

## ⏳ Planned

- `03_missing_values.py`  
  Handling missing data (`isna`, `fillna`, `dropna`)  
  결측치 처리 전략

- `04_groupby_basics.py`  
  Aggregation and group-based analysis  
  그룹 연산 및 요약 통계

- `05_merge_concat.py`  
  Combining datasets  
  데이터 병합과 결합

---

## 🧠 Why pandas Matters

pandas enables:
- Efficient manipulation of real-world datasets
- Clean and expressive data transformation logic
- Rapid exploratory data analysis (EDA)
- Seamless integration with NumPy and ML libraries

Most real data science work happens inside pandas.

Mastering pandas means being able to:
**understand data, clean data, and prepare data for modeling.**

pandas를 잘 다룬다는 것은 결국
**데이터를 이해하고, 정리하고, 모델에 투입할 수 있는 형태로 만드는 능력**을 의미합니다.

---

## 🔗 Connection to Machine Learning

pandas plays a central role in:
- Feature engineering
- Train/test dataset preparation
- Label creation and transformation
- Model evaluation data handling

This module serves as the practical bridge between
numerical computation (NumPy) and applied machine learning.

---

## 📌 학습 요약 (한국어)

- pandas 핵심 자료구조(Series, DataFrame) 이해
- 실전 필수인 선택/필터링/정렬 패턴 확보
- EDA 및 전처리 파이프라인의 기본기 강화
- 이후 groupby, 결측치 처리, merge로 확장 준비

---

## 🚧 Status

**In progress – pandas Fundamentals (Day 26–27 complete)**

This module is actively developed.
Each completed file represents one focused learning day.

본 모듈은 지속적으로 확장되며,
실제 데이터 분석 프로젝트에서 가장 많이 활용되는 도구로 발전합니다.