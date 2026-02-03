/*
Day 27: Retention Analysis - Retention Matrix

[EN]
This SQL builds a retention matrix where:
- Rows represent cohort start periods
- Columns represent time offsets (e.g., weeks or months since cohort start)
- Values represent retention rate or active user count

The retention matrix is a standard output for product analytics,
allowing easy comparison of cohort behavior over time.

[KR]
이 SQL은 리텐션 매트릭스를 생성한다.
- 행(row): 코호트 시작 시점
- 열(column): 코호트 시작 이후 경과 기간(offset)
- 값(value): 리텐션 비율 또는 활성 유저 수

리텐션 매트릭스는
제품 분석, 성장 분석, 코호트 비교에서 가장 대표적인 결과물이다.
*/

------------------------------------------------------------
-- 🧩 Assumed Input Tables
--
-- retention_events(user_id, retention_month)
-- cohort(user_id, cohort_month)
--
-- ⚠️ Day 23~26에서 정의한 결과를 사용
------------------------------------------------------------

WITH cohort_activity AS (
  /* 1) 코호트 월과 리텐션 월 결합 */
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

retention_counts AS (
  /* 2) cohort_month × month_offset별 활성 유저 수 */
  SELECT
    cohort_month,
    month_offset,
    COUNT(DISTINCT user_id) AS active_users
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
    r.active_users,
    s.cohort_size,
    ROUND((r.active_users::numeric / s.cohort_size) * 100, 2) AS retention_rate_pct
  FROM retention_counts r
  JOIN cohort_size s
    ON r.cohort_month = s.cohort_month
)

SELECT
  cohort_month,
  month_offset,
  retention_rate_pct
FROM retention_rate
ORDER BY cohort_month, month_offset;