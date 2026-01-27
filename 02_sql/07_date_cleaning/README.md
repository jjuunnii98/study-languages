# SQL Data Cleaning

This directory focuses on **data cleaning and preprocessing techniques in SQL**.

Data cleaning is a critical step in any data pipeline.
Poorly cleaned data leads to incorrect joins, misleading aggregations,
and unreliable analytical results.

본 폴더는 SQL을 활용한 **데이터 정제(Data Cleaning)** 핵심 기법을 다룹니다.
실무 분석 및 머신러닝 파이프라인에서 반드시 필요한 전처리 패턴을
SQL 단계에서 안정적으로 수행하는 것을 목표로 합니다.

---

## 🎯 Learning Objectives

- Handle missing and invalid values using SQL
- Normalize and standardize categorical fields
- Clean and transform string-based data
- Improve data quality before analysis or modeling
- Build reliable SQL preprocessing pipelines

---

## 📂 Files & Progress

### `01_null_handling.sql` (Day 18)
Handling NULL values

- `IS NULL`, `IS NOT NULL`
- `COALESCE`, `NULLIF`
- Default value substitution
- NULL-safe logic patterns

**한국어 요약**
- 결측치 판별과 대체 전략 이해
- SQL 단계에서 데이터 안정성 확보
- 집계/분석 오류 예방

---

### `02_case_when.sql` (Day 19)
Conditional logic with CASE WHEN

- Conditional transformation of values
- Category normalization
- Rule-based feature engineering
- Combining CASE with aggregation

**한국어 요약**
- 조건 기반 데이터 변환
- 범주형 데이터 정규화
- 파생 변수(feature) 생성 패턴 습득

---

### `03_string_functions.sql` (Day 20)
String processing and text cleaning

- Case normalization (`LOWER`, `UPPER`)
- Whitespace removal (`TRIM`, `LTRIM`, `RTRIM`)
- Substring extraction (`SUBSTRING`, `LEFT`, `RIGHT`)
- String replacement (`REPLACE`)
- String concatenation (`CONCAT`, `CONCAT_WS`)
- Position-based parsing (`POSITION`)
- Practical text-cleaning patterns

**한국어 요약**
- 문자열 기반 데이터 정제 핵심 함수 정리
- 날짜/코드/이메일 등 문자열 파싱
- 분석 품질을 높이는 SQL 문자열 처리 전략

---

## 🧠 Why Data Cleaning in SQL Matters

Cleaning data at the SQL layer:
- Reduces downstream complexity in Python or ML pipelines
- Ensures consistent joins and aggregations
- Improves model input quality
- Makes analytical results more trustworthy

SQL 기반 전처리는:
- 파이프라인 초기에 오류를 차단하고
- 분석/모델링 단계의 부담을 크게 줄여줍니다.

---

## 🚧 Status

**Completed — Data Cleaning (Day 18–20)**

This section is complete.
Next steps naturally extend to:
- Query performance optimization
- Window functions
- CTE-based transformations

본 파트는 Day 18–20까지 완료되었으며,
이후 성능 최적화 및 고급 쿼리 파트로 연결됩니다.