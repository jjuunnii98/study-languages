/*
Day 29: Funnel Analysis — Define Funnel Events

[EN]
This query defines funnel steps from raw event logs and produces
a user-level "first reach timestamp" per step.
It creates the canonical dataset used for funnel conversion metrics.

[KR]
이 쿼리는 Raw 이벤트 로그에서 퍼널 단계(step)를 정의하고,
각 사용자(user)가 각 단계에 "최초로 도달한 시간"을 산출합니다.
이 결과는 퍼널 전환율 계산의 표준 입력 데이터가 됩니다.

---------------------------------------
Assumptions (가정)
---------------------------------------
Table: events
- user_id        : user identifier
- event_time     : timestamp of event (UTC or local)
- event_name     : event type (e.g., page_view, sign_up, purchase)
- page           : optional (page path or screen name)
- properties     : optional (JSON) e.g., button_id, plan, etc.

Note:
- 실제 스키마에 맞춰 컬럼명만 바꿔서 사용하면 됩니다.
*/

WITH
/* ---------------------------------------
1) Define funnel step mapping
   - 이벤트를 퍼널 단계로 매핑
   - 실무에서는 "정의(매핑)"이 곧 지표의 신뢰도를 결정
--------------------------------------- */
funnel_step_map AS (
  SELECT 1 AS step_order, 'visit'     AS step_name, 'page_view' AS event_name
  UNION ALL
  SELECT 2 AS step_order, 'signup'    AS step_name, 'sign_up'   AS event_name
  UNION ALL
  SELECT 3 AS step_order, 'activate'  AS step_name, 'activate'  AS event_name
  UNION ALL
  SELECT 4 AS step_order, 'purchase'  AS step_name, 'purchase'  AS event_name
),

/* ---------------------------------------
2) Filter raw events
   - 분석 대상 이벤트만 남김
   - 기간/봇/테스트 계정 등 필터링은 여기서 처리하는게 표준
--------------------------------------- */
filtered_events AS (
  SELECT
    e.user_id,
    e.event_time,
    e.event_name
  FROM events e
  WHERE 1=1
    AND e.user_id IS NOT NULL
    AND e.event_time IS NOT NULL
    -- ✅ 필요 시 기간 필터 (예시)
    -- AND e.event_time >= TIMESTAMP '2026-01-01'
    -- AND e.event_time <  TIMESTAMP '2026-02-01'
    -- ✅ 테스트/봇 제외 규칙(예시)
    -- AND e.user_id NOT IN ('test_user_1', 'internal_admin')
),

/* ---------------------------------------
3) Map events to funnel steps
   - event_name 기준으로 step을 부여
--------------------------------------- */
mapped_funnel_events AS (
  SELECT
    fe.user_id,
    fe.event_time,
    fsm.step_order,
    fsm.step_name
  FROM filtered_events fe
  JOIN funnel_step_map fsm
    ON fe.event_name = fsm.event_name
),

/* ---------------------------------------
4) User-level "first reach" timestamp per step
   - 같은 step 이벤트가 여러 번 발생할 수 있으므로 MIN(event_time)
--------------------------------------- */
user_step_first_reach AS (
  SELECT
    user_id,
    step_order,
    step_name,
    MIN(event_time) AS first_reach_time
  FROM mapped_funnel_events
  GROUP BY user_id, step_order, step_name
)

/* ---------------------------------------
Final Output
---------------------------------------
Output columns:
- user_id
- step_order
- step_name
- first_reach_time (user가 해당 step에 최초 도달한 시각)

이 결과를 기반으로:
- step별 도달 사용자수
- step간 전환율
- step별 소요시간(time-to-step)
을 계산할 수 있다.
--------------------------------------- */
SELECT
  user_id,
  step_order,
  step_name,
  first_reach_time
FROM user_step_first_reach
ORDER BY user_id, step_order;