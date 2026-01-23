# SQL Data Cleaning

This directory covers practical **data cleaning and preprocessing patterns in SQL**.
It focuses on handling missing values, standardizing messy fields, and creating
analysis-ready features directly in SQL.

본 폴더는 SQL로 수행하는 **데이터 정제(Data Cleaning) 및 전처리 패턴**을 다룹니다.  
결측/이상값 처리, 값 표준화, 파생변수 생성 등을 통해  
분석 및 모델링에 바로 사용할 수 있는 형태로 데이터를 정리하는 것을 목표로 합니다.

---

## 📂 Files

### `01_null_handling.sql` (Day 18)
Handling missing values (NULL)

- `IS NULL` / `IS NOT NULL`
- `COALESCE`로 기본값 대체
- `NULLIF`로 무의미한 값(예: 빈 문자열) 정규화
- `CASE WHEN` 기반 NULL 처리
- 집계 함수에서 NULL의 동작 이해
- 계산식에서 NULL 전파 방지 (방어적 처리)

**한국어 요약**
- NULL은 0이나 빈 문자열과 다르다
- 비교는 반드시 `IS NULL`을 사용한다
- 집계/계산/조건문에서 NULL을 방어적으로 처리하는 습관이 중요하다

---

### `02_case_when.sql` (Day 19)
Conditional logic and derived features (feature engineering)

- CASE WHEN 기본 문법과 조건 분기
- 구간화(bucketing)로 범주형 파생 변수 생성
- 결측/이상값을 포함한 데이터 품질 라벨링
- 상태(state) 파생 (예: active/inactive/dormant)
- 집계 전 파생변수 생성 후 GROUP BY 적용 (실무 패턴)
- 조건 우선순위(WHEN 순서)의 중요성
- `COALESCE`/`NULLIF`와 결합한 실전형 정제 패턴

**한국어 요약**
- CASE WHEN은 “비즈니스 규칙”을 SQL로 명시하는 핵심 도구다
- 파생변수(세그먼트/상태/플래그)를 만들면 분석의 해석력이 크게 올라간다
- ELSE를 명시해 예외 케이스를 놓치지 않는 것이 실무적으로 중요하다

---

## 🎯 Learning Objectives

- Handle missing and invalid values safely in SQL
- Standardize messy fields into consistent formats
- Create derived features for segmentation and modeling
- Write robust SQL that supports reproducible analytics pipelines

---

## 🧠 Why Data Cleaning Matters

Data cleaning is not optional.

- Dirty data produces incorrect insights
- Models trained on unclean data fail silently
- Business decisions require consistent definitions

Cleaning data directly in SQL:
- reduces downstream complexity
- improves reproducibility
- makes pipelines transparent and auditable

데이터 정제는 분석/모델링 이전에 반드시 필요한 단계이며,  
SQL 단계에서 정제를 수행하면 파이프라인이 단순해지고 재현성이 높아집니다.

---

## 🚧 Status

**In progress — Data Cleaning (Day 18–19 complete)**

Next steps (planned):
- `03_string_functions.sql` (text cleaning & normalization)

본 파트는 Day 18–19까지 완료되었으며,  
다음은 문자열 정제(텍스트 전처리)로 확장합니다.