# Cohort Analysis

This directory covers **cohort analysis fundamentals** using SQL.
A cohort groups users by a shared starting event (e.g., first purchase, signup),
and measures how user behavior changes over time after that starting point.

본 폴더는 SQL로 수행하는 **코호트 분석의 핵심 흐름**을 다룹니다.  
코호트는 “첫 구매/첫 가입/첫 이벤트”처럼 동일한 시작점을 기준으로 사용자를 묶고,  
시간이 지남에 따라 행동(활동/재구매/잔존)이 어떻게 변화하는지를 분석합니다.

---

## 🎯 Learning Objectives

- Define cohorts based on users’ first event
- Compute cohort size as the base denominator
- Prepare a clean foundation for retention and LTV analysis
- Practice reusable SQL patterns using CTEs

---

## 📂 Files & Progress

Each file represents one step of a realistic cohort analysis pipeline.

각 파일은 “실무 코호트 분석 파이프라인”을 단계별로 분해하여 구성했습니다.

### ✅ Completed

- `01_define_cohort.sql` (Day 23)  
  **Define cohort by first event time**  
  첫 이벤트(예: purchase)를 기준으로 코호트 월(cohort_month) 정의  
  - `MIN(event_time)`로 유저별 첫 이벤트 산출  
  - `DATE_TRUNC('month', ...)`로 월 단위 코호트 라벨링  
  - 코호트 월별 유저 수 집계로 정의 검증

- `02_cohort_size.sql` (Day 24)  
  **Compute cohort size (initial users)**  
  각 코호트의 초기 유저 수(cohort_size) 계산  
  - Retention/LTV 분석의 분모(기준값)로 사용  
  - Cohort 정의 로직을 재사용 가능한 형태로 분리

---

## 🧠 Why Cohort Size Matters

Cohort analysis is not only about counting users later.
It starts by defining the **correct denominator**:

- Cohort Size = users who entered the cohort in the first period
- Retention Rate = active_users / cohort_size
- Cohort LTV = cohort_revenue / cohort_size

코호트 크기(cohort_size)는 이후 분석의 기준점(분모)이기 때문에  
**초기 코호트 정의가 정확해야** 결과가 신뢰 가능해집니다.

---

## 🔜 Next Steps (Recommended)

To complete a full cohort analysis workflow, the next steps typically are:

1. `03_activity_by_cohort.sql`  
   코호트별 기간별(월/주) 활동 유저 집계

2. `04_retention_matrix.sql`  
   코호트 잔존율 매트릭스 구성 (기간 offset 기반)

3. `05_cohort_ltv.sql`  
   코호트 LTV 계산 (매출/수익 기반)

---

## ⚙ Notes (DB Differences)

This repo uses `DATE_TRUNC('month', ...)` (PostgreSQL-style).
If you use other DBs, adjust date functions accordingly:

- MySQL: `DATE_FORMAT(ts, '%Y-%m-01')`
- BigQuery: `DATE_TRUNC(DATE(ts), MONTH)`
- Snowflake: `DATE_TRUNC('MONTH', ts)`

본 템플릿은 PostgreSQL 스타일을 기본으로 작성되어 있으며,  
DB에 따라 날짜 함수만 바꾸면 동일한 로직으로 적용할 수 있습니다.

---

## 🚧 Status

**In progress – Cohort Analysis (Day 23–24 complete)**

본 폴더는 현재 진행 중이며,  
Day 23–24(코호트 정의 및 코호트 크기)가 완료된 상태입니다.