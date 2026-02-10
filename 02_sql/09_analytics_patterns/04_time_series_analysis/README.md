# Time Series Analysis (SQL)

This directory covers **time series analysis patterns** using SQL,
focusing on how event-based data evolves over time.

Rather than treating time as a simple grouping key,
this module emphasizes:
- correct time bucketing
- continuity of time
- prevention of temporal leakage
- preparation for trend and growth analysis

본 디렉토리는 SQL을 활용해  
이벤트 데이터의 **시간적 변화 구조를 분석**하는 패턴을 다룹니다.

---

## 🎯 Objectives

- Aggregate event data into stable time buckets (day / week / month)
- Handle missing time intervals explicitly
- Normalize timestamps and manage time zones safely
- Build reusable time-series metric tables
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

**Output Metrics**
- `bucket_date`
- `event_count`
- `active_users`
- `revenue_sum`
- `purchase_count`
- `avg_revenue_per_purchase`

**Purpose**
- Create a clean, BI-ready daily metrics table
- Serve as a base for rolling averages and growth calculations

---

## 🧠 Why Time Series Analysis Matters

Most real-world analytics questions are time-based:

- Are users becoming more active over time?
- Is revenue growing or stagnating?
- Do recent changes reflect trends or noise?

Incorrect handling of time can cause:
- misleading trends
- hidden seasonality
- severe data leakage

Time series analysis enforces **causal order** and
ensures that insights reflect real temporal behavior.

시계열 분석은 단순 집계가 아니라  
**시간 흐름을 존중하는 분석 규칙**입니다.

---

## 📌 한국어 요약

- Day 32: 시간 버킷 기반 집계의 표준 패턴 정리
- 날짜 연속성(date spine)을 통한 누락 구간 처리
- 타임존과 기간 경계를 명시적으로 관리
- 이후 rolling, WoW/MoM, 누적 지표 분석의 기반 구축

이 폴더는  
**실무용 시계열 SQL 분석 템플릿의 출발점**입니다.

---

## 🚧 Status

**In progress — Time Series Analysis**

Next recommended topics:
- Moving averages and rolling windows
- Week-over-week / Month-over-month growth
- Lag-based comparisons
- Trend and seasonality detection