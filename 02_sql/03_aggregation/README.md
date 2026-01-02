# SQL Aggregation

This directory covers **SQL aggregation techniques**, which are essential for
data analysis, reporting, and feature engineering.

Aggregation allows us to summarize raw transactional data into
meaningful insights that can be directly used for decision-making
and machine learning pipelines.

본 폴더는 SQL의 **집계(Aggregation)** 개념을 다룹니다.  
집계는 원시 데이터를 요약하여 의미 있는 정보로 변환하는 핵심 과정이며,
데이터 분석·리포트·머신러닝 전처리에서 필수적인 기술입니다.

---

## 🎯 Learning Objectives

- Understand how to summarize data using GROUP BY
- Filter aggregated results correctly using HAVING
- Distinguish between row-level filtering and group-level filtering
- Apply aggregation logic for real-world analytics use cases

---

## 📂 Files & Progress

### ✅ Completed

#### `01_group_by.sql` (Day 9)
**GROUP BY basics and aggregation logic**

- Grouping data by one or multiple columns
- Using aggregation functions (SUM, COUNT, AVG)
- Combining GROUP BY with ORDER BY
- Understanding grouping behavior and constraints

> GROUP BY는 데이터 분석에서
> "어떤 기준으로 요약할 것인가"를 결정하는 핵심 문법입니다.

---

#### `02_having.sql` (Day 10)
**Filtering aggregated results with HAVING**

- Difference between WHERE and HAVING
- Applying conditions to aggregated values
- Combining WHERE + GROUP BY + HAVING
- Common mistakes when filtering aggregated data

> HAVING은 "집계된 결과"를 필터링할 때 사용하는 문법으로,
> 실무 SQL에서 매우 자주 등장합니다.

---

## 🧠 Why Aggregation Matters

Aggregation is critical for:

- Exploratory Data Analysis (EDA)
- Business metrics and reporting
- Feature engineering for machine learning
- Risk analysis and cohort analysis

Without proper aggregation logic,
raw data cannot be transformed into actionable insights.

집계 개념이 없으면
대부분의 실무 데이터 분석은 불가능합니다.

---

## 📌 Practical Perspective (한국어 요약)

- GROUP BY는 데이터 요약의 출발점
- HAVING은 집계 결과를 조건으로 필터링할 때 필수
- WHERE와 HAVING의 역할 구분은 SQL 실력의 기준점
- 분석 SQL → ML Feature Engineering으로 자연스럽게 연결됨

---

## 🚧 Status

**In progress – SQL Aggregation**

Next planned file:
- `03_count_sum_avg.sql`  
  Detailed comparison of COUNT, SUM, AVG and NULL handling

본 단원은 순차적으로 확장되며,
집계 함수 심화까지 완료되면 하나의 완성된 분석 블록이 됩니다.