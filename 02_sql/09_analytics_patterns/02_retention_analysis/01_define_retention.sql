/*
Day 26: Retention Analysis - Define Retention Event

[EN]
This SQL defines what "retention" means in an analytical context.
Retention is not just repeated activity, but a business-defined signal
(e.g., purchase, login, core action).

This file creates a clean retention event table that can be reused
for cohort retention, rolling retention, or LTV analysis.

[KR]
이 SQL은 "리텐션(retention)"의 정의를 명확히 분리한다.
리텐션은 단순한 재방문이 아니라,
비즈니스적으로 의미 있는 핵심 행동(core event)을 기준으로 정의되어야 한다.

본 파일은 이후 코호트 리텐션, 롤링 리텐션, LTV 분석에
공통으로 재사용 가능한 retention 이벤트 테이블을 만든다.
*/

------------------------------------------------------------
-- 🧩 Assumed Base Schema
-- events(
--   user_id,
--   event_time,
--   event_type
-- )
------------------------------------------------------------

WITH filtered_events AS (
  /* 1) 리텐션을 정의할 핵심 이벤트 필터링
     - 예: purchase, login, core_action
     - 분석 목적에 따라 event_type 조건 변경
  */
  SELECT
    user_id,
    event_time
  FROM events
  WHERE event_type = 'purchase'
),

retention_events AS (
  /* 2) 유저별 리텐션 이벤트 정규화
     - event_time을 날짜/월 단위로 변환 가능
     - 이후 분석에서 기준 시점으로 사용
  */
  SELECT
    user_id,
    event_time,
    DATE(event_time) AS retention_date,
    DATE_TRUNC('month', event_time) AS retention_month
  FROM filtered_events
)

SELECT
  user_id,
  event_time,
  retention_date,
  retention_month
FROM retention_events
ORDER BY user_id, event_time;