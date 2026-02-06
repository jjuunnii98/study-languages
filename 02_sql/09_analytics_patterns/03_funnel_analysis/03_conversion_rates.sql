/*
Day 31: Funnel Analysis — Conversion Rates

[EN]
This query computes step-to-step conversion rates in a funnel.
It answers the core question:
"Of users who reached step N, how many progressed to step N+1?"

[KR]
이 쿼리는 퍼널 각 단계 간 전환율(conversion rate)을 계산합니다.
즉,
- 이전 단계(step N)에 도달한 사용자 중
- 다음 단계(step N+1)로 이동한 비율
을 정량적으로 산출합니다.

----------------------------------------------------
Input (from Day 29–30)
----------------------------------------------------
- user_id
- step_order
- step_name
- first_reach_time

----------------------------------------------------
Output
----------------------------------------------------
- step_order
- step_name
- users_reached
- prev_step_users
- conversion_rate_pct
*/

WITH
/* ----------------------------------------------------
1) Canonical funnel dataset
   - Day 29에서 정의한 user × step × first_reach_time
---------------------------------------------------- */
funnel_user_steps AS (
  SELECT
    user_id,
    step_order,
    step_name,
    first_reach_time
  FROM funnel_user_steps_source
  -- 실제 환경에서는:
  -- VIEW 또는 Day29 CTE 결과를 참조
),

/* ----------------------------------------------------
2) Step-level user counts
   - 각 step에 도달한 사용자 수
---------------------------------------------------- */
step_counts AS (
  SELECT
    step_order,
    step_name,
    COUNT(DISTINCT user_id) AS users_reached
  FROM funnel_user_steps
  GROUP BY step_order, step_name
),

/* ----------------------------------------------------
3) Join with previous step
   - step N과 step N-1을 연결
---------------------------------------------------- */
step_with_prev AS (
  SELECT
    curr.step_order,
    curr.step_name,
    curr.users_reached,
    prev.users_reached AS prev_step_users
  FROM step_counts curr
  LEFT JOIN step_counts prev
    ON curr.step_order = prev.step_order + 1
)

/* ----------------------------------------------------
Final Output: Conversion Rates
---------------------------------------------------- */
SELECT
  step_order,
  step_name,
  users_reached,
  prev_step_users,

  CASE
    WHEN prev_step_users IS NULL THEN NULL
    WHEN prev_step_users = 0 THEN 0
    ELSE ROUND(
      (users_reached::DECIMAL / prev_step_users) * 100,
      2
    )
  END AS conversion_rate_pct

FROM step_with_prev
ORDER BY step_order;