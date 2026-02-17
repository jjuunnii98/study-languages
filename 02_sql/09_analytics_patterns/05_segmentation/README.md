# Segmentation (SQL) — Analytics Patterns 05

This directory covers **user segmentation analysis patterns** using SQL.

Segmentation answers a core analytics question:

> **“Which groups of users behave differently — and how should we act on it?”**

본 디렉토리는 SQL로 **세그먼트를 정의하고**,  
각 세그먼트의 **핵심 지표를 계산한 뒤**,  
세그먼트 간 **성과 차이를 비교**하는 실전 패턴을 다룹니다.

---

## 🎯 Learning Objectives

By completing this module, you will be able to:

- Define segments using clear business rules (rule-based segmentation)
- Compute segment-level KPIs for reporting and decision-making
- Compare segments with standardized metrics (share, rank, lift)
- Produce analysis outputs ready for BI dashboards and product strategy

---

## 📂 Files & Progress

Each file represents a step in the segmentation workflow:

**Segment Definition → Segment Metrics → Segment Comparison**

---

### ✅ Day 35 — Segment Definition  
`01_segment_definition.sql`

**What it does**

- Defines segments based on stable user attributes or behavioral rules
- Outputs a consistent segmentation table that downstream queries can reuse

**Core concepts**

- `segment_key` / `segment_value` design pattern  
- Rule-based segmentation (e.g., country/device/plan/tenure)
- Reusable segmentation layer (base table or CTE)

**Output (recommended)**

- `user_segments(user_id, segment_key, segment_value)`

**한국어 요약**

- 세그먼트 기준을 명확히 정의(속성 기반/규칙 기반)
- 분석에 재사용 가능한 세그먼트 테이블 구조 설계

---

### ✅ Day 36 — Segment Metrics  
`02_segment_metrics.sql`

**What it does**

- Aggregates user activity into segment-level KPIs

**Typical metrics**

- users, active_users
- orders, revenue
- active_rate, purchase_rate
- ARPU, AOV (optional)

**Output (example)**

- `segment_metrics(segment_key, segment_value, users, active_users, orders, revenue, ...)`

**한국어 요약**

- 세그먼트별 KPI 집계(활성률/전환율/ARPU 등)
- 리포트/대시보드 친화적 형태로 결과 구성

---

### ✅ Day 37 — Segment Comparison  
`03_segment_comparison.sql`

**What it does**

- Compares segment KPIs side-by-side and adds business-ready context

**Comparison features**

- `user_share` (segment size share)
- `*_lift` vs overall baseline (relative performance)
- ranking (e.g., ARPU rank)

**Why it matters**

Segmentation is only useful when you can answer:

- Which segment is big enough to matter? (**share**)
- Which segment performs better/worse than average? (**lift**)
- Which segment should we prioritize? (**rank**)

**한국어 요약**

- 세그먼트 간 성과 차이를 “규모(share) + 상대 성과(lift) + 우선순위(rank)”로 비교
- 실무 의사결정에 바로 연결되는 비교 결과 생성

---

## 🧠 Recommended Data Model (Concept)

These SQL patterns assume a common analytics setup:

- `users(user_id, signup_date, country, device_type, plan, ...)`
- `events(user_id, event_time, event_name, revenue, ...)`

Segmentation is typically **joined to user-level activity**, then aggregated.

---

## 🔄 Workflow Summary

```text
User Table / Event Table
        ↓
(1) Define Segments
        ↓
(2) Compute Segment Metrics
        ↓
(3) Compare Segments (share / lift / rank)
        ↓
BI Dashboard / Product Decisions