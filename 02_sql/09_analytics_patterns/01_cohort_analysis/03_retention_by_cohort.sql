/*
Day 25: Cohort Analysis - Retention by Cohort (코호트 잔존율 계산)

[EN]
This SQL calculates cohort retention by:
1) Defining each user's cohort month (first event month)
2) Computing each user's activity month (event month)
3) Calculating the month offset between cohort_month and activity_month
4) Aggregating active users per cohort_month and offset
5) Joining with cohort_size to compute retention_rate

[KR]
이 SQL은 코호트 잔존율(retention)을 다음 흐름으로 계산한다:
1) 유저별 코호트 월(cohort_month) 정의 (첫 이벤트 월)
2) 유저별 활동 월(activity_month) 생성 (이벤트가 발생한 월)
3) cohort_month 대비 활동 월의 차이(offset, 개월 수) 계산
4) 코호트별/offset별 활성 유저 수(active_users) 집계
5) cohort_size와 결합해 retention_rate 계산

------------------------------------------------------------
🧩 Assumed Schema (예시 스키마)
- events(user_id, event_time, event_type)

⚠️ DB/스키마에 맞게 테이블명/컬럼명 및 날짜 함수 조정 필요
------------------------------------------------------------
*/

WITH base_events AS (
  /* 1) 코호트 분석에 사용할 이벤트 필터링 (예: purchase)
     - signup 코호트면 event_type='signup'로 변경
  */
  SELECT
    user_id,
    event_time
  FROM events
  WHERE event_type = 'purchase'
),

first_event AS (
  /* 2) 유저별 첫 이벤트 시점(코호트 기준 시점) */
  SELECT
    user_id,
    MIN(event_time) AS first_event_time
  FROM base_events
  GROUP BY user_id
),

cohort AS (
  /* 3) 코호트 월(cohort_month) 생성 */
  SELECT
    user_id,
    DATE_TRUNC('month', first_event_time) AS cohort_month
  FROM first_event
),

activity AS (
  /* 4) 활동 월(activity_month) 생성
     - 유저가 이벤트를 발생시킨 월 단위로 변환
     - DISTINCT로 같은 월 중복 이벤트는 1번 활동으로 처리 (active user 기준)
  */
  SELECT DISTINCT
    user_id,
    DATE_TRUNC('month', event_time) AS activity_month
  FROM base_events
),

cohort_activity AS (
  /* 5) cohort_month 대비 activity_month의 offset(개월 차) 계산
     - offset = 0이면 첫 달(코호트 진입 달)
     - offset = 1이면 다음 달 retention

     PostgreSQL: DATE_PART로 월 차이 계산
  */
  SELECT
    c.cohort_month,
    a.activity_month,
    (
      (DATE_PART('year', a.activity_month) - DATE_PART('year', c.cohort_month)) * 12
      + (DATE_PART('month', a.activity_month) - DATE_PART('month', c.cohort_month))
    )::int AS month_offset,
    a.user_id
  FROM cohort c
  JOIN activity a
    ON c.user_id = a.user_id
  WHERE a.activity_month >= c.cohort_month
),

retention_counts AS (
  /* 6) 코호트 월 × offset별 활성 유저 수 집계 */
  SELECT
    cohort_month,
    month_offset,
    COUNT(DISTINCT user_id) AS active_users
  FROM cohort_activity
  GROUP BY cohort_month, month_offset
),

cohort_size AS (
  /* 7) 코호트 크기(초기 유저 수) 계산 */
  SELECT
    cohort_month,
    COUNT(DISTINCT user_id) AS cohort_size
  FROM cohort
  GROUP BY cohort_month
)

SELECT
  r.cohort_month,
  r.month_offset,
  r.active_users,
  s.cohort_size,
  ROUND((r.active_users::numeric / s.cohort_size) * 100, 2) AS retention_rate_pct
FROM retention_counts r
JOIN cohort_size s
  ON r.cohort_month = s.cohort_month
ORDER BY r.cohort_month, r.month_offset;