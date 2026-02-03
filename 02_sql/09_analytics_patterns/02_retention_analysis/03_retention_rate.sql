/*
Day 28: Retention Analysis - Retention Rate Calculation

[EN]
This SQL calculates retention rate by period (e.g., month offset)
based on a predefined retention event and cohort definition.

Retention rate is defined as:
(number of retained users at period t) / (cohort size)

This file focuses on producing a clean, interpretable retention rate table
that can be directly used for reporting and visualization.

[KR]
이 SQL은 리텐션 비율(retention rate)을 기간(offset) 기준으로 계산한다.

리텐션 비율의 정의:
(특정 기간에 유지된 유저 수) / (해당 코호트의 전체 유저 수)

본 파일은 리포트 및 시각화에 바로 사용할 수 있는
정제된 리텐션 비율 테이블을 생성하는 데 초점을 둔다.
*/

------------------------------------------------------------
-- 🧩 Assumed Input Tables
--
-- cohort(user_id, cohort_month)
-- retention_events(user_id, retention_month)
--
-- ⚠️ Day 26에서 정의한 retention_events 사용
------------------------------------------------------------

WITH cohort_activity AS (
  /* 1) 코호트와 리텐션 이벤트 결합 */
  SELECT
    c.user_id,
    c.cohort_month,
    r.retention_month,
    (
      (DATE_PART('year', r.retention_month) - DATE_PART('year', c.cohort_month)) * 12
      + (DATE_PART('month', r.retention_month) - DATE_PART('month', c.cohort_month))
    )::int AS month_offset
  FROM cohort c
  JOIN retention_events r
    ON c.user_id = r.user_id
  WHERE r.retention_month >= c.cohort_month
),

retained_users AS (
  /* 2) 코호트 × offset별 유지된 유저 수 */
  SELECT
    cohort_month,
    month_offset,
    COUNT(DISTINCT user_id) AS retained_users
  FROM cohort_activity
  GROUP BY cohort_month, month_offset
),

cohort_size AS (
  /* 3) 코호트 크기(분모) */
  SELECT
    cohort_month,
    COUNT(DISTINCT user_id) AS cohort_size
  FROM cohort
  GROUP BY cohort_month
),

retention_rate AS (
  /* 4) 리텐션 비율 계산 */
  SELECT
    r.cohort_month,
    r.month_offset,
    r.retained_users,
    s.cohort_size,
    ROUND((r.retained_users::numeric / s.cohort_size) * 100, 2) AS retention_rate_pct
  FROM retained_users r
  JOIN cohort_size s
    ON r.cohort_month = s.cohort_month
)

SELECT
  cohort_month,
  month_offset,
  retained_users,
  cohort_size,
  retention_rate_pct
FROM retention_rate
ORDER BY cohort_month, month_offset;