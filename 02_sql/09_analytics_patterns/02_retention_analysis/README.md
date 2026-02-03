# Retention Analysis (SQL)

This directory documents **user retention analysis patterns implemented in SQL**.

Retention analysis answers one fundamental analytics question:

> **“After their first engagement, how many users remain active over time?”**

본 디렉토리는 SQL을 활용해  
리텐션을 **정의 → 구조화 → 지표화**하는 전 과정을 단계적으로 정리합니다.

---

## 🎯 Objectives

- Define retention with clear, reproducible analytical logic
- Measure user retention over time using cohort-based methods
- Construct retention matrices suitable for visualization and BI tools
- Calculate standardized retention rate metrics
- Produce clean, report-ready SQL outputs

---

## 📂 Structure & Learning Flow

Each SQL file represents **one analytical step**.  
Later steps are explicitly built on the outputs of earlier ones.

---

### ✅ Day 26 — Retention Definition  
**`01_define_retention.sql`**

Defines what “retention” means in analytical terms.

**What this step does**
- Converts raw event logs into retention-ready events
- Establishes the rule for “active user” over time

**Key Concepts**
- Retention event definition  
- Activity-based user survival  
- Separation of business logic from metrics  

**Output**
- `retention_events (user_id, retention_date)`

---

### ✅ Day 27 — Retention Matrix  
**`02_retention_matrix.sql`**

Transforms retention events into a cohort-based matrix structure.

**What this step does**
- Aligns users by cohort (first activity month)
- Calculates time offsets from cohort start
- Aggregates retained users per cohort-period

**Key Concepts**
- Cohort month definition  
- Month offset calculation  
- Cohort-based aggregation  

**Output**
- Long-format retention matrix (pivot-ready)

---

### ✅ Day 28 — Retention Rate Metric  
**`03_retention_rate.sql`**

Converts retention counts into a standardized KPI.

**Retention Rate Formula**

- retention_rate = retained_users / cohort_size

**What this step does**
- Separates numerator and denominator explicitly
- Produces interpretable, time-based retention rates
- Formats results for reporting and dashboards

**Key Concepts**
- Retained users vs cohort size  
- Time-based retention measurement  
- BI-friendly metric design  

**Output**
- `cohort_month`
- `month_offset`
- `retained_users`
- `cohort_size`
- `retention_rate_pct`

---

## 🧠 Why Retention Analysis Matters

Retention is not just a metric —  
it reflects the **health and sustainability of a product or business**.

- **High retention** → strong product–market fit, long-term growth
- **Low retention** → issues in onboarding, UX, or value delivery

Retention analysis helps answer:

> **“Why do users stay — and when do they leave?”**

---

## 📌 한국어 요약

- **Day 26**: 리텐션 개념을 SQL로 명확히 정의
- **Day 27**: 코호트 기반 리텐션 매트릭스 생성
- **Day 28**: KPI로 활용 가능한 리텐션 비율 계산

이 폴더는  
**리텐션을 감각이 아닌 수치로 설명하는 SQL 분석 패턴 템플릿**입니다.

---

## 🚧 Status

**Completed (Day 26–28)**

This module forms a complete and reusable  
retention analysis workflow for:

- Analytics
- BI / Dashboarding
- Data science feature engineering