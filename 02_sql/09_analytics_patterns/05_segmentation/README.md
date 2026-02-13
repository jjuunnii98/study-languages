# Segmentation (SQL)

This directory covers **practical user segmentation patterns** using SQL.

Segmentation answers a core analytics question:

> **“Which users behave differently, and how should we group them for decisions?”**

Segmentation is not just labeling.
It is a decision framework that supports:
- targeting (CRM / marketing)
- product personalization
- retention strategy
- risk monitoring and alerts
- KPI reporting by segment

본 디렉토리는 SQL로 **사용자/고객 세그먼트**를 정의하는 실전 패턴을 다룹니다.

세그먼테이션의 핵심 질문은 다음입니다:

> **“행동이 다른 사용자들을 어떻게 그룹화해서 의사결정에 활용할 것인가?”**

세그먼트는 단순 분류가 아니라,
타겟팅/리텐션/리스크 관리/지표 보고를 위한 **의사결정 단위**입니다.

---

## 🎯 Objectives

- Define segments with reproducible SQL rules (not “black box” labels)
- Build snapshot-based segmentation tables (`as_of_date`)
- Use RFM-style signals: Recency / Frequency / Monetary
- Store supporting metrics for validation and future threshold tuning
- Enable downstream analysis by joining segments to KPI tables

---

## 📂 File Structure & Progress

Each file represents one analytical step.
Later steps build directly on earlier definitions.

각 파일은 하나의 분석 단계를 담당하며,
이전 단계의 정의를 기반으로 확장됩니다.

---

## ✅ Completed

### ✅ Day 35 — Segment Definition (Rule-based + RFM)
**`01_segment_definition.sql`**

**Purpose**
- Create a reusable segmentation output table/view:
  `user_id, segment, as_of_date, recency_days, frequency_90d, monetary_90d`

**Key Concepts**
- Snapshot-based segmentation using `as_of_date`
- RFM-like metrics:
  - Recency: days since last purchase/activity
  - Frequency: purchase count in last 90 days
  - Monetary: revenue in last 90 days
- Rule-based segment assignment via `CASE`
  - `new_or_active`
  - `vip`
  - `repeat_buyer`
  - `at_risk`
  - `inactive`

**Why it matters**
- Rule-based segmentation is explainable:
  “Why is this user VIP?” can be answered directly.
- Storing metrics makes it easy to tune thresholds later.

---

## 🧠 Why Segmentation Matters

Average metrics hide important user behavior differences.

Segmentation enables:
- targeted retention campaigns (e.g., at-risk users)
- prioritizing high-value users (VIP)
- measuring KPI changes by segment
- building “risk-aware” monitoring rules

평균 지표는 중요한 차이를 숨깁니다.

세그먼테이션을 하면:
- 이탈 위험군(at_risk) 대상 캠페인
- VIP 우선순위 관리
- 세그먼트별 KPI 비교
- 리스크 기반 모니터링 룰 구축
이 가능해집니다.

---

## 🚀 Next (Recommended)

Suggested next steps for this module:

- Segment KPI summary (ARPU, conversion, retention by segment)
- Transition matrix (segment movement over time)
- Behavioral clustering (optional): compare rule-based vs clustering-based segments
- Dashboard-ready outputs for BI tools

---

## 🚧 Status

**In progress — Segmentation (Day 35 completed)**  
This module will expand into segment KPI reporting and time-based transitions.# Segmentation (SQL)

This directory covers **practical user segmentation patterns** using SQL.

Segmentation answers a core analytics question:

> **“Which users behave differently, and how should we group them for decisions?”**

Segmentation is not just labeling.
It is a decision framework that supports:
- targeting (CRM / marketing)
- product personalization
- retention strategy
- risk monitoring and alerts
- KPI reporting by segment

본 디렉토리는 SQL로 **사용자/고객 세그먼트**를 정의하는 실전 패턴을 다룹니다.

세그먼테이션의 핵심 질문은 다음입니다:

> **“행동이 다른 사용자들을 어떻게 그룹화해서 의사결정에 활용할 것인가?”**

세그먼트는 단순 분류가 아니라,
타겟팅/리텐션/리스크 관리/지표 보고를 위한 **의사결정 단위**입니다.

---

## 🎯 Objectives

- Define segments with reproducible SQL rules (not “black box” labels)
- Build snapshot-based segmentation tables (`as_of_date`)
- Use RFM-style signals: Recency / Frequency / Monetary
- Store supporting metrics for validation and future threshold tuning
- Enable downstream analysis by joining segments to KPI tables

---

## 📂 File Structure & Progress

Each file represents one analytical step.
Later steps build directly on earlier definitions.

각 파일은 하나의 분석 단계를 담당하며,
이전 단계의 정의를 기반으로 확장됩니다.

---

## ✅ Completed

### ✅ Day 35 — Segment Definition (Rule-based + RFM)
**`01_segment_definition.sql`**

**Purpose**
- Create a reusable segmentation output table/view:
  `user_id, segment, as_of_date, recency_days, frequency_90d, monetary_90d`

**Key Concepts**
- Snapshot-based segmentation using `as_of_date`
- RFM-like metrics:
  - Recency: days since last purchase/activity
  - Frequency: purchase count in last 90 days
  - Monetary: revenue in last 90 days
- Rule-based segment assignment via `CASE`
  - `new_or_active`
  - `vip`
  - `repeat_buyer`
  - `at_risk`
  - `inactive`

**Why it matters**
- Rule-based segmentation is explainable:
  “Why is this user VIP?” can be answered directly.
- Storing metrics makes it easy to tune thresholds later.

---

## 🧠 Why Segmentation Matters

Average metrics hide important user behavior differences.

Segmentation enables:
- targeted retention campaigns (e.g., at-risk users)
- prioritizing high-value users (VIP)
- measuring KPI changes by segment
- building “risk-aware” monitoring rules

평균 지표는 중요한 차이를 숨깁니다.

세그먼테이션을 하면:
- 이탈 위험군(at_risk) 대상 캠페인
- VIP 우선순위 관리
- 세그먼트별 KPI 비교
- 리스크 기반 모니터링 룰 구축
이 가능해집니다.

---

## 🚀 Next (Recommended)

Suggested next steps for this module:

- Segment KPI summary (ARPU, conversion, retention by segment)
- Transition matrix (segment movement over time)
- Behavioral clustering (optional): compare rule-based vs clustering-based segments
- Dashboard-ready outputs for BI tools

---

## 🚧 Status

**In progress — Segmentation (Day 35 completed)**  
This module will expand into segment KPI reporting and time-based transitions.