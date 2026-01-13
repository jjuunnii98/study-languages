# SQL Window Functions

This directory covers **SQL Window Functions**, which enable
advanced analytical queries while preserving row-level detail.

Window functions are essential for time-series analysis,
ranking, cumulative calculations, and behavioral analytics.

본 폴더는 SQL의 **윈도우 함수(Window Functions)**를 다룹니다.  
윈도우 함수는 행을 그룹으로 묶지 않고도,
각 행 기준의 분석 결과를 함께 계산할 수 있게 해줍니다.

---

## 🎯 Learning Objectives

- Understand what window functions are and why they matter
- Learn how the OVER clause defines analytical windows
- Apply PARTITION BY and ORDER BY for grouped analytics
- Distinguish window functions from GROUP BY aggregations
- Prepare for ranking and time-based analytical functions

---

## 📂 Files & Progress

Each file represents a focused analytical concept.
Examples are written with **practical analytics use cases** in mind.

각 파일은 실무에서 자주 사용되는 분석 패턴을 중심으로 구성되어 있습니다.

---

### ✅ Completed

#### `01_ever_clause.sql` (Day 13)
**OVER clause fundamentals**

- Basic usage of `OVER()`
- Difference between `GROUP BY` and window functions
- `PARTITION BY` for grouped analytics
- `ORDER BY` for cumulative calculations
- Combining `PARTITION BY` and `ORDER BY`
- Preserving row-level detail while adding aggregate context

> 윈도우 함수의 핵심은 **OVER 절**입니다.  
> 이 파일은 이후 모든 윈도우 함수 학습의 기반이 됩니다.

---

### ⏳ Planned

#### `02_rank_dense_rank.sql`
**Ranking functions**

- `RANK()` vs `DENSE_RANK()`
- Handling ties in ordered data
- Ranking within partitions
- Practical ranking use cases

---

#### `03_row_number.sql`
**Row numbering**

- `ROW_NUMBER()` for unique row ordering
- Deduplication patterns
- Pagination logic
- Selecting top-N records per group

---

#### `04_lag_lead.sql`
**Time-aware analysis**

- `LAG()` and `LEAD()` functions
- Comparing current and previous rows
- Time-series change detection
- Financial and behavioral analytics patterns

---

## 🧠 Why Window Functions Matter

Window functions allow you to:

- Perform advanced analytics without collapsing rows
- Analyze trends over time
- Rank and compare entities within groups
- Build features for financial, healthcare, and behavioral data
- Write expressive and performant analytical SQL

In modern data analytics,
window functions are a **must-have skill**.

---

## 📌 학습 요약 (한국어)

- 윈도우 함수는 행 단위 분석을 가능하게 하는 핵심 SQL 기능
- `OVER()`는 모든 윈도우 함수의 출발점
- `PARTITION BY`는 분석 그룹을 정의
- `ORDER BY`는 누적·순서 기반 분석을 가능하게 함
- GROUP BY로는 불가능한 분석을 가능하게 함

---

## 🚧 Status

**In progress – Window Functions (Day 13 started)**

This module is actively developed.
The next steps include ranking and time-shift functions.

본 단계는 Day 13부터 진행 중이며,  
이후 순위 함수와 시계열 분석으로 확장됩니다.