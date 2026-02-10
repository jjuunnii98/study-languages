# Analytics Patterns (SQL)

This directory contains **advanced analytics patterns implemented purely in SQL**.  
Each submodule represents a reusable analytical framework commonly used in
product analytics, growth analysis, and data-driven decision-making.

> **From raw events → analytical structure → decision-ready metrics**

본 디렉토리는 SQL을 활용해  
실무에서 반복적으로 사용되는 **분석 패턴(Analytics Patterns)** 을  
체계적으로 정리한 포트폴리오입니다.

---

## 🎯 Objectives

- Transform raw event data into analytical insights
- Apply cohort-based and time-based thinking using SQL
- Build reusable SQL templates for analytics & BI
- Demonstrate end-to-end analytical reasoning (definition → metric → interpretation)
- Prepare SQL-based analytics portfolio for graduate research & industry use

---

## 📂 Modules Overview

### 1️⃣ Cohort Analysis  
📁 `01_cohort_analysis/`

Analyze user behavior based on **first engagement time**.

**Key Questions**
- When did users first join?
- How large is each cohort?
- How does engagement evolve by cohort?

**Key Techniques**
- Cohort definition (`first_event_date`)
- Cohort sizing
- Retention by cohort

**Days**
- Day 23–25

---

### 2️⃣ Retention Analysis  
📁 `02_retention_analysis/`

Measure **how many users remain active over time** after initial engagement.

**Key Questions**
- How many users come back after N days?
- How does retention differ across cohorts?

**Key Techniques**
- Retention event definition
- Retention matrix construction
- Retention rate calculation

**Days**
- Day 26–28

---

### 3️⃣ Funnel Analysis  
📁 `03_funnel_analysis/`

Track **user drop-off across sequential steps**.

**Key Questions**
- Where do users drop off?
- Which step has the biggest friction?
- What is the overall conversion rate?

**Key Techniques**
- Funnel step definition
- Step-wise user counts
- Conversion rate calculation

**Days**
- Day 29–31

---

### 4️⃣ Time Series Analysis  
📁 `04_time_series_analysis/`

Understand **how metrics evolve over time** and compare against past periods.

**Key Questions**
- Is the metric growing or declining?
- Is change meaningful or just noise?
- How does today compare to yesterday or last week?

**Key Techniques**
- Time bucket aggregation
- Moving averages
- Period-over-period (DoD / WoW / MoM) analysis

**Days**
- Day 32–34

---

## 🧠 Why Analytics Patterns Matter

Analytics patterns are not just SQL queries —  
they represent **ways of thinking about data**.

These patterns enable you to:
- Move beyond simple counts and sums
- Reason about time, cohorts, and user journeys
- Translate raw data into actionable insights
- Communicate findings clearly to stakeholders

In both **graduate research** and **industry analytics**,  
these patterns form the foundation of serious data work.

---

## 📌 한국어 요약

- 코호트, 리텐션, 퍼널, 시계열 분석을 SQL로 체계화
- 이벤트 데이터 → 분석 구조 → 지표 계산의 전체 흐름 구현
- BI·리포트·연구 모두에 재사용 가능한 SQL 템플릿 제공
- 단순 문법이 아닌 **분석 사고력 중심 포트폴리오**

---

## 🚧 Status

**Completed (Day 23–34)**  

This directory represents a complete, practical SQL analytics framework  
suitable for:
- Product analytics
- Growth analysis
- BI dashboards
- Graduate-level data analytics portfolios