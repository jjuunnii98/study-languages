# pandas Fundamentals

This directory covers the **fundamental pandas concepts**
required for real-world data analysis and machine learning workflows.

pandas is the primary Python library for structured data manipulation,
built on top of NumPy, and is essential for EDA, preprocessing,
feature engineering, and time-based analytics.

본 폴더는 실전 데이터 분석을 위한
pandas의 핵심 개념과 사용 패턴을 단계적으로 정리합니다.  
NumPy 기반의 표 형태 데이터 처리 라이브러리인 pandas를 활용해  
EDA, 전처리, 피처 엔지니어링, 시계열 처리까지 연결하는 것을 목표로 합니다.

---

## 🎯 Learning Objectives

- Understand pandas core data structures: Series and DataFrame
- Perform selection, filtering, and indexing effectively
- Summarize data using groupby and reshape using pivot/melt
- Combine datasets using merge/join/concat
- Handle time series with datetime parsing and resampling
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
  - Series/DataFrame 생성과 구조 확인 (`shape`, `dtypes`)
  - 기본 선택/필터링 흐름 맛보기
  - 파생 변수 생성의 기초

- `02_select_filter.py` (Day 27)  
  **Selection & Filtering (실전 필수 패턴)**  
  데이터 선택/필터링/정렬을 위한 핵심 문법 정리  
  - 컬럼 선택(Series vs DataFrame)
  - `loc` / `iloc` 기반 행 선택
  - boolean indexing + 다중 조건 필터링
  - `isin`, `between`, `query` 활용
  - `sort_values`, `reset_index` 패턴

- `03_groupby_reshape.py` (Day 28)  
  **GroupBy & Reshape (pivot/melt)**  
  분석 지표 생성과 리포팅 형태 변환의 핵심  
  - `groupby` + `agg`로 지표 생성
  - 다차원 집계(예: segment × month)
  - `pivot_table`로 wide 리포트 구성
  - `melt`로 tidy/long 형태 변환
  - 그룹 내 랭킹(`groupby` + `rank`) 패턴

- `04_merge_join_concat.py` (Day 29)  
  **Merge / Join / Concat (데이터 결합)**  
  SQL JOIN을 pandas에서 구현하는 실전 패턴  
  - `merge(how=inner/left/right/outer)`의 의미
  - `left_on/right_on`으로 key명이 다를 때 결합
  - index 기반 `join` (집계 테이블 붙이기)
  - `concat(axis=0/1)`로 행/열 확장
  - 데이터 정합성 점검(outer + indicator, 중복 key)

- `05_time_series_basics.py` (Day 30)  
  **Time Series Basics (datetime/resample/rolling)**  
  시계열 처리의 기초를 실전 패턴으로 정리  
  - `to_datetime`으로 파싱
  - `.dt`로 날짜 구성요소 추출
  - datetime index 설정 후 `resample` 기간 집계(D/W/M)
  - `rolling` 이동통계(이동평균)
  - datetime slicing으로 기간 필터링

---

## ⏳ Planned

- `06_missing_values.py`  
  Handling missing data (`isna`, `fillna`, `dropna`)  
  결측치 처리 전략

- `07_groupby_time_resample.py`  
  GroupBy + Resample combined patterns  
  그룹 집계 + 기간 집계 결합(리텐션/코호트 전 단계)

- `08_export_reporting.py`  
  Exporting results (csv, parquet) & simple reporting patterns  
  결과 저장 및 리포팅 패턴

---

## 🧠 Why pandas Matters

pandas enables:
- Efficient manipulation of real-world datasets
- Clean and expressive data transformation logic
- Rapid exploratory data analysis (EDA)
- Seamless integration with NumPy and ML libraries
- Time-based aggregation and reporting for business metrics

Most real data science work happens inside pandas.

Mastering pandas means being able to:
**understand data, clean data, combine data, and prepare data for modeling.**

pandas를 잘 다룬다는 것은 결국
**데이터를 이해하고, 정리하고, 결합하고, 모델에 투입 가능한 형태로 만드는 능력**을 의미합니다.

---

## 🔗 Connection to Machine Learning

pandas plays a central role in:
- Feature engineering
- Train/test dataset preparation
- Label creation and transformation
- Model evaluation data handling
- Reproducible analytics pipelines

This module serves as the practical bridge between
numerical computation (NumPy) and applied machine learning.

---

## 📌 학습 요약 (한국어)

- pandas 핵심 자료구조(Series, DataFrame) 이해
- 실전 필수 선택/필터링/정렬 패턴 확보
- groupby/pivot/melt를 통한 요약 및 형태 변환 능력 강화
- merge/join/concat으로 분석용 테이블을 구성하는 결합 역량 확보
- datetime/resample/rolling 기반 시계열 기초 완성

---

## 🚧 Status

**In progress – pandas Fundamentals (Day 26–30 complete)**

This module is actively developed.
Each completed file represents one focused learning day.

본 모듈은 지속적으로 확장되며,
실제 데이터 분석 프로젝트에서 가장 많이 활용되는 도구로 발전합니다.