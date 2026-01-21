# SQL Data Cleaning

This module focuses on **data cleaning and preprocessing techniques in SQL**,
which are essential for reliable analytics, reporting, and machine learning workflows.

본 파트는 SQL을 활용한 **데이터 정제(Data Cleaning)** 기법을 다루며,
실제 분석 및 모델링 단계에서 발생하는 데이터 품질 문제를 해결하는 데 초점을 둡니다.

---

## 🎯 Learning Objectives

- Understand how NULL values affect SQL queries
- Safely handle missing, invalid, or inconsistent data
- Build robust and defensive SQL logic for real-world datasets
- Prepare clean, analysis-ready tables directly from raw data

---

## 📂 Files & Progress

각 파일은 실무에서 자주 발생하는 데이터 품질 이슈를
하나의 주제로 나누어 정리합니다.

---

### ✅ Completed

#### `01_null_handling.sql` (Day 18)
**Handling missing values (NULL)**

**Key topics**
- `IS NULL` / `IS NOT NULL`
- `COALESCE` for default value substitution
- `NULLIF` for standardizing invalid values
- `CASE WHEN` for conditional NULL handling
- NULL behavior in aggregation functions
- Safe calculations with NULL values

**핵심 내용 (한국어 요약)**
- NULL은 0이나 빈 문자열과 다르다
- NULL 비교에는 반드시 `IS NULL` 사용
- 계산식/집계에서 NULL 전파 주의
- 분석 오류를 막기 위한 방어적 SQL 작성

---

### ⏳ Planned

#### `02_case_when.sql`
**Conditional logic and derived features**
- 조건 기반 파생 변수 생성
- 카테고리화 (bucketization)
- 비즈니스 규칙을 SQL로 명시

---

#### `03_string_functions.sql`
**Text cleaning and string normalization**
- `TRIM`, `LOWER`, `UPPER`
- `REPLACE`, `SUBSTRING`
- 패턴 기반 텍스트 정제

---

## 🧠 Why Data Cleaning Matters

Data cleaning is not optional.

- Dirty data leads to wrong insights
- Models trained on unclean data fail silently
- Business decisions rely on consistent definitions

Performing data cleaning directly in SQL:
- Reduces downstream complexity
- Improves reproducibility
- Makes data pipelines more transparent

SQL 데이터 정제는
분석 이전에 반드시 거쳐야 하는 **가장 중요한 단계**입니다.

---

## 📌 학습 요약 (한국어)

- NULL 처리의 정확한 이해
- 실무 데이터 품질 문제 해결 능력 향상
- 안전하고 재현 가능한 SQL 작성
- 이후 분석/모델링 단계의 신뢰성 확보

---

## 🚧 Status

**In progress — Data Cleaning (Day 18 started)**

This module is actively expanded with real-world cleaning patterns.

본 파트는 Day 18부터 시작되었으며,
실무 중심 데이터 정제 패턴을 지속적으로 추가합니다.