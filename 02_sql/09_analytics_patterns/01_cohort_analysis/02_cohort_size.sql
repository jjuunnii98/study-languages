/*
Day 24: Cohort Analysis - Cohort Size (코호트 크기 계산)

[EN]
This SQL calculates the size of each cohort,
defined as the number of unique users in their first cohort period.

Cohort size is the denominator for retention and LTV analysis.

[KR]
이 SQL은 각 코호트의 "초기 유저 수(Cohort Size)"를 계산한다.
코호트 크기는 이후 Retention, LTV 분석의 기준값(분모)이 된다.

------------------------------------------------------------
🧩 Assumed Schema (예시 스키마)
- events(user_id, event_time, event_type)

⚠️ 실제 테이블/컬럼명은 환경에 맞게 수정 필요
------------------------------------------------------------
*/

WITH base_events AS (
  /* 1) 코호트 기준 이벤트 필터링
     - 예: purchase, signup 등
  */
  SELECT
    user_id,
    event_time
  FROM events
  WHERE event_type = 'purchase'
),

first_event AS (
  /* 2) 유저별 첫 이벤트 시점 계산 */
  SELECT
    user_id,
    MIN(event_time) AS first_event_time
  FROM base_events
  GROUP BY user_id
),

cohort AS (
  /* 3) 코호트 기준 월 생성 */
  SELECT
    user_id,
    DATE_TRUNC('month', first_event_time) AS cohort_month
  FROM first_event
)

SELECT
  cohort_month,
  COUNT(DISTINCT user_id) AS cohort_size
FROM cohort
GROUP BY cohort_month
ORDER BY cohort_month;