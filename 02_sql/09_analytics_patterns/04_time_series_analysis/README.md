# Time Series Analysis (SQL)

This directory covers **core time series analysis patterns** using SQL.  
Time series analysis focuses on understanding **how metrics evolve over time**,
detecting trends, seasonality, and changes in growth dynamics.

> **“How is the metric changing over time, and compared to the past?”**

본 디렉토리는 SQL만으로  
시계열 데이터를 **집계 → 비교 → 해석**하는 핵심 분석 패턴을 다룹니다.

---

## 🎯 Objectives

- Aggregate metrics into consistent time buckets (day / week / month)
- Compare current values against previous periods (PoP: DoD / WoW / MoM)
- Smooth noisy metrics using moving averages
- Produce BI-ready time series outputs
- Build reusable SQL templates for dashboards and analytics

---

## 📂 File Structure & Progress

Each file represents one fundamental time series analysis step.
Later steps build directly on earlier outputs.

---

### ✅ Day 32 — Time Bucket Aggregation  
**`01_time_bucket_aggregation.sql`**

- Raw event 데이터를 시간 단위로 집계
- 일별 / 주별 / 월별 지표 생성

**Key Concepts**
- `DATE_TRUNC()`  
- Time bucket standardization  
- Metric aggregation (COUNT, SUM)

**Output**
- `bucket_date`
- aggregated metrics (e.g. DAU, revenue)

---

### ✅ Day 33 — Moving Average  
**`02_moving_average.sql`**

- 시계열 변동성 완화를 위한 이동 평균 계산
- 단기 노이즈 제거 및 추세 파악

**Key Concepts**
- Window functions (`AVG() OVER`)
- Rolling window (7-day, 14-day)
- Trend smoothing

**Output**
- `metric_value`
- `moving_avg_n_days`

---

### ✅ Day 34 — Period-over-Period (PoP) Analysis  
**`03_period_over_period.sql`**

- 이전 기간 대비 변화량 및 성장률 계산
- DoD / WoW / MoM 분석의 표준 패턴

**Key Concepts**
- `LAG()` window function
- Absolute change vs. percentage change
- Division-by-zero & NULL handling
- BI-friendly output design

**Metrics**
- Day-over-Day (DoD)
- Week-over-Week (WoW)
- (확장 가능) Month-over-Month (MoM)

**Output**
- current value
- previous period value
- diff
- growth rate (%)

---

## 🧠 Why Time Series Analysis Matters

Time series analysis answers critical business questions:

- Is the product growing or stagnating?
- Are recent changes meaningful or just noise?
- Did a feature release or campaign have impact?
- Is growth accelerating or decelerating?

시계열 분석은 단순 조회가 아니라  
**의사결정을 위한 변화 감지 도구**입니다.

---

## 📌 한국어 요약

- Day 32: 시간 단위로 데이터 집계 (기초 지표 생성)
- Day 33: 이동 평균으로 추세 파악
- Day 34: 이전 기간 대비 변화량 및 성장률 계산

이 폴더는  
**SQL 기반 시계열 분석의 표준 템플릿**을 제공합니다.

---

## 🚧 Status

**Completed (Day 32–34)**  

This module forms a complete, reusable SQL time series analysis toolkit  
suitable for analytics, BI dashboards, and data-driven decision-making.