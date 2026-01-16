# SQL Window Functions

This directory covers **SQL Window Functions**, which enable advanced analytics
while preserving row-level detail.

Window functions are essential for:
- ranking and tiering
- cumulative metrics
- top-N per group
- time-series comparisons (lag/lead)
- feature engineering for analytics and ML workflows

본 폴더는 SQL의 **윈도우 함수(Window Functions)**를 다룹니다.  
윈도우 함수는 `GROUP BY`처럼 행을 합치지 않고도,
**각 행을 유지한 채 분석 지표를 함께 계산**할 수 있게 해줍니다.

---

## 🎯 Learning Objectives

- Understand the purpose of window functions and the `OVER()` clause
- Use `PARTITION BY` for group-aware analytics
- Use `ORDER BY` for ordered/cumulative analytics
- Apply ranking functions (`RANK`, `DENSE_RANK`, `ROW_NUMBER`)
- Build practical patterns such as **Top-N per group** and **stable ranking**
- Prepare for time-aware analytics (e.g., `LAG`, `LEAD`)

---

## 📂 Files & Progress

Each file is written with practical analytics use cases in mind.
Files are completed incrementally with daily commits.

각 파일은 실무 분석에 바로 적용 가능한 예제 중심으로 구성되어 있으며,
Day 단위로 점진적으로 확장됩니다.

---

## ✅ Completed

### `01_ever_clause.sql` (Day 13)
**OVER clause fundamentals**

**Key topics**
- Basic `OVER()` usage
- Difference between `GROUP BY` and window functions
- `PARTITION BY` for group-wise analytics
- `ORDER BY` within `OVER()` for ordered/cumulative patterns
- Preserving row-level detail while adding aggregate context

**핵심 포인트(한국어)**
- 윈도우 함수의 시작점은 `OVER()`  
- `GROUP BY`는 행을 줄이지만, 윈도우 함수는 **행을 유지**한다  
- `PARTITION BY`로 그룹 기준 분석, `ORDER BY`로 순서/누적 분석 가능

---

### `02_rank_dense_rank.sql` (Day 14)
**Ranking functions: tie-handling and practical patterns**

**Key topics**
- `RANK()` vs `DENSE_RANK()` differences (tie-handling)
- Stable / deterministic ranking using tie-breakers in `ORDER BY`
- Partitioned ranking: ranking **within groups**
- Top-N per group using CTE/subquery filtering (`rank <= N`)
- A realistic example pattern: customer tiering

**핵심 포인트(한국어)**
- `RANK()`는 동점 후 순위를 건너뜀 (1,1,3…)  
- `DENSE_RANK()`는 동점 후 순위가 연속 (1,1,2…)  
- 실무에서는 재현성을 위해 `ORDER BY`에 tie-breaker를 추가하는 것이 중요

---

## ⏳ Planned

### `03_row_number.sql`
**Row numbering and deduplication**
- `ROW_NUMBER()` for unique ordering
- Deduplication patterns (latest record per group)
- Top-1 per group
- Pagination and deterministic selection

---

## 🧠 Why Window Functions Matter

Window functions enable:
- analytical features without losing granularity
- scalable ranking and segmentation
- time-aware comparisons in longitudinal datasets
- expressive SQL for BI/analytics pipelines
- feature engineering for ML preprocessing (SQL-first workflows)

In modern analytics, window functions are a **core competency**.

---

## 📌 학습 요약 (한국어)

- 윈도우 함수는 **행을 유지**하면서 분석 지표를 계산하는 핵심 SQL 기술
- `OVER()`는 윈도우 함수의 기반이며, `PARTITION BY`/`ORDER BY`로 분석 창을 정의
- `RANK`/`DENSE_RANK`는 동점 처리 규칙이 달라 실무 목적에 따라 선택해야 함
- 그룹별 Top-N, 안정적 순위 계산 등 실무 패턴의 기반이 됨

---

## 🚧 Status

**In progress – Window Functions (Day 13–14 completed)**

Next steps focus on `ROW_NUMBER()` and time-shift functions (`LAG`, `LEAD`)
to support deduplication and time-series analytics.

본 단계는 Day 14까지 완료되었으며,  
다음은 `ROW_NUMBER()` 및 `LAG/LEAD` 기반 시계열 분석으로 확장됩니다.