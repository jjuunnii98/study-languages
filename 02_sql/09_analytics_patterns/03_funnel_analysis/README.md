# Funnel Analysis (SQL)

This directory covers **funnel analysis patterns** using SQL.  
A funnel answers a core product and growth question:

> **“Where do users drop off, and which step is the bottleneck?”**

본 디렉토리는 SQL로 퍼널 분석을 수행하는 표준 흐름을 다룹니다.  
퍼널 분석은 유저가 특정 목표(예: 구매, 가입, 활성화)에 도달하기까지  
어느 단계에서 이탈하는지(병목)를 정량적으로 파악합니다.

---

## 🎯 Objectives

- Define funnel steps consistently from raw event logs
- Convert noisy event data into a canonical “user × step × first reach time” dataset
- Count unique users reaching each step (step counts)
- Compute step-to-step conversion rates
- Produce outputs that are directly usable for BI dashboards and reporting

---

## 📂 File Structure & Progress

Each file represents one analytical step.  
Later steps build directly on earlier definitions.

### ✅ Day 29 — Define Funnel Events  
**`01_define_funnel_events.sql`**

- Raw 이벤트 로그에서 퍼널 단계(step)를 정의
- 이벤트를 step으로 매핑하고, 사용자별 step “최초 도달 시각” 산출

**Key Concepts**
- Funnel step mapping (step_order, step_name)
- Filtering raw events (기간/테스트/봇 제외 등)
- First reach timestamp per step (`MIN(event_time)`)

**Output**
- Canonical dataset:
  - `user_id`
  - `step_order`
  - `step_name`
  - `first_reach_time`

---

### ✅ Day 30 — Step Counts  
**`02_step_counts.sql`**

- 각 step에 도달한 “고유 사용자 수” 계산
- Drop-off(이탈) 확인을 위한 기본 테이블 생성

**Key Concepts**
- `COUNT(DISTINCT user_id)` for unique reach
- Step-level aggregation
- (Optional) Cohort-based step counts design (BI 친화)

**Output**
- `step_order`
- `step_name`
- `users_reached`

---

### ✅ Day 31 — Conversion Rates  
**`03_conversion_rates.sql`**

- 단계 간 전환율 계산
- “이전 step 도달자 대비 다음 step 도달자 비율”을 KPI로 산출

**Key Concepts**
- Step-to-step conversion:
  - `users(step N+1) / users(step N)`
- Safe join with previous step (robust to funnel edits)
- Zero/NULL handling for reporting stability

**Output**
- `step_order`
- `step_name`
- `users_reached`
- `prev_step_users`
- `conversion_rate_pct`

---

## 🧠 Why Funnel Analysis Matters

Funnel metrics are essential for:
- Product onboarding optimization
- Conversion rate improvement
- Growth experiments and A/B testing
- Diagnosing UX friction and step-level bottlenecks

A funnel is not just a metric —  
it is an actionable map of user behavior.

---

## 📌 한국어 요약

- Day 29: 퍼널 단계 정의 + 사용자별 step 최초 도달 시각 생성
- Day 30: step별 도달 사용자 수(step counts) 계산
- Day 31: 단계 간 전환율(conversion rates) 산출

이 폴더는  
**퍼널 정의 → 정규화 → 집계 → KPI화**까지 완결된 분석 템플릿입니다.

---

## 🚧 Status

**Completed (Day 29–31)**  
Next recommended steps:
- Time-to-convert (step 간 소요시간 분석)
- Funnel breakdown by segment (채널/국가/디바이스 등)
- Visualization-ready outputs for BI dashboards