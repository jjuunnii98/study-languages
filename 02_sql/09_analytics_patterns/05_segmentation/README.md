# Segmentation Analysis (SQL)

This directory covers **user segmentation analytics patterns** using SQL.  
Segmentation transforms raw behavioral data into structured user groups  
that support marketing, product, and revenue decisions.

> “Not all users are equal. Segmentation quantifies those differences.”

본 디렉토리는 SQL을 활용해  
유저를 행동 기반으로 분류하고,  
그 세그먼트를 KPI와 연결하는 전체 분석 흐름을 다룹니다.

---

## 🎯 Objectives

- Define meaningful user segments based on behavior
- Apply RFM-style logic (Recency, Frequency, Monetary)
- Quantify segment-level performance metrics
- Bridge user grouping with business KPIs
- Build reusable SQL templates for analytics pipelines

---

## 📂 File Structure & Progress

Each file represents a key analytical step.

---

## ✅ Day 35 — Segment Definition  
**`01_segment_definition.sql`**

Defines user segments using behavioral metrics.

### Analytical Logic

- **Recency** → 최근 활동 시점
- **Frequency** → 최근 90일 활동 빈도
- **Monetary** → 최근 90일 매출

### Example Segments

- `vip`  
- `loyal`  
- `at_risk`  
- `inactive`  

### Output

`user_segments`

| user_id | segment | as_of_date | recency_days | frequency_90d | monetary_90d |
|----------|----------|------------|--------------|---------------|--------------|

---

## ✅ Day 36 — Segment Metrics  
**`02_segment_metrics.sql`**

Transforms segments into decision-ready KPIs.

### Metrics Computed

- users
- active_users_30d
- purchasers_90d
- purchases_90d
- revenue_90d
- avg_recency_days
- purchase_rate_pct
- arpu_90d
- arppu_90d

### Analytical Importance

This step answers:

- Which segment drives revenue?
- Which segment is deteriorating?
- Which segment deserves targeted campaigns?

### Output

Segment-level KPI table:

| segment | users | revenue_90d | purchase_rate_pct | arpu_90d | arppu_90d |

---

## 🧠 Why Segmentation Matters

Segmentation is not just grouping —  
it is a **strategic abstraction layer** between raw data and business decisions.

- Marketing → Target high-value users
- Product → Identify retention risk
- Finance → Forecast revenue contribution
- Growth → Optimize lifecycle campaigns

Without segmentation, analytics remains descriptive.  
With segmentation, analytics becomes actionable.

---

## 📌 한국어 요약

- Day 35: 행동 기반 세그먼트 정의 (RFM 로직)
- Day 36: 세그먼트별 KPI 계산 및 리포트 구조화
- 세그먼트는 단순 분류가 아니라, 의사결정 프레임워크이다.

이 폴더는  
**행동 데이터 → 세그먼트 → KPI → 전략 실행**  
으로 이어지는 SQL 분석 패턴 템플릿이다.

---

## 🚧 Status

Completed (Day 35–36)

This module forms a reusable segmentation framework  
for marketing analytics, product analytics, and revenue intelligence.