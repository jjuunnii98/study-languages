# Time Series Analysis (SQL)

This directory covers **time series analysis patterns** using SQL,
focusing on how event-based metrics evolve over time.

Rather than treating time as a simple grouping key,
this module emphasizes:
- correct time bucketing
- continuity of time (date spine)
- prevention of temporal leakage
- preparation for trend and growth analysis

본 디렉토리는 SQL을 활용해  
이벤트/로그 기반 데이터의 **시간적 변화**를 분석하는 패턴을 다룹니다.

---

## 🎯 Objectives

- Aggregate event data into stable time buckets (day / week / month)
- Handle missing time intervals explicitly (zero-filled)
- Normalize timestamps and manage time zones safely
- Build reusable time-series metric tables (BI-ready)
- Smooth noise and extract trends using moving averages
- Prepare foundations for rolling metrics and growth analysis

---

## 📂 Structure & Progress

Each file represents one core time-series analytics pattern.
Files are completed incrementally with daily commits.

각 파일은 시계열 분석의 핵심 패턴 하나를 다루며,
일일 학습 단위로 순차적으로 완성됩니다.

---

### ✅ Day 32 — Time Bucket Aggregation  
**`01_time_bucket_aggregation.sql`**

Aggregation of event data into continuous time buckets.

**Key Concepts**
- `DATE_TRUNC` for day/week/month bucketing
- Explicit analysis window definition
- Time zone normalization (UTC-based)
- Continuous date spine using `generate_series`
- Zero-filling missing time buckets
- Separation of business logic (e.g., revenue events)

**Output Metrics (example)**
- `bucket_date`
- `event_count`
- `active_users`
- `revenue_sum`
- `purchase_count`
- `avg_revenue_per_purchase`

**Purpose**
- Create a clean, BI-ready daily metrics table
- Serve as the base for rolling averages and growth calculations

---

### ✅ Day 33 — Moving Average (Smoothing & Trend)  
**`02_moving_average.sql`**

Moving averages and rolling metrics using window functions.

**Key Concepts**
- Window frames with `ROWS BETWEEN ...` (explicit rolling window)
- 7-day moving average (MA7) for daily smoothing
- Rolling sums (e.g., 7-day rolling revenue)
- Optional MA excluding “today” for monitoring
- Recommended: compute on a continuous date spine to avoid bias

**Outputs (example)**
- Raw metrics: `dau`, `revenue`
- Smoothed metrics: `dau_ma7`, `dau_ma28`, `revenue_ma7`, `revenue_ma28`
- Rolling metrics: `revenue_roll7_sum`
- Comparison: `dau_minus_ma7`, `dau_vs_trend`

**Purpose**
- Separate trend from noise
- Prepare signals for growth analysis (WoW/MoM) and anomaly checks

---

## 🧠 Why Time Series Analysis Matters

Most real-world analytics questions are time-based:

- Are users becoming more active over time?
- Is revenue growing or stagnating?
- Did a product change create a real trend or just noise?

Incorrect handling of time can cause:
- misleading trends
- hidden seasonality
- severe data leakage (training on future information)

Time series analysis enforces **temporal order**
and ensures insights reflect real behavior.

시계열 분석은 단순 집계가 아니라  
**시간 흐름을 존중하는 분석 규칙**입니다.

---

## 📌 한국어 요약

- Day 32: 시간 버킷 기반 집계 + 날짜 연속성(date spine) + 누락 구간 0 처리
- Day 33: 이동평균(MA)과 rolling 지표로 추세(trend) 추출
- 다음 단계(WoW/MoM, 누적 지표, 이상탐지)로 확장 가능한 기반 완성

이 폴더는  
**실무용 시계열 SQL 분석 템플릿**을 단계적으로 구축하는 모듈입니다.

---

## 🚧 Status

**In progress — Time Series Analysis**

Next recommended topics:
- Week-over-week / Month-over-month growth using `LAG()`
- Cumulative metrics (running totals)
- Seasonality patterns and calendar effects
- Simple anomaly detection rules (z-score, MAD-based)