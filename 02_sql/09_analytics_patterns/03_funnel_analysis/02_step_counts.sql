/*
Day 30: Funnel Analysis — Step Counts

[EN]
This query computes the number of unique users who reached each funnel step.
It is designed to work on top of the canonical dataset created in Day 29:
(user_id, step_order, step_name, first_reach_time).

[KR]
이 쿼리는 퍼널의 각 단계(step)에 도달한 "고유 사용자 수"를 계산합니다.
Day 29에서 정의한 표준 결과(유저×스텝×최초도달시간)를 입력으로 사용합니다.

----------------------------------------------------
Input (Day 29 output)
----------------------------------------------------
- user_id
- step_order
- step_name
- first_reach_time

Output
- step_order
- step_name
- users_reached (해당 step에 도달한 사용자 수)
- (optional) cohort_date 기반 step counts
*/

WITH
/* ----------------------------------------------------
1) Canonical funnel dataset (Day 29 result)
   - 실제 환경에서는 Day 29 결과를 VIEW/CTE로 저장해도 좋다.
---------------------------------------------------- */
funnel_user_steps AS (
  -- ✅ Day 29 SQL을 VIEW로 만들어 두었다면 여기서 SELECT 하면 됨
  -- SELECT * FROM analytics.funnel_user_steps;

  -- 여기서는 Day 29 로직을 참조해서 "존재한다고 가정"한다.
  SELECT
    user_id,
    step_order,
    step_name,
    first_reach_time
  FROM funnel_user_steps_source
  -- ↑ 실제로는:
  -- 1) Day 29 결과를 테이블/뷰로 만들어서 사용하거나
  -- 2) Day 29 CTE를 그대로 붙여넣고 마지막 SELECT만 변경한다.
),

/* ----------------------------------------------------
2) Step counts (global)
   - step별 도달한 사용자 수 (고유 user_id)
---------------------------------------------------- */
step_counts_global AS (
  SELECT
    step_order,
    step_name,
    COUNT(DISTINCT user_id) AS users_reached
  FROM funnel_user_steps
  GROUP BY step_order, step_name
),

/* ----------------------------------------------------
3) (Optional) Cohort definition
   - cohort: 예) 첫 방문(visit) step의 first_reach_time 날짜
   - BI/리포트에서 cohort별 퍼널 drop을 비교할 때 유용

   ※ cohort를 월 단위로 바꾸고 싶으면 DATE_TRUNC('month', ...) 사용
---------------------------------------------------- */
user_cohort AS (
  SELECT
    user_id,
    MIN(CASE WHEN step_order = 1 THEN first_reach_time END) AS cohort_ts
  FROM funnel_user_steps
  GROUP BY user_id
),

step_counts_by_cohort AS (
  SELECT
    -- cohort_date: 일 단위 기준
    CAST(uc.cohort_ts AS DATE) AS cohort_date,
    fus.step_order,
    fus.step_name,
    COUNT(DISTINCT fus.user_id) AS users_reached
  FROM funnel_user_steps fus
  JOIN user_cohort uc
    ON fus.user_id = uc.user_id
  WHERE uc.cohort_ts IS NOT NULL
  GROUP BY CAST(uc.cohort_ts AS DATE), fus.step_order, fus.step_name
)

-- ----------------------------------------------------
-- Final Output
-- 1) Global step counts
-- 2) Cohort step counts (optional)
-- ----------------------------------------------------

/* ✅ 1) Global step counts */
SELECT
  step_order,
  step_name,
  users_reached
FROM step_counts_global
ORDER BY step_order;

/*
✅ 2) Cohort step counts가 필요하면 위 SELECT를 주석 처리하고 아래를 사용

SELECT
  cohort_date,
  step_order,
  step_name,
  users_reached
FROM step_counts_by_cohort
ORDER BY cohort_date, step_order;
*/