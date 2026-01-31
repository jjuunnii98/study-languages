/*
Day 23: Cohort Analysis - Define Cohort (코호트 정의)

[EN]
This SQL defines a user cohort based on the user's first activity (first purchase / first signup / first event).
A cohort is typically grouped by the month (or week) of the first event.

[KR]
이 SQL은 사용자의 "첫 활동(첫 구매/첫 가입/첫 이벤트)"를 기준으로 코호트를 정의한다.
코호트는 보통 첫 활동이 발생한 월(Month) 또는 주(Week) 단위로 묶는다.

------------------------------------------------------------
🧩 Assumed Schema (예시 스키마)
- events(user_id, event_time, event_type)
  또는
- orders(user_id, order_time, order_id, revenue)

✅ You should replace table/column names with your actual schema.
------------------------------------------------------------
*/

WITH base_events AS (
  /* 1) 분석 대상 이벤트만 필터링
     - 예: signup / purchase 같은 "코호트 기준 이벤트"를 선택
     - 상황에 따라 event_type 조건을 제거해도 됨
  */
  SELECT
    user_id,
    event_time
  FROM events
  WHERE event_type = 'purchase'
),

first_event AS (
  /* 2) 유저별 첫 이벤트 시점 계산 (코호트 기준)
     - MIN(event_time) = 첫 구매/첫 활동 시점
  */
  SELECT
    user_id,
    MIN(event_time) AS first_event_time
  FROM base_events
  GROUP BY user_id
),

cohort AS (
  /* 3) 코호트 라벨 생성 (월 단위)
     - DB별로 날짜 함수가 다를 수 있음
     - 아래 예시는 PostgreSQL 기준: DATE_TRUNC('month', timestamp)

     MySQL이라면:
       DATE_FORMAT(first_event_time, '%Y-%m-01') AS cohort_month

     BigQuery라면:
       DATE_TRUNC(DATE(first_event_time), MONTH) AS cohort_month
  */
  SELECT
    user_id,
    first_event_time,
    DATE_TRUNC('month', first_event_time) AS cohort_month
  FROM first_event
)

SELECT
  cohort_month,
  COUNT(DISTINCT user_id) AS cohort_users
FROM cohort
GROUP BY cohort_month
ORDER BY cohort_month;