# SQL Aggregation

This directory covers **SQL aggregation techniques**, which are fundamental for
data analysis, reporting, and feature engineering.

Aggregation transforms raw transactional data into
meaningful summaries that can be directly used for
analytics, decision-making, and machine learning pipelines.

본 폴더는 SQL의 **집계(Aggregation)** 개념을 체계적으로 다룹니다.  
집계는 원시 데이터를 요약하여 의미 있는 정보로 변환하는 핵심 과정이며,
데이터 분석·리포트·머신러닝 전처리에서 필수적인 기술입니다.

---

## 🎯 Learning Objectives

- Summarize data using GROUP BY
- Filter aggregated results correctly with HAVING
- Understand COUNT, SUM, AVG and their NULL-handling behavior
- Avoid common aggregation mistakes in real-world datasets
- Build aggregation queries suitable for analytics and ML features

---

## 📂 Files & Progress

Each file represents one focused learning unit
with **practical SQL examples and detailed Korean explanations**.

각 파일은 실무에서 바로 활용 가능한 예제를 중심으로 구성되며,
집계 로직에서 자주 발생하는 실수 포인트를 함께 설명합니다.

---

### ✅ Completed

#### `01_group_by.sql` (Day 9)
**GROUP BY basics**

- Grouping by one or multiple columns
- Using aggregation functions with GROUP BY
- Combining GROUP BY with ORDER BY
- Understanding grouping constraints

> GROUP BY는 데이터 분석에서  
> “어떤 기준으로 요약할 것인가”를 결정하는 출발점입니다.

---

#### `02_having.sql` (Day 10)
**Filtering aggregated results with HAVING**

- Difference between WHERE and HAVING
- Filtering groups after aggregation
- Combining WHERE + GROUP BY + HAVING
- Common mistakes when filtering aggregated data

> HAVING은 집계된 결과를 조건으로 필터링할 때 사용하는 문법으로,  
> 실무 SQL에서 매우 자주 등장합니다.

---

#### `03_count_sum_avg.sql` (Day 11)
**COUNT / SUM / AVG and NULL handling**

- `COUNT(*)` vs `COUNT(column)`
- How SUM and AVG treat NULL values
- Handling all-NULL groups with COALESCE
- Preventing division-by-zero with NULLIF
- Customer-level aggregation as feature engineering examples

> NULL과 0의 차이를 이해하는 것은  
> 정확한 분석과 신뢰할 수 있는 지표 계산의 핵심입니다.

---

## 🧠 Why Aggregation Matters

Aggregation is essential for:

- Exploratory Data Analysis (EDA)
- Business metrics and reporting
- Cohort analysis and risk analysis
- Feature engineering for machine learning models

Without proper aggregation logic,
raw data cannot be transformed into actionable insights.

집계 개념이 없으면
대부분의 실무 데이터 분석은 불가능합니다.

---

## 📌 Practical Takeaways (한국어 요약)

- GROUP BY는 요약 분석의 핵심 문법
- HAVING은 집계 결과를 필터링할 때 반드시 필요
- COUNT/SUM/AVG는 NULL 처리 방식이 서로 다름
- COALESCE와 NULLIF는 실무 집계 쿼리의 기본 안전장치
- 집계 결과는 ML 모델의 핵심 입력(feature)으로 활용됨

---

## 🚧 Status

**Completed – SQL Aggregation (Day 9–11)**

This module forms a complete aggregation block
and serves as a foundation for subqueries, window functions,
and advanced analytical SQL.

본 단원은 Day 11까지 완료되었으며,  
이후 서브쿼리·윈도우 함수·고급 분석 SQL로 확장됩니다.