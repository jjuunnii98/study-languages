# Cohort Analysis (코호트 분석)

This module covers **cohort analysis using SQL**, a core analytics pattern
widely used in product analytics, growth analysis, and retention modeling.

Cohort analysis answers questions such as:
- How many users stay active after their first interaction?
- How does retention change over time for different user cohorts?
- Are newer cohorts behaving better or worse than older ones?

본 폴더는 SQL을 활용한 **코호트 분석의 전체 흐름**을 단계적으로 정리합니다.  
코호트 분석은 사용자 행동 분석, 리텐션 분석, 성장 지표 분석에서
가장 핵심적인 분석 패턴 중 하나입니다.

---

## 🎯 Learning Objectives

- Define cohorts based on users’ first activity
- Calculate cohort sizes as a baseline
- Measure retention by time offset (month-based)
- Build reusable SQL patterns for product analytics
- Prepare cohort outputs for reporting and visualization

---

## 📂 Structure & Progress

Each SQL file represents one logical step in the cohort analysis pipeline.
Files are designed to be executed sequentially.

각 SQL 파일은 코호트 분석의 한 단계를 담당하며,  
순차적으로 실행하면 완전한 코호트 리텐션 분석 결과를 얻을 수 있습니다.

### ✅ Completed

#### 1️⃣ `01_define_cohort.sql` (Day 23)
**Cohort Definition (코호트 정의)**

- 유저별 첫 이벤트 시점을 기준으로 cohort_month 정의
- `MIN(event_time)`을 활용한 최초 활동 기준 설정
- `DATE_TRUNC('month')`로 월 단위 코호트 생성

📌 핵심 개념  
> “코호트란, 동일한 시작 시점을 공유하는 사용자 집단이다.”

---

#### 2️⃣ `02_cohort_size.sql` (Day 24)
**Cohort Size Calculation (코호트 크기 계산)**

- cohort_month별 유저 수 집계
- 이후 리텐션 계산을 위한 분모(baseline) 생성
- `COUNT(DISTINCT user_id)` 활용

📌 핵심 개념  
> “Retention은 반드시 cohort_size를 기준으로 계산된다.”

---

#### 3️⃣ `03_retention_by_cohort.sql` (Day 25)
**Retention by Month Offset (코호트 잔존율 계산)**

- cohort_month 대비 활동 월(activity_month) 계산
- cohort_month와 activity_month 간의 month_offset 산출
- offset별 활성 유저 수(active_users) 집계
- cohort_size와 결합하여 retention_rate(%) 계산

📌 핵심 개념  
> “Retention은 ‘예측’이 아니라 ‘시간에 따른 생존/잔존’의 문제다.”

---

## 🧠 Key Concepts Summary

- **Cohort Month**  
  유저가 처음으로 핵심 이벤트를 수행한 월

- **Activity Month**  
  유저가 실제로 활동한 월

- **Month Offset**  
  cohort_month 기준으로 몇 개월 뒤에 활동했는지  
  (0 = 첫 달, 1 = 다음 달, …)

- **Active Users**  
  특정 cohort_month × offset 조합에서 활동한 유저 수

- **Retention Rate**  
  `active_users / cohort_size`

---

## 🧩 Typical Use Cases

- Product user retention analysis
- Subscription churn analysis
- Growth cohort comparison (early vs recent cohorts)
- Behavioral analysis for feature adoption
- Foundation for cohort retention matrix & LTV analysis

---

## 🔗 Next Steps

This module can be extended into:
- Retention matrix (pivoted cohort table)
- Cohort-based churn analysis
- LTV estimation by cohort
- Visualization with BI tools or Python

이 폴더는 이후:
- 코호트 매트릭스
- LTV 분석
- Python/BI 시각화
로 자연스럽게 확장될 수 있습니다.

---

## 🚧 Status

**Completed (Day 23–25)**

This cohort analysis module provides a complete,
end-to-end SQL-based retention analysis pipeline.

본 코호트 분석 파트는  
SQL 기반 리텐션 분석의 완성된 기본 템플릿입니다.